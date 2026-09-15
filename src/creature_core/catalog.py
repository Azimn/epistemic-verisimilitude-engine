from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Mapping


class Desire(IntEnum):
    TO_IMPRESS = 0
    COMPASSION = 1
    ANGER = 2
    TO_PLAY = 3
    HUNGER = 4
    FEAR = 5
    CURIOSITY = 6
    TO_POO = 7
    TIREDNESS = 8
    IDLE_WITH_PLAYER = 9
    WANDERLUST = 10
    TO_PUKE = 11
    BUILD_HOME = 12
    BRING_STUFF_HOME = 13
    FOR_WATER = 14
    RESTORE_HEALTH = 15
    BE_FRIENDS = 16
    ATTRACT_PLAYER_ATTENTION = 17
    MANIFEST_STATE = 18
    GET_WARMER = 19
    GET_COLDER = 20
    TO_SCRATCH = 21
    RUN_AWAY_FROM_PLAYER = 22
    TO_REST = 23
    OBEY_PLAYER = 24
    ILLNESS = 25
    OBEY_CREATURE = 26
    SADNESS = 27
    STAY_NEAR_HOME = 28
    GO_HOME = 28  # compatibility alias; original enum name is STAY_NEAR_HOME
    TELL_PLAYER_OPINION = 29
    PLAY_WITH_PLAYER = 30
    TELL_CREATURE_OPINION = 31
    EDUCATE_FRIEND = 32
    FOLLOW_PLAYER_DESIRE = 33
    GET_HIGH = 34
    HANG_AROUND_HOME = 35
    MENTAL_ILLNESS = 36
    MISS_FRIEND = 37
    LOOK_AROUND = 38
    STEAL = 39


class DesireSource(IntEnum):
    IMPRESS_FROM_WATCHING_PLAYER = 0
    IMPRESS_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT = 1
    COMPASSION_FROM_WATCHING_PLAYER = 2
    COMPASSION_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT = 3
    COMPASSION_FROM_BEING_CONTENT = 4
    COMPASSION_INNATE_NICENESS = 5
    ANGER_FROM_WATCHING_PLAYER = 6
    ANGER_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT = 7
    ANGER_FROM_BEING_DISSATISFIED = 8
    ANGER_FROM_BEING_DAMAGED = 9
    ANGER_FROM_SADNESS = 10
    ANGER_INNATE_AGGRESSION = 11
    TO_PLAY_FROM_WATCHING_PLAYER = 12
    TO_PLAY_FROM_WATCHING_VILLAGERS = 13
    HUNGER_FROM_ENERGY = 14
    HUNGER_FROM_WATCHING_VILLAGERS = 15
    HUNGER_FROM_SADNESS = 16
    FEAR_FROM_DARKNESS = 17
    FEAR_FROM_BEING_DAMAGED = 18
    FEAR_FROM_SEEING_SCAREY_MAGIC = 19
    CURIOSITY = 20
    TO_POO_FROM_PHYSICAL_POO = 21
    TIREDNESS_FROM_EXHAUSTION = 22
    TIREDNESS_FROM_LAZINESS = 23
    TIREDNESS_FROM_NIGHT_TIME = 24
    TIREDNESS_FROM_SADNESS = 25
    TIREDNESS_INNATE_LETHARGY = 26
    TO_IDLE_AROUND_WITH_PLAYER = 27
    WANDERLUST = 28
    TO_PUKE = 29
    TO_BUILD_HOME = 30
    TO_BRING_STUFF_HOME = 31
    FOR_WATER_FROM_DEHYDRATION = 32
    TO_RESTORE_HEALTH_FROM_LIFE = 33
    TO_BE_FRIENDS = 34
    TO_BE_FRIENDS_INNATE_FRIENDLINESS = 35
    TO_ATTRACT_PLAYERS_ATTENTION_FROM_LONELINESS = 36
    TO_ATTRACT_PLAYERS_ATTENTION_FROM_LACK_OF_INTERACTION = 37
    TO_MANIFEST_STATE = 38
    TO_MANIFEST_STATE_INNATE_COMMUNICATIVENESS = 39
    TO_GET_WARMER = 40
    TO_GET_COLDER = 41
    TO_SCRATCH = 42
    TO_RUN_AWAY_FROM_PLAYER = 43
    TO_REST = 44
    TO_OBEY_PLAYER = 45
    ILLNESS = 46
    TO_OBEY_CREATURE = 47
    SADNESS = 48
    TO_GO_HOME = 49
    TO_TELL_PLAYER_WHAT_YOU_THINK_OF_HIM = 50
    TO_PLAY_WITH_PLAYER = 51
    TO_TELL_CREATURE_WHAT_YOU_THINK_OF_HIM = 52
    TO_EDUCATE_FRIEND = 53
    TO_FOLLOW_PLAYER_DESIRE = 54
    TO_GET_HIGH = 55
    TO_HANG_AROUND_AT_HOME = 56
    SOURCE_FOR_MENTAL_ILLNESS = 57
    TO_MISS_FRIEND = 58
    TO_LOOK_AROUND = 59
    TO_STEAL = 60


SOURCE_TO_DESIRE: dict[DesireSource, Desire] = {
    DesireSource.IMPRESS_FROM_WATCHING_PLAYER: Desire.TO_IMPRESS,
    DesireSource.IMPRESS_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT: Desire.TO_IMPRESS,
    DesireSource.COMPASSION_FROM_WATCHING_PLAYER: Desire.COMPASSION,
    DesireSource.COMPASSION_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT: Desire.COMPASSION,
    DesireSource.COMPASSION_FROM_BEING_CONTENT: Desire.COMPASSION,
    DesireSource.COMPASSION_INNATE_NICENESS: Desire.COMPASSION,
    DesireSource.ANGER_FROM_WATCHING_PLAYER: Desire.ANGER,
    DesireSource.ANGER_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT: Desire.ANGER,
    DesireSource.ANGER_FROM_BEING_DISSATISFIED: Desire.ANGER,
    DesireSource.ANGER_FROM_BEING_DAMAGED: Desire.ANGER,
    DesireSource.ANGER_FROM_SADNESS: Desire.ANGER,
    DesireSource.ANGER_INNATE_AGGRESSION: Desire.ANGER,
    DesireSource.TO_PLAY_FROM_WATCHING_PLAYER: Desire.TO_PLAY,
    DesireSource.TO_PLAY_FROM_WATCHING_VILLAGERS: Desire.TO_PLAY,
    DesireSource.HUNGER_FROM_ENERGY: Desire.HUNGER,
    DesireSource.HUNGER_FROM_WATCHING_VILLAGERS: Desire.HUNGER,
    DesireSource.HUNGER_FROM_SADNESS: Desire.HUNGER,
    DesireSource.FEAR_FROM_DARKNESS: Desire.FEAR,
    DesireSource.FEAR_FROM_BEING_DAMAGED: Desire.FEAR,
    DesireSource.FEAR_FROM_SEEING_SCAREY_MAGIC: Desire.FEAR,
    DesireSource.CURIOSITY: Desire.CURIOSITY,
    DesireSource.TO_POO_FROM_PHYSICAL_POO: Desire.TO_POO,
    DesireSource.TIREDNESS_FROM_EXHAUSTION: Desire.TIREDNESS,
    DesireSource.TIREDNESS_FROM_LAZINESS: Desire.TIREDNESS,
    DesireSource.TIREDNESS_FROM_NIGHT_TIME: Desire.TIREDNESS,
    DesireSource.TIREDNESS_FROM_SADNESS: Desire.TIREDNESS,
    DesireSource.TIREDNESS_INNATE_LETHARGY: Desire.TIREDNESS,
    DesireSource.TO_IDLE_AROUND_WITH_PLAYER: Desire.IDLE_WITH_PLAYER,
    DesireSource.WANDERLUST: Desire.WANDERLUST,
    DesireSource.TO_PUKE: Desire.TO_PUKE,
    DesireSource.TO_BUILD_HOME: Desire.BUILD_HOME,
    DesireSource.TO_BRING_STUFF_HOME: Desire.BRING_STUFF_HOME,
    DesireSource.FOR_WATER_FROM_DEHYDRATION: Desire.FOR_WATER,
    DesireSource.TO_RESTORE_HEALTH_FROM_LIFE: Desire.RESTORE_HEALTH,
    DesireSource.TO_BE_FRIENDS: Desire.BE_FRIENDS,
    DesireSource.TO_BE_FRIENDS_INNATE_FRIENDLINESS: Desire.BE_FRIENDS,
    DesireSource.TO_ATTRACT_PLAYERS_ATTENTION_FROM_LONELINESS: Desire.ATTRACT_PLAYER_ATTENTION,
    DesireSource.TO_ATTRACT_PLAYERS_ATTENTION_FROM_LACK_OF_INTERACTION: Desire.ATTRACT_PLAYER_ATTENTION,
    DesireSource.TO_MANIFEST_STATE: Desire.MANIFEST_STATE,
    DesireSource.TO_MANIFEST_STATE_INNATE_COMMUNICATIVENESS: Desire.MANIFEST_STATE,
    DesireSource.TO_GET_WARMER: Desire.GET_WARMER,
    DesireSource.TO_GET_COLDER: Desire.GET_COLDER,
    DesireSource.TO_SCRATCH: Desire.TO_SCRATCH,
    DesireSource.TO_RUN_AWAY_FROM_PLAYER: Desire.RUN_AWAY_FROM_PLAYER,
    DesireSource.TO_REST: Desire.TO_REST,
    DesireSource.TO_OBEY_PLAYER: Desire.OBEY_PLAYER,
    DesireSource.ILLNESS: Desire.ILLNESS,
    DesireSource.TO_OBEY_CREATURE: Desire.OBEY_CREATURE,
    DesireSource.SADNESS: Desire.SADNESS,
    DesireSource.TO_GO_HOME: Desire.STAY_NEAR_HOME,
    DesireSource.TO_TELL_PLAYER_WHAT_YOU_THINK_OF_HIM: Desire.TELL_PLAYER_OPINION,
    DesireSource.TO_PLAY_WITH_PLAYER: Desire.PLAY_WITH_PLAYER,
    DesireSource.TO_TELL_CREATURE_WHAT_YOU_THINK_OF_HIM: Desire.TELL_CREATURE_OPINION,
    DesireSource.TO_EDUCATE_FRIEND: Desire.EDUCATE_FRIEND,
    DesireSource.TO_FOLLOW_PLAYER_DESIRE: Desire.FOLLOW_PLAYER_DESIRE,
    DesireSource.TO_GET_HIGH: Desire.GET_HIGH,
    DesireSource.TO_HANG_AROUND_AT_HOME: Desire.HANG_AROUND_HOME,
    DesireSource.SOURCE_FOR_MENTAL_ILLNESS: Desire.MENTAL_ILLNESS,
    DesireSource.TO_MISS_FRIEND: Desire.MISS_FRIEND,
    DesireSource.TO_LOOK_AROUND: Desire.LOOK_AROUND,
    DesireSource.TO_STEAL: Desire.STEAL,
}


@dataclass(frozen=True)
class ActionSpec:
    name: str
    affinities: Mapping[Desire, float]
    target_kinds: frozenset[str] = frozenset()
    required_attributes: Mapping[str, object] = field(default_factory=dict)
    known_by_default: bool = True
    cost: float = 0.0


DEFAULT_ACTIONS: tuple[ActionSpec, ...] = (
    ActionSpec("show_off", {Desire.TO_IMPRESS: 1.0}),
    ActionSpec("inspect", {Desire.CURIOSITY: 1.0, Desire.LOOK_AROUND: 0.7}, frozenset({"*"})),
    ActionSpec("look_around", {Desire.CURIOSITY: 0.65, Desire.LOOK_AROUND: 1.0, Desire.WANDERLUST: 0.35}),
    ActionSpec("eat", {Desire.HUNGER: 1.0}, frozenset({"food", "animal", "villager"}), {"edible": True}),
    ActionSpec("drink", {Desire.FOR_WATER: 1.0}, frozenset({"water", "sea"}), {"drinkable": True}),
    ActionSpec("sleep", {Desire.TIREDNESS: 0.9, Desire.TO_REST: 1.0, Desire.RESTORE_HEALTH: 0.25}),
    ActionSpec("flee", {Desire.FEAR: 1.0, Desire.RUN_AWAY_FROM_PLAYER: 1.0}, frozenset({"threat", "player", "magic", "creature", "villager"})),
    ActionSpec("attack", {Desire.ANGER: 1.0}, frozenset({"threat", "creature", "villager", "object"})),
    ActionSpec("play", {Desire.TO_PLAY: 1.0, Desire.PLAY_WITH_PLAYER: 0.85}, frozenset({"toy", "player", "creature", "ball"})),
    ActionSpec("follow_player", {Desire.IDLE_WITH_PLAYER: 0.5, Desire.OBEY_PLAYER: 0.8, Desire.FOLLOW_PLAYER_DESIRE: 0.9}),
    ActionSpec("communicate_state", {Desire.MANIFEST_STATE: 1.0, Desire.ATTRACT_PLAYER_ATTENTION: 0.7, Desire.TELL_PLAYER_OPINION: 0.8}),
    ActionSpec("befriend", {Desire.BE_FRIENDS: 1.0}, frozenset({"creature", "villager", "player"})),
    ActionSpec("help", {Desire.COMPASSION: 1.0}, frozenset({"villager", "creature", "object"}), {"needs_help": True}),
    ActionSpec("build_home", {Desire.BUILD_HOME: 1.0}),
    ActionSpec("bring_home", {Desire.BRING_STUFF_HOME: 1.0}, frozenset({"object", "food", "wood", "rock", "toy"})),
    ActionSpec("go_home", {Desire.STAY_NEAR_HOME: 1.0, Desire.HANG_AROUND_HOME: 0.7}),
    ActionSpec("heal_self", {Desire.RESTORE_HEALTH: 1.0, Desire.ILLNESS: 0.7}),
    ActionSpec("seek_warmth", {Desire.GET_WARMER: 1.0}, frozenset({"fire", "home", "warm_place", "object"})),
    ActionSpec("seek_cool", {Desire.GET_COLDER: 1.0}, frozenset({"water", "shade", "cool_place", "object"})),
    ActionSpec("scratch", {Desire.TO_SCRATCH: 1.0}),
    ActionSpec("poo", {Desire.TO_POO: 1.0}),
    ActionSpec("puke", {Desire.TO_PUKE: 1.0}),
    ActionSpec("steal", {Desire.STEAL: 1.0}, frozenset({"object", "food", "toy"})),
    ActionSpec("idle_with_player", {Desire.IDLE_WITH_PLAYER: 1.0, Desire.ATTRACT_PLAYER_ATTENTION: 0.4, Desire.SADNESS: 0.35}),
    ActionSpec("obey_creature", {Desire.OBEY_CREATURE: 1.0}, frozenset({"creature"})),
    ActionSpec("seek_comfort", {Desire.SADNESS: 1.0}, frozenset({"player", "creature", "home"})),
    ActionSpec("educate_friend", {Desire.EDUCATE_FRIEND: 1.0}, frozenset({"creature"})),
    ActionSpec("tell_creature_opinion", {Desire.TELL_CREATURE_OPINION: 1.0}, frozenset({"creature"})),
    ActionSpec("consume_intoxicant", {Desire.GET_HIGH: 1.0}, frozenset({"intoxicant", "object"}), {"intoxicating": True}),
    ActionSpec("act_confused", {Desire.MENTAL_ILLNESS: 1.0, Desire.MANIFEST_STATE: 0.2}),
    ActionSpec("seek_friend", {Desire.MISS_FRIEND: 1.0}, frozenset({"creature", "player"})),
    ActionSpec("wander", {Desire.WANDERLUST: 1.0, Desire.LOOK_AROUND: 0.45}),
)

ACTION_BY_NAME = {a.name: a for a in DEFAULT_ACTIONS}
