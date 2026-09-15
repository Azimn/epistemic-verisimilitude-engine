from __future__ import annotations

import math

from .catalog import SOURCE_TO_DESIRE, Desire, DesireSource
from .model import WorldFrame, clamp


class MotivationMixin:
    def _source_values(self, frame: WorldFrame) -> dict[DesireSource, float]:
        b = frame.body
        b.normalize()
        p = self.personality
        social = frame.social
        since_player = self.tick - self.player_model.last_interaction_tick if self.player_model.last_interaction_tick >= 0 else 999
        visible = [self.beliefs[p.object_id] for p in frame.percepts if p.object_id in self.beliefs]
        danger = max([float(x.attributes.get("threat", 0.0)) for x in visible] + [0.0])
        scary_magic = max([float(x.attributes.get("scary_magic", 0.0)) for x in visible] + [0.0])
        needs_help = max([float(bool(x.attributes.get("needs_help", False))) for x in visible] + [0.0])
        impressive = max([float(x.attributes.get("impressive", 0.0)) for x in visible] + [0.0])
        hostile = max([float(x.attributes.get("hostile", 0.0)) for x in visible] + [0.0])
        novelty = 0.0
        if frame.percepts:
            novelty = sum(1.0 - self.beliefs[x.object_id].confidence for x in frame.percepts if x.object_id in self.beliefs) / len(frame.percepts)
        cell = f"{int(frame.position[0] // 8)}:{int(frame.position[2] // 8)}"
        spatial_novelty = 1.0 / (1.0 + self.exploration_visits.get(cell, 0))
        observed = self.last_player_observation.action.lower() if self.last_player_observation else ""
        watched = lambda *words: 1.0 if any(w in observed for w in words) else 0.0
        content = clamp((b.energy + b.health + b.hydration + (1.0 - b.exhaustion) + (1.0 - b.sadness)) / 5.0)
        dissatisfied = 1.0 - content

        v: dict[DesireSource, float] = {
            DesireSource.IMPRESS_FROM_WATCHING_PLAYER: watched("impress", "magic", "show"),
            DesireSource.IMPRESS_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT: impressive,
            DesireSource.COMPASSION_FROM_WATCHING_PLAYER: watched("help", "heal", "feed", "rescue"),
            DesireSource.COMPASSION_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT: needs_help,
            DesireSource.COMPASSION_FROM_BEING_CONTENT: content * 0.4,
            DesireSource.COMPASSION_INNATE_NICENESS: p.niceness * 0.25,
            DesireSource.ANGER_FROM_WATCHING_PLAYER: watched("attack", "slap", "destroy"),
            DesireSource.ANGER_FROM_SEEING_OBJECTS_WHICH_DESERVE_IT: max(hostile, danger),
            DesireSource.ANGER_FROM_BEING_DISSATISFIED: dissatisfied,
            DesireSource.ANGER_FROM_BEING_DAMAGED: b.recent_damage,
            DesireSource.ANGER_FROM_SADNESS: b.sadness,
            DesireSource.ANGER_INNATE_AGGRESSION: p.aggression * 0.25,
            DesireSource.TO_PLAY_FROM_WATCHING_PLAYER: watched("play", "ball", "toy"),
            DesireSource.TO_PLAY_FROM_WATCHING_VILLAGERS: clamp(social.get("villagers_playing", 0.0)),
            DesireSource.HUNGER_FROM_ENERGY: 1.0 - b.energy,
            DesireSource.HUNGER_FROM_WATCHING_VILLAGERS: clamp(social.get("villagers_eating", 0.0)),
            DesireSource.HUNGER_FROM_SADNESS: b.sadness * 0.25,
            DesireSource.FEAR_FROM_DARKNESS: b.night * 0.4,
            DesireSource.FEAR_FROM_BEING_DAMAGED: b.recent_damage,
            DesireSource.FEAR_FROM_SEEING_SCAREY_MAGIC: scary_magic,
            DesireSource.CURIOSITY: clamp(0.25 * p.curiosity + 0.50 * max(novelty, social.get("novelty", 0.0)) + 0.25 * spatial_novelty),
            DesireSource.TO_POO_FROM_PHYSICAL_POO: b.poo_load,
            DesireSource.TIREDNESS_FROM_EXHAUSTION: b.exhaustion,
            DesireSource.TIREDNESS_FROM_LAZINESS: p.laziness * 0.45,
            DesireSource.TIREDNESS_FROM_NIGHT_TIME: b.night * 0.6,
            DesireSource.TIREDNESS_FROM_SADNESS: b.sadness * 0.35,
            DesireSource.TIREDNESS_INNATE_LETHARGY: p.laziness * 0.25,
            DesireSource.TO_IDLE_AROUND_WITH_PLAYER: clamp(1.0 - since_player / 100.0) * self.player_model.affection,
            DesireSource.WANDERLUST: clamp(p.wanderlust * (0.25 + 0.35 * social.get("unexplored", 0.5) + 0.40 * spatial_novelty)),
            DesireSource.TO_PUKE: b.nausea,
            DesireSource.TO_BUILD_HOME: clamp(social.get("needs_home", 0.0)),
            DesireSource.TO_BRING_STUFF_HOME: clamp(social.get("home_needs_resources", 0.0)),
            DesireSource.FOR_WATER_FROM_DEHYDRATION: 1.0 - b.hydration,
            DesireSource.TO_RESTORE_HEALTH_FROM_LIFE: 1.0 - b.health,
            DesireSource.TO_BE_FRIENDS: clamp(social.get("friend_opportunity", 0.0)),
            DesireSource.TO_BE_FRIENDS_INNATE_FRIENDLINESS: p.friendliness * 0.25,
            DesireSource.TO_ATTRACT_PLAYERS_ATTENTION_FROM_LONELINESS: b.loneliness,
            DesireSource.TO_ATTRACT_PLAYERS_ATTENTION_FROM_LACK_OF_INTERACTION: (clamp(since_player / 100.0) if self.player_model.last_interaction_tick >= 0 else 0.0),
            DesireSource.TO_MANIFEST_STATE: clamp(max(b.sadness, 1.0 - b.energy, b.exhaustion, 1.0 - b.health, 1.0 - b.hydration)),
            DesireSource.TO_MANIFEST_STATE_INNATE_COMMUNICATIVENESS: p.communicativeness * 0.25,
            DesireSource.TO_GET_WARMER: clamp((0.42 - b.temperature) / 0.42),
            DesireSource.TO_GET_COLDER: clamp((b.temperature - 0.58) / 0.42),
            DesireSource.TO_SCRATCH: b.itch,
            DesireSource.TO_RUN_AWAY_FROM_PLAYER: clamp(self.player_model.fear - self.player_model.trust * 0.3),
            DesireSource.TO_REST: clamp(max(b.exhaustion, 1.0 - b.health) * 0.75),
            DesireSource.TO_OBEY_PLAYER: clamp(p.obedience * self.player_model.respect),
            DesireSource.ILLNESS: b.illness,
            DesireSource.TO_OBEY_CREATURE: clamp(social.get("dominant_creature_command", 0.0)),
            DesireSource.SADNESS: b.sadness,
            DesireSource.TO_GO_HOME: clamp((not b.at_home) * social.get("home_pull", 0.0)),
            DesireSource.TO_TELL_PLAYER_WHAT_YOU_THINK_OF_HIM: clamp(abs(self.player_model.affection - 0.5) * 2.0),
            DesireSource.TO_PLAY_WITH_PLAYER: clamp(p.playfulness * self.player_model.affection * (1.0 - min(1.0, since_player / 50.0))),
            DesireSource.TO_TELL_CREATURE_WHAT_YOU_THINK_OF_HIM: clamp(social.get("opinion_of_creature_strength", 0.0)),
            DesireSource.TO_EDUCATE_FRIEND: clamp(social.get("friend_needs_teaching", 0.0)),
            DesireSource.TO_FOLLOW_PLAYER_DESIRE: max(self.player_model.inferred_desires.values(), default=0.0),
            DesireSource.TO_GET_HIGH: b.intoxication_opportunity,
            DesireSource.TO_HANG_AROUND_AT_HOME: 1.0 if b.at_home else 0.0,
            DesireSource.SOURCE_FOR_MENTAL_ILLNESS: clamp(social.get("mental_illness", 0.0)),
            DesireSource.TO_MISS_FRIEND: clamp(social.get("friend_absence", 0.0)),
            DesireSource.TO_LOOK_AROUND: clamp(0.25 + 0.5 * p.curiosity + 0.25 * social.get("novelty", 0.0)),
            DesireSource.TO_STEAL: clamp(p.acquisitiveness * social.get("unguarded_valuable", 0.0)),
        }
        for source, value in frame.external_sources.items():
            v[source] = clamp(value)
        return v

    def update_desires(self, frame: WorldFrame, dt: float = 1.0) -> None:
        sources = self._source_values(frame)
        grouped: dict[Desire, list[tuple[DesireSource, float]]] = {d: [] for d in Desire}
        for source, raw in sources.items():
            grouped[SOURCE_TO_DESIRE[source]].append((source, clamp(raw) * self.source_weights[source]))
        for desire, state in self.desires.items():
            state.previous = state.value
            state.source_values = {s: clamp(v) for s, v in grouped[desire]}
            source_drive = 0.0
            if grouped[desire]:
                vals = [clamp(v) for _, v in grouped[desire]]
                source_drive = 1.0 - math.prod(1.0 - x for x in vals)
            target = clamp(state.baseline + source_drive)
            # Recovered: growth/decay/source state and continuous updates.
            # Inferred: exact numerical integration until the original function is matched.
            growth = state.growth_rate * (1.0 - state.value)
            relaxation = 0.32 * (target - state.value)
            decay = state.decay * state.value if target < state.value else 0.0
            state.value = clamp(state.value + dt * (growth + relaxation - decay))

    def dominant_source(self, desire: Desire) -> DesireSource | None:
        values = self.desires[desire].source_values
        return max(values, key=values.get) if values else None

    def select_desire(self) -> Desire:
        scored: list[tuple[float, Desire]] = []
        for desire, state in self.desires.items():
            if not state.active or self.tick < state.suppressed_until:
                continue
            scored.append((state.value, desire))
        scored.sort(reverse=True, key=lambda x: (x[0], -int(x[1])))
        winner = scored[0][1] if scored else Desire.LOOK_AROUND
        current = self._dominant_desire
        if current in self.desires and self.desires[current].active:
            cur = self.desires[current].value
            best = self.desires[winner].value
            if cur >= self.desires[current].threshold and best - cur < 0.10:
                winner = current
        self._dominant_desire = winner
        return winner
