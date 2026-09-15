from __future__ import annotations

from typing import Any

from .catalog import Desire
from .model import Belief, MimicEpisode, Percept, PlayerObservation, RelationState, clamp


def _ema(old: float, new: float, alpha: float) -> float:
    return old + alpha * (new - old)


class PerceptionMixin:
    def perceive(self, percepts: list[Percept]) -> None:
        seen: set[str] = set()
        focus_candidates: list[tuple[float, str]] = []
        for p in percepts:
            seen.add(p.object_id)
            old = self.beliefs.get(p.object_id)
            was_new = old is None
            if old is None:
                self.beliefs[p.object_id] = Belief(
                    object_id=p.object_id,
                    kind=p.kind,
                    attributes=dict(p.attributes),
                    first_seen=self.tick,
                    last_seen=self.tick,
                    confidence=clamp(0.65 + 0.35 * p.salience),
                )
            else:
                old.kind = p.kind
                old.attributes.update(p.attributes)
                old.last_seen = self.tick
                old.confidence = clamp(old.confidence + 0.25 * p.salience)

            belief = self.beliefs[p.object_id]
            novelty = 1.0 if was_new else max(0.0, 1.0 - belief.confidence)
            threat = float(belief.attributes.get("threat", 0.0)) + float(belief.attributes.get("scary_magic", 0.0))
            persistence = 0.20 if self.attention.focused_object_id == p.object_id else 0.0
            focus_candidates.append((p.salience + 0.45 * novelty + 0.65 * threat + persistence, p.object_id))

            if p.kind in {"player", "creature", "villager"}:
                rel = self.relations.setdefault(p.object_id, RelationState(p.object_id))
                rel.familiarity = clamp(rel.familiarity + 0.015 + 0.02 * p.salience)
                rel.last_seen = self.tick

        for object_id, belief in self.beliefs.items():
            if object_id not in seen:
                age = max(1, self.tick - belief.last_seen)
                belief.confidence = max(0.05, belief.confidence * (0.995 ** age))

        if focus_candidates:
            focus_candidates.sort(reverse=True)
            chosen = focus_candidates[0][1]
            if chosen != self.attention.focused_object_id:
                self.attention.previous_object_id = self.attention.focused_object_id
                self.attention.focused_object_id = chosen
                self.attention.focus_since = self.tick
        self.last_percepts = list(percepts)

    def _update_exploration(self, position: tuple[float, float, float]) -> None:
        cell = f"{int(position[0] // 8)}:{int(position[2] // 8)}"
        self.exploration_visits[cell] = self.exploration_visits.get(cell, 0) + 1

    def inspect(self, object_id: str, revealed_attributes: dict[str, Any]) -> None:
        if object_id not in self.beliefs:
            return
        belief = self.beliefs[object_id]
        belief.attributes.update(revealed_attributes)
        belief.inspections += 1
        belief.confidence = clamp(belief.confidence + 0.2)

    def observe_player(self, obs: PlayerObservation) -> None:
        self.last_player_observation = obs
        self.player_model.last_interaction_tick = self.tick
        inferred = self._infer_player_desires(obs)
        self.mimic_history.append(MimicEpisode(self.tick, obs.action, obs.target_id, dict(inferred)))
        for desire, strength in inferred.items():
            old = self.player_model.inferred_desires.get(desire, 0.0)
            self.player_model.inferred_desires[desire] = clamp(_ema(old, strength, 0.45))

        action = obs.action.lower()
        if any(k in action for k in ("stroke", "reward", "feed", "heal", "play", "help")):
            self.player_model.affection = clamp(self.player_model.affection + 0.025)
            self.player_model.trust = clamp(self.player_model.trust + 0.02)
        if any(k in action for k in ("slap", "punish", "attack", "hurt")):
            self.player_model.fear = clamp(self.player_model.fear + 0.05)
            self.player_model.trust = clamp(self.player_model.trust - 0.04)

    def _infer_player_desires(self, obs: PlayerObservation) -> dict[Desire, float]:
        action = obs.action.lower()
        result: dict[Desire, float] = {}
        keyword_map = {
            Desire.HUNGER: ("feed", "eat", "food"),
            Desire.TO_PLAY: ("play", "ball", "toy"),
            Desire.BUILD_HOME: ("build", "house", "home"),
            Desire.RESTORE_HEALTH: ("heal", "cure"),
            Desire.ANGER: ("attack", "slap", "destroy"),
            Desire.COMPASSION: ("help", "heal", "rescue", "feed"),
            Desire.FEAR: ("flee", "run_away"),
            Desire.BRING_STUFF_HOME: ("bring", "carry", "storage"),
            Desire.BE_FRIENDS: ("friend", "stroke", "kiss"),
        }
        for desire, words in keyword_map.items():
            if any(w in action for w in words):
                result[desire] = max(result.get(desire, 0.0), 0.8)

        effects = obs.apparent_effects
        if effects.get("energy", 0.0) > 0:
            result[Desire.HUNGER] = max(result.get(Desire.HUNGER, 0.0), 0.9)
        if effects.get("health", 0.0) > 0:
            result[Desire.RESTORE_HEALTH] = max(result.get(Desire.RESTORE_HEALTH, 0.0), 0.9)
        if effects.get("hydration", 0.0) > 0:
            result[Desire.FOR_WATER] = max(result.get(Desire.FOR_WATER, 0.0), 0.9)
        return result
