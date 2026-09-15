from __future__ import annotations

from .learning import DecisionTreeOpinion
from .model import clamp


def _ema(old: float, new: float, alpha: float) -> float:
    return old + alpha * (new - old)


def _signed_clamp(value: float) -> float:
    return max(-1.0, min(1.0, value))


class LearningMixin:
    def complete_action(self, outcome: float = 0.0, *, satisfied: bool | None = None) -> None:
        if self.context_history:
            self.context_history[-1].outcome = float(outcome)
        if not self.active_plan:
            return

        plan = self.active_plan
        if satisfied is None:
            spec = self.actions.get(plan.action)
            satisfied = bool(spec and float(spec.affinities.get(plan.desire, 0.0)) >= 0.75)
        if satisfied:
            state = self.desires[plan.desire]
            state.value *= 0.30
            state.suppressed_until = max(state.suppressed_until, self.tick + 2)
            if plan.source is not None:
                state.source_values[plan.source] = 0.0
        self.active_plan = None

    def feedback(self, value: float, *, window: int = 8, decay: float = 0.68) -> None:
        value = _signed_clamp(float(value))
        recent = list(self.context_history)[-window:]
        for lag, ctx in enumerate(reversed(recent)):
            credit = value * (decay ** lag)
            key = (ctx.desire, ctx.action)
            old = self.action_opinions.get(key, 0.0)
            self.action_opinions[key] = _signed_clamp(_ema(old, credit, 0.24))
            tree = self.opinion_trees.setdefault(key, DecisionTreeOpinion())
            tree.add(ctx.features, credit)

            if ctx.target_id and ctx.target_id in self.beliefs:
                belief = self.beliefs[ctx.target_id]
                old_obj = belief.object_opinions.get(ctx.action, 0.0)
                belief.object_opinions[ctx.action] = _signed_clamp(_ema(old_obj, credit, 0.30))
                if ctx.target_id in self.relations:
                    rel = self.relations[ctx.target_id]
                    rel.affection = clamp(rel.affection + 0.025 * credit)
                    if credit < 0:
                        rel.fear = clamp(rel.fear + 0.02 * abs(credit))

            if ctx.desire_source is not None:
                old_weight = self.source_weights[ctx.desire_source]
                self.source_weights[ctx.desire_source] = max(0.2, min(2.0, old_weight + 0.04 * credit))

        if value > 0:
            self.player_model.trust = clamp(self.player_model.trust + 0.015 * value)
            self.player_model.affection = clamp(self.player_model.affection + 0.02 * value)
        elif value < 0:
            self.player_model.fear = clamp(self.player_model.fear + 0.02 * abs(value))
            self.player_model.trust = clamp(self.player_model.trust - 0.015 * abs(value))

    def teach_action(self, action: str, known: bool = True) -> None:
        if known:
            self.known_actions.add(action)
        else:
            self.known_actions.discard(action)
