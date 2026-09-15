from __future__ import annotations

import random
from collections import deque
from typing import Iterable

from .catalog import DEFAULT_ACTIONS, ActionSpec, Desire, DesireSource
from .learning import DecisionTreeOpinion
from .model import (
    AttentionState,
    Belief,
    ContextRecord,
    DecisionTrace,
    DesireState,
    ExpressionState,
    MimicEpisode,
    Personality,
    Plan,
    PlayerModel,
    RelationState,
    WorldFrame,
    clamp,
)
from .persistence import PersistenceMixin
from .runtime_learning import LearningMixin
from .runtime_motivation import MotivationMixin
from .runtime_perception import PerceptionMixin
from .runtime_planning import PlanningMixin


class CreatureCore(
    PerceptionMixin,
    MotivationMixin,
    PlanningMixin,
    LearningMixin,
    PersistenceMixin,
):
    """Standalone reconstruction candidate for the Black & White Creature core.

    The class reproduces the recovered cognitive organization, not the original
    executable: situated beliefs, continuous sourced desires, desire/action
    opinions, plans, context history, feedback learning, player modeling,
    attention/exploration state, and a separately serializable mind.
    """

    def __init__(
        self,
        *,
        seed: int = 1,
        personality: Personality | None = None,
        actions: Iterable[ActionSpec] = DEFAULT_ACTIONS,
        creature_type: str = "generic",
    ) -> None:
        self.rng = random.Random(seed)
        self.seed = seed
        self.tick = 0
        self.creature_type = creature_type
        self.personality = personality or Personality()
        self.actions = {a.name: a for a in actions}
        self.known_actions = {a.name for a in actions if a.known_by_default}

        self.beliefs: dict[str, Belief] = {}
        self.desires = {
            d: DesireState(
                desire=d,
                value=self.rng.uniform(0.0, 0.04),
                baseline=0.01 if d in (Desire.CURIOSITY, Desire.LOOK_AROUND) else 0.0,
                growth_rate=0.008,
                decay=0.018,
                threshold=0.06,
            )
            for d in Desire
        }
        self.source_weights = {s: 1.0 for s in DesireSource}

        self.action_opinions: dict[tuple[Desire, str], float] = {}
        self.opinion_trees: dict[tuple[Desire, str], DecisionTreeOpinion] = {}
        self.player_model = PlayerModel()

        self.active_plan: Plan | None = None
        self.suspended_plans: deque[Plan] = deque(maxlen=8)
        self.context_history: deque[ContextRecord] = deque(maxlen=320)
        self.previous_actions: deque[str] = deque(maxlen=64)

        self.last_player_observation = None
        self.last_percepts = []
        self.attention = AttentionState()
        self.expression = ExpressionState()
        self.exploration_visits: dict[str, int] = {}
        self.relations: dict[str, RelationState] = {}
        self.mimic_history: deque[MimicEpisode] = deque(maxlen=64)
        self.development_stage = 0.5
        self._dominant_desire = Desire.LOOK_AROUND

    def step(self, frame: WorldFrame) -> DecisionTrace:
        """Advance one cognitive cycle and return an inspectable decision trace."""
        self.tick += 1
        if frame.player_observation:
            self.observe_player(frame.player_observation)

        self._update_exploration(frame.position)
        self.perceive(frame.percepts)
        self.update_desires(frame)
        dominant = self.select_desire()

        positive = (
            self.desires[Desire.TO_PLAY].value
            + self.desires[Desire.BE_FRIENDS].value
            + self.desires[Desire.CURIOSITY].value
        )
        negative = (
            self.desires[Desire.FEAR].value
            + self.desires[Desire.ANGER].value
            + self.desires[Desire.SADNESS].value
        )
        self.expression.valence = max(-1.0, min(1.0, (positive - negative) / 3.0))
        self.expression.arousal = clamp(
            max(
                self.desires[Desire.FEAR].value,
                self.desires[Desire.ANGER].value,
                self.desires[Desire.CURIOSITY].value,
            )
        )
        self.expression.dominant_desire = dominant

        plan, candidates, reused, resumed = self.choose_plan(dominant)
        belief = self.beliefs.get(plan.target_id) if plan.target_id else None
        features = self._features(plan.desire, plan.action, belief)
        self.context_history.append(
            ContextRecord(
                tick=self.tick,
                desire=plan.desire,
                desire_source=plan.source,
                action=plan.action,
                target_id=plan.target_id,
                features=features,
                predicted_utility=plan.score,
            )
        )
        self.previous_actions.append(plan.action)

        return DecisionTrace(
            tick=self.tick,
            dominant_desire=dominant,
            dominant_source=plan.source,
            desire_values={d.name: round(s.value, 6) for d, s in self.desires.items()},
            action=plan.action,
            target_id=plan.target_id,
            plan_score=plan.score,
            candidates=[(p.action, p.target_id, p.score) for p in candidates[:20]],
            active_plan_reused=reused,
            resumed_plan=resumed,
        )
