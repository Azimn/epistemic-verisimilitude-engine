from __future__ import annotations

import math
import unittest
from collections import Counter

from creature_core import BodyState, CreatureCore, Desire, DesireSource, Percept, Personality, WorldFrame
from creature_core.catalog import DEFAULT_ACTIONS, SOURCE_TO_DESIRE


class BehavioralSignatureTests(unittest.TestCase):
    def test_recovered_vocabulary_is_complete(self):
        self.assertEqual(len(Desire), 40)
        self.assertEqual(len(DesireSource), 61)
        self.assertEqual(len(SOURCE_TO_DESIRE), 61)
        manifestable = {d for action in DEFAULT_ACTIONS for d in action.affinities}
        self.assertEqual(set(Desire), manifestable)

    def test_long_run_does_not_collapse_to_single_loop(self):
        c = CreatureCore(
            seed=42,
            personality=Personality(curiosity=.8, playfulness=.7, friendliness=.6, wanderlust=.7),
        )
        percepts = [
            Percept("apple", "food", {"edible": True, "ripe": True}, 1.0),
            Percept("pond", "water", {"drinkable": True}, .8),
            Percept("ball", "toy", {"round": True}, .9),
            Percept("villager", "villager", {}, .8),
            Percept("rock", "object", {"impressive": .2}, .6),
        ]
        actions: list[str] = []
        motives: list[str] = []
        for tick in range(250):
            phase = tick // 50
            if phase == 0:
                body = BodyState()
                social = {"unexplored": .9, "novelty": .8, "friend_opportunity": .1}
            elif phase == 1:
                body = BodyState(energy=.08)
                social = {"unexplored": .3, "novelty": .1, "friend_opportunity": .1}
            elif phase == 2:
                body = BodyState(hydration=.05)
                social = {"unexplored": .3, "novelty": .1, "friend_opportunity": .1}
            elif phase == 3:
                body = BodyState(exhaustion=.95, night=1.0)
                social = {"unexplored": .2, "novelty": .1, "friend_opportunity": .1}
            else:
                body = BodyState(loneliness=.8)
                social = {"unexplored": .2, "novelty": .1, "friend_opportunity": .9}
            trace = c.step(WorldFrame(
                body=body, percepts=percepts, social=social,
                position=(float(tick // 10) * 8.0, 0.0, 0.0),
            ))
            actions.append(trace.action)
            motives.append(trace.dominant_desire.name)
            c.complete_action(outcome=.2)
        counts = Counter(actions)
        total = len(actions)
        entropy = -sum((n / total) * math.log(n / total) for n in counts.values())
        entropy /= math.log(max(2, len(counts)))
        self.assertGreaterEqual(len(counts), 7)
        self.assertGreaterEqual(len(set(motives)), 9)
        self.assertGreater(entropy, .65)
        self.assertLess(max(counts.values()) / total, .55)

    def _train_target(self, rewarded_target: str) -> CreatureCore:
        c = CreatureCore(seed=17)
        a = Percept("ball-a", "toy", {"round": True, "color": "red"}, 1.0)
        b = Percept("ball-b", "toy", {"round": True, "color": "blue"}, 1.0)
        frame = WorldFrame(percepts=[a, b])
        for _ in range(70):
            c.desires[Desire.TO_PLAY].value = .98
            c._dominant_desire = Desire.TO_PLAY
            trace = c.step(frame)
            if trace.action == "play":
                c.feedback(1.0 if trace.target_id == rewarded_target else -.6, window=1)
            c.complete_action()
        return c

    def test_different_histories_produce_different_persistent_minds(self):
        a = self._train_target("ball-a")
        b = self._train_target("ball-b")
        self.assertGreater(a.beliefs["ball-a"].object_opinions["play"], a.beliefs["ball-b"].object_opinions.get("play", 0.0))
        self.assertGreater(b.beliefs["ball-b"].object_opinions.get("play", 0.0), b.beliefs["ball-a"].object_opinions.get("play", 0.0))
        self.assertNotEqual(a.beliefs["ball-a"].object_opinions, b.beliefs["ball-a"].object_opinions)

    def test_reinforcement_reversal_relearns_without_erasing_history_instantly(self):
        c = CreatureCore(seed=23)
        a = Percept("a", "toy", {"round": True}, 1.0)
        b = Percept("b", "toy", {"round": True}, 1.0)
        frame = WorldFrame(percepts=[a, b])

        def train(reward_target: str, rounds: int) -> None:
            for _ in range(rounds):
                c.desires[Desire.TO_PLAY].value = .98
                c._dominant_desire = Desire.TO_PLAY
                trace = c.step(frame)
                if trace.action == "play":
                    c.feedback(1.0 if trace.target_id == reward_target else -.7, window=1)
                c.complete_action()

        train("a", 80)
        a_before = c.beliefs["a"].object_opinions.get("play", 0.0)
        b_before = c.beliefs["b"].object_opinions.get("play", 0.0)
        self.assertGreater(a_before, b_before)
        train("b", 120)
        a_after = c.beliefs["a"].object_opinions.get("play", 0.0)
        b_after = c.beliefs["b"].object_opinions.get("play", 0.0)
        self.assertGreater(b_after, a_after)
        self.assertLess(a_after, a_before)

    def test_attention_prefers_salient_threat_and_exploration_records_place(self):
        c = CreatureCore(seed=19)
        c.step(WorldFrame(
            percepts=[
                Percept("pretty", "object", {}, 1.0),
                Percept("danger", "magic", {"scary_magic": 1.0}, .55),
            ],
            position=(17.0, 0.0, 25.0),
        ))
        self.assertEqual(c.attention.focused_object_id, "danger")
        self.assertEqual(c.exploration_visits.get("2:3"), 1)


if __name__ == "__main__":
    unittest.main()
