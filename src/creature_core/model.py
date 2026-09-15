from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .catalog import Desire, DesireSource


class Provenance(str, Enum):
    RECOVERED = "recovered_from_code"
    DOCUMENTED = "documented_primary_source"
    INFERRED = "inferred_reconstruction"
    PROJECT = "project_extension"


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if v < lo else hi if v > hi else v


@dataclass
class Percept:
    object_id: str
    kind: str
    attributes: dict[str, Any] = field(default_factory=dict)
    salience: float = 0.5
    position: tuple[float, float, float] | None = None


@dataclass
class PlayerObservation:
    action: str
    target_id: str | None = None
    target_kind: str | None = None
    apparent_effects: dict[str, float] = field(default_factory=dict)


@dataclass
class BodyState:
    energy: float = 1.0
    health: float = 1.0
    exhaustion: float = 0.0
    hydration: float = 1.0
    temperature: float = 0.5
    itch: float = 0.0
    illness: float = 0.0
    poo_load: float = 0.0
    nausea: float = 0.0
    recent_damage: float = 0.0
    sadness: float = 0.0
    loneliness: float = 0.0
    night: float = 0.0
    intoxication_opportunity: float = 0.0
    at_home: bool = False

    def normalize(self) -> None:
        for name in (
            "energy", "health", "exhaustion", "hydration", "temperature", "itch",
            "illness", "poo_load", "nausea", "recent_damage", "sadness", "loneliness",
            "night", "intoxication_opportunity",
        ):
            setattr(self, name, clamp(float(getattr(self, name))))


@dataclass
class Personality:
    niceness: float = 0.5
    aggression: float = 0.5
    playfulness: float = 0.5
    curiosity: float = 0.5
    laziness: float = 0.5
    friendliness: float = 0.5
    communicativeness: float = 0.5
    obedience: float = 0.5
    wanderlust: float = 0.5
    acquisitiveness: float = 0.2


@dataclass
class Belief:
    object_id: str
    kind: str
    attributes: dict[str, Any]
    first_seen: int
    last_seen: int
    confidence: float = 1.0
    inspections: int = 0
    object_opinions: dict[str, float] = field(default_factory=dict)


@dataclass
class DesireState:
    desire: Desire
    value: float = 0.0
    previous: float = 0.0
    baseline: float = 0.0
    growth_rate: float = 0.01
    decay: float = 0.01
    threshold: float = 0.1
    active: bool = True
    suppressed_until: int = 0
    source_values: dict[DesireSource, float] = field(default_factory=dict)


@dataclass
class Plan:
    desire: Desire
    action: str
    target_id: str | None
    score: float
    created_tick: int
    source: DesireSource | None = None
    interrupted: bool = False


@dataclass
class ContextRecord:
    tick: int
    desire: Desire
    desire_source: DesireSource | None
    action: str
    target_id: str | None
    features: dict[str, Any]
    predicted_utility: float
    outcome: float | None = None


@dataclass
class PlayerModel:
    inferred_desires: dict[Desire, float] = field(default_factory=dict)
    trust: float = 0.5
    affection: float = 0.5
    fear: float = 0.0
    respect: float = 0.5
    last_interaction_tick: int = -1


@dataclass
class AttentionState:
    focused_object_id: str | None = None
    focus_since: int = 0
    previous_object_id: str | None = None


@dataclass
class ExpressionState:
    valence: float = 0.0
    arousal: float = 0.0
    dominant_desire: Desire | None = None


@dataclass
class RelationState:
    object_id: str
    familiarity: float = 0.0
    affection: float = 0.5
    fear: float = 0.0
    last_seen: int = -1


@dataclass
class MimicEpisode:
    tick: int
    action: str
    target_id: str | None
    inferred_desires: dict[Desire, float]


@dataclass
class WorldFrame:
    body: BodyState = field(default_factory=BodyState)
    percepts: list[Percept] = field(default_factory=list)
    player_observation: PlayerObservation | None = None
    social: dict[str, float] = field(default_factory=dict)
    external_sources: dict[DesireSource, float] = field(default_factory=dict)
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class DecisionTrace:
    tick: int
    dominant_desire: Desire
    dominant_source: DesireSource | None
    desire_values: dict[str, float]
    action: str
    target_id: str | None
    plan_score: float
    candidates: list[tuple[str, str | None, float]]
    active_plan_reused: bool = False
    resumed_plan: bool = False


@dataclass
class LearningEpisode:
    features: dict[str, Any]
    reward: float
