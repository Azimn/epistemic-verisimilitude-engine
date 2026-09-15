from __future__ import annotations

from typing import Any

from .catalog import ActionSpec, Desire
from .model import Belief, Plan


class PlanningMixin:
    def _matches(self, spec: ActionSpec, belief: Belief) -> bool:
        if spec.target_kinds and "*" not in spec.target_kinds and belief.kind not in spec.target_kinds:
            return False
        for key, expected in spec.required_attributes.items():
            if belief.attributes.get(key) != expected:
                return False
        return belief.confidence > 0.04

    def _features(self, desire: Desire, action: str, belief: Belief | None) -> dict[str, Any]:
        features: dict[str, Any] = {
            "desire": desire.name,
            "action": action,
            "development_stage": round(self.development_stage, 2),
            "player_trust": round(self.player_model.trust, 2),
            "player_fear": round(self.player_model.fear, 2),
        }
        if belief:
            features["target_kind"] = belief.kind
            features["belief_confidence"] = round(belief.confidence, 2)
            for key, value in sorted(belief.attributes.items()):
                if isinstance(value, (bool, int, float, str)):
                    features[f"target.{key}"] = value
        return features

    def _global_action_opinion(self, desire: Desire, action: str) -> float:
        return self.action_opinions.get((desire, action), 0.0)

    def _tree_opinion(self, desire: Desire, action: str, features: dict[str, Any]) -> float:
        tree = self.opinion_trees.get((desire, action))
        return tree.predict(features) if tree else 0.0

    def _candidate_score(self, desire: Desire, spec: ActionSpec, belief: Belief | None) -> float:
        state = self.desires[desire]
        affinity = float(spec.affinities.get(desire, 0.0))
        if desire == Desire.FOLLOW_PLAYER_DESIRE and self.player_model.inferred_desires:
            player_desire, strength = max(self.player_model.inferred_desires.items(), key=lambda kv: kv[1])
            if spec.name == "follow_player" and strength > 0.5:
                affinity *= 0.35
            affinity = max(affinity, float(spec.affinities.get(player_desire, 0.0)) * strength)
        if desire == Desire.TO_IMPRESS and self.last_player_observation and spec.name in self.last_player_observation.action.lower():
            affinity = max(affinity, 0.85)

        features = self._features(desire, spec.name, belief)
        global_opinion = self._global_action_opinion(desire, spec.name)
        generalized = self._tree_opinion(desire, spec.name, features)
        object_opinion = belief.object_opinions.get(spec.name, 0.0) if belief else 0.0
        repetition = list(self.previous_actions)[-8:].count(spec.name) / 8.0

        relation_bias = 0.0
        if belief and belief.object_id in self.relations:
            rel = self.relations[belief.object_id]
            if desire in (Desire.BE_FRIENDS, Desire.PLAY_WITH_PLAYER, Desire.EDUCATE_FRIEND):
                relation_bias = 0.12 * rel.affection + 0.06 * rel.familiarity - 0.15 * rel.fear
            elif desire in (Desire.FEAR, Desire.RUN_AWAY_FROM_PLAYER):
                relation_bias = 0.12 * rel.fear

        novelty = 0.0
        if belief and desire in (Desire.CURIOSITY, Desire.LOOK_AROUND):
            novelty = 1.0 - belief.confidence + min(0.25, 0.05 * max(0, 2 - belief.inspections))

        return (
            state.value * affinity
            + 0.36 * global_opinion
            + 0.52 * generalized
            + 0.30 * object_opinion
            + 0.18 * novelty
            + relation_bias
            - 0.10 * repetition
            - spec.cost
            + self.rng.uniform(-0.012, 0.012)
        )

    def _candidate_plans(self, desire: Desire) -> list[Plan]:
        candidates: list[Plan] = []
        source = self.dominant_source(desire)
        for spec in self.actions.values():
            if spec.name not in self.known_actions:
                continue
            has_affinity = desire in spec.affinities
            if desire == Desire.FOLLOW_PLAYER_DESIRE and self.player_model.inferred_desires:
                player_desire, strength = max(self.player_model.inferred_desires.items(), key=lambda kv: kv[1])
                has_affinity = has_affinity or (strength > 0.05 and player_desire in spec.affinities)
            if desire == Desire.TO_IMPRESS and self.last_player_observation:
                has_affinity = has_affinity or (spec.name in self.last_player_observation.action.lower())
            if not has_affinity:
                continue

            if not spec.target_kinds:
                candidates.append(Plan(desire, spec.name, None, self._candidate_score(desire, spec, None), self.tick, source))
                continue
            for belief in self.beliefs.values():
                if self._matches(spec, belief):
                    candidates.append(Plan(desire, spec.name, belief.object_id, self._candidate_score(desire, spec, belief), self.tick, source))
        return candidates

    def _can_keep_plan(self, plan: Plan, dominant: Desire) -> bool:
        if plan.desire != dominant:
            return False
        if plan.target_id is not None and plan.target_id not in self.beliefs:
            return False
        return self.tick - plan.created_tick <= 12

    def choose_plan(self, dominant: Desire) -> tuple[Plan, list[Plan], bool, bool]:
        if self.active_plan and self._can_keep_plan(self.active_plan, dominant):
            return self.active_plan, [self.active_plan], True, False

        if self.active_plan and self.active_plan.desire != dominant:
            old = self.active_plan
            old.interrupted = True
            self.suspended_plans.appendleft(old)
            self.active_plan = None

        for suspended in list(self.suspended_plans):
            if suspended.desire == dominant and self.tick - suspended.created_tick <= 30:
                self.suspended_plans.remove(suspended)
                suspended.interrupted = False
                suspended.score += 0.03
                self.active_plan = suspended
                return suspended, [suspended], False, True

        candidates = self._candidate_plans(dominant)
        if not candidates:
            fallback = Plan(
                dominant,
                "look_around",
                None,
                self.desires[dominant].value * 0.4,
                self.tick,
                self.dominant_source(dominant),
            )
            self.active_plan = fallback
            return fallback, [fallback], False, False

        candidates.sort(key=lambda p: p.score, reverse=True)
        self.active_plan = candidates[0]
        return self.active_plan, candidates, False, False
