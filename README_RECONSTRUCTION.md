# Creature Cognitive Core Reconstruction v0.1

This branch contains a runnable, standalone reconstruction of the cognitive organization recovered from Lionhead's *Black & White* Creature AI. It is a research implementation, not a claim of byte-identical source recovery.

## What v0.1 reconstructs

The engine includes the full recovered vocabulary of 40 Creature desires and 61 desire sources, source-driven continuous motivation, suppression/competition and dominant-motive selection, perception-limited object beliefs, generalized desire/action opinions represented by learned decision trees, object-specific learned opinions, explicit plans, prior action/context history, temporally distributed reward/punishment, observational player-goal inference, persistent attitude to the player, short interruption/resumption, and a separately serializable mind that can be transplanted onto a different body/species configuration.

The main loop is:

`PERCEPTION -> BELIEF UPDATE -> DESIRE SOURCES -> DESIRE DYNAMICS -> DOMINANT DESIRE -> ACTION/TARGET CANDIDATES -> LEARNED OPINIONS -> PLAN -> ACTION CONTEXT -> OUTCOME/FEEDBACK -> LEARNING`

This deliberately has no LLM dependency.

## Provenance discipline

Not every numerical rule in this version is historically recovered. The implementation uses four evidence classes:

- **Recovered from code:** the existence and organization of `CreatureMental`, desires, per-desire source lists, 40 desire identities, 61 source identities, growth/decay fields, suppression APIs, beliefs, desire/action decision-tree collections, action opinions, plans, previous action/context stacks, player-attitude/player-desire state, `SaveMind`, and creature-type-dependent desire timing.
- **Documented in primary sources:** epistemic verisimilitude, heterogeneous representation, reinforcement/teaching, observational learning, generalized opinions, and the design goal of a malleable autonomous creature.
- **Inferred reconstruction:** the exact numerical desire integrator, plan scoring weights, decision-tree induction algorithm, temporal-credit constants, commitment hysteresis, and precise player-goal inference rules. These are deliberately centralized and replaceable when exact decompilation becomes available.
- **Project extension:** JSON mind serialization and test-facing trace/fingerprint APIs. These exist to make experiments reproducible and are not attributed to Lionhead.

## Why action coverage is data-driven

The original game exposes hundreds of animation/gameplay actions. Reconstructing every animation-specific primitive would not improve the cognitive experiment. The core therefore provides a compact default action catalog and an extensible `ActionSpec` layer. New actions can be added without changing cognition.

## Quick start

```python
from creature_core import BodyState, CreatureCore, Percept, WorldFrame

creature = CreatureCore(seed=1)
food = Percept("apple", "food", {"edible": True}, salience=1.0)
trace = creature.step(WorldFrame(body=BodyState(energy=0.1), percepts=[food]))
print(trace.dominant_desire, trace.action, trace.target_id)
```

Run tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Validation target

This implementation is only successful if it reproduces the behavioral signatures of the original Creature. The repository's `tests/CREATURE_TEST_PROTOCOL.md` remains authoritative for comparison. v0.1 should therefore be treated as a Challenger against the original Black & White runtime, not as the new Champion by assumption.
