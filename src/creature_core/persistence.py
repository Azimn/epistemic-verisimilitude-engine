from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .catalog import Desire, DesireSource
from .learning import DecisionTreeOpinion
from .model import (
    AttentionState,
    Belief,
    ContextRecord,
    ExpressionState,
    MimicEpisode,
    Personality,
    PlayerModel,
    RelationState,
)


class PersistenceMixin:
    """Serialization of the cognitive mind separately from body/world state.

    Black & White serializes CreatureMental independently enough that community
    tools can transplant a trained mind across creature bodies. This JSON format
    is a project extension for experiments, not a reconstruction of Lionhead's
    binary .erc layout.
    """

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "eve-creature-core-mind-v1",
            "seed": self.seed,
            "tick": self.tick,
            "creature_type": self.creature_type,
            "development_stage": self.development_stage,
            "personality": asdict(self.personality),
            "attention": asdict(self.attention),
            "expression": {
                "valence": self.expression.valence,
                "arousal": self.expression.arousal,
                "dominant_desire": self.expression.dominant_desire.name if self.expression.dominant_desire else None,
            },
            "exploration_visits": dict(self.exploration_visits),
            "relations": {k: asdict(v) for k, v in self.relations.items()},
            "mimic_history": [
                {
                    "tick": e.tick,
                    "action": e.action,
                    "target_id": e.target_id,
                    "inferred_desires": {d.name: v for d, v in e.inferred_desires.items()},
                }
                for e in self.mimic_history
            ],
            "beliefs": {
                k: {
                    "object_id": v.object_id,
                    "kind": v.kind,
                    "attributes": v.attributes,
                    "first_seen": v.first_seen,
                    "last_seen": v.last_seen,
                    "confidence": v.confidence,
                    "inspections": v.inspections,
                    "object_opinions": v.object_opinions,
                }
                for k, v in self.beliefs.items()
            },
            "desires": {
                d.name: {
                    "value": s.value,
                    "previous": s.previous,
                    "baseline": s.baseline,
                    "growth_rate": s.growth_rate,
                    "decay": s.decay,
                    "threshold": s.threshold,
                    "active": s.active,
                    "suppressed_until": s.suppressed_until,
                    "source_values": {k.name: v for k, v in s.source_values.items()},
                }
                for d, s in self.desires.items()
            },
            "source_weights": {s.name: v for s, v in self.source_weights.items()},
            "action_opinions": {f"{d.name}|{a}": v for (d, a), v in self.action_opinions.items()},
            "opinion_trees": {f"{d.name}|{a}": t.to_dict() for (d, a), t in self.opinion_trees.items()},
            "player_model": {
                "inferred_desires": {d.name: v for d, v in self.player_model.inferred_desires.items()},
                "trust": self.player_model.trust,
                "affection": self.player_model.affection,
                "fear": self.player_model.fear,
                "respect": self.player_model.respect,
                "last_interaction_tick": self.player_model.last_interaction_tick,
            },
            "known_actions": sorted(self.known_actions),
            "previous_actions": list(self.previous_actions),
            "dominant_desire": self._dominant_desire.name,
            "context_history": [
                {
                    "tick": c.tick,
                    "desire": c.desire.name,
                    "desire_source": c.desire_source.name if c.desire_source else None,
                    "action": c.action,
                    "target_id": c.target_id,
                    "features": c.features,
                    "predicted_utility": c.predicted_utility,
                    "outcome": c.outcome,
                }
                for c in self.context_history
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, seed: int | None = None, creature_type: str | None = None):
        obj = cls(
            seed=int(data.get("seed", 1) if seed is None else seed),
            personality=Personality(**data.get("personality", {})),
            creature_type=creature_type or data.get("creature_type", "generic"),
        )
        obj.tick = int(data.get("tick", 0))
        obj.development_stage = float(data.get("development_stage", 0.5))

        if data.get("attention"):
            obj.attention = AttentionState(**data["attention"])
        if data.get("expression"):
            ex = data["expression"]
            obj.expression = ExpressionState(
                float(ex.get("valence", 0.0)),
                float(ex.get("arousal", 0.0)),
                Desire[ex["dominant_desire"]] if ex.get("dominant_desire") else None,
            )

        obj.exploration_visits = {str(k): int(v) for k, v in data.get("exploration_visits", {}).items()}
        obj.relations = {k: RelationState(**v) for k, v in data.get("relations", {}).items()}
        obj.mimic_history.extend(
            MimicEpisode(
                int(e["tick"]),
                e["action"],
                e.get("target_id"),
                {Desire[k]: float(v) for k, v in e.get("inferred_desires", {}).items()},
            )
            for e in data.get("mimic_history", [])
        )

        obj.beliefs = {
            k: Belief(
                object_id=v["object_id"],
                kind=v["kind"],
                attributes=dict(v.get("attributes", {})),
                first_seen=int(v["first_seen"]),
                last_seen=int(v["last_seen"]),
                confidence=float(v.get("confidence", 1.0)),
                inspections=int(v.get("inspections", 0)),
                object_opinions={a: float(x) for a, x in v.get("object_opinions", {}).items()},
            )
            for k, v in data.get("beliefs", {}).items()
        }

        for name, raw in data.get("desires", {}).items():
            d = Desire[name]
            s = obj.desires[d]
            for attr in ("value", "previous", "baseline", "growth_rate", "decay", "threshold"):
                if attr in raw:
                    setattr(s, attr, float(raw[attr]))
            s.active = bool(raw.get("active", True))
            s.suppressed_until = int(raw.get("suppressed_until", 0))
            s.source_values = {DesireSource[k]: float(v) for k, v in raw.get("source_values", {}).items()}

        obj.source_weights.update({DesireSource[k]: float(v) for k, v in data.get("source_weights", {}).items()})

        for key, value in data.get("action_opinions", {}).items():
            d, action = key.split("|", 1)
            obj.action_opinions[(Desire[d], action)] = float(value)
        for key, raw in data.get("opinion_trees", {}).items():
            d, action = key.split("|", 1)
            obj.opinion_trees[(Desire[d], action)] = DecisionTreeOpinion.from_dict(raw)

        pm = data.get("player_model", {})
        obj.player_model = PlayerModel(
            inferred_desires={Desire[k]: float(v) for k, v in pm.get("inferred_desires", {}).items()},
            trust=float(pm.get("trust", 0.5)),
            affection=float(pm.get("affection", 0.5)),
            fear=float(pm.get("fear", 0.0)),
            respect=float(pm.get("respect", 0.5)),
            last_interaction_tick=int(pm.get("last_interaction_tick", -1)),
        )

        obj.known_actions = set(data.get("known_actions", obj.known_actions))
        obj.previous_actions.extend(data.get("previous_actions", []))
        obj._dominant_desire = Desire[data.get("dominant_desire", "LOOK_AROUND")]

        for raw in data.get("context_history", []):
            obj.context_history.append(
                ContextRecord(
                    tick=int(raw["tick"]),
                    desire=Desire[raw["desire"]],
                    desire_source=DesireSource[raw["desire_source"]] if raw.get("desire_source") else None,
                    action=raw["action"],
                    target_id=raw.get("target_id"),
                    features=dict(raw.get("features", {})),
                    predicted_utility=float(raw.get("predicted_utility", 0.0)),
                    outcome=raw.get("outcome"),
                )
            )
        return obj

    def save_mind(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load_mind(cls, path: str | Path, *, seed: int | None = None, creature_type: str | None = None):
        return cls.from_dict(
            json.loads(Path(path).read_text(encoding="utf-8")),
            seed=seed,
            creature_type=creature_type,
        )

    def fingerprint(self) -> dict[str, Any]:
        """Compact state summary for matched-history and transplant experiments."""
        top_desires = sorted(((s.value, d.name) for d, s in self.desires.items()), reverse=True)[:8]
        top_opinions = sorted(
            ((abs(v), d.name, a, v) for (d, a), v in self.action_opinions.items()),
            reverse=True,
        )[:12]
        return {
            "tick": self.tick,
            "belief_count": len(self.beliefs),
            "top_desires": [(n, round(v, 4)) for v, n in top_desires],
            "top_action_opinions": [(d, a, round(v, 4)) for _, d, a, v in top_opinions],
            "player_model": {
                "trust": round(self.player_model.trust, 4),
                "affection": round(self.player_model.affection, 4),
                "fear": round(self.player_model.fear, 4),
            },
        }
