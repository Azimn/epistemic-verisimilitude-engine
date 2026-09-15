# Creature Cognitive Core v0.1: Reconstruction Status

Status: runnable Challenger, not yet validated against the original runtime.

## Scope

This implementation reconstructs the cognitive core exposed by the surviving Black & White code, symbols, headers, historical descriptions, and CreatureMind behavior. It deliberately excludes rendering, animation, navigation mesh/pathfinding, game-specific spell execution, village simulation, and the hundreds of concrete action primitives that belong to the game layer rather than the cognitive architecture.

## Recovered architecture coverage

| Recovered Black & White subsystem | v0.1 reconstruction | Fidelity status |
| --- | --- | --- |
| `CreatureDesires` | 40 recovered desires, 61 recovered source identities, per-source values, continuous update, activation, suppression, dominant motive | Structurally faithful; numerical integrator inferred |
| `CreatureMentalBeliefs` | Explicit object-specific beliefs created only from percepts, confidence/recency, inspections, object-specific action opinions | Structurally faithful; belief decay coefficient inferred |
| `DecisionTreeCollection` / `AttributeTest` | Desire/action-specific online regression trees trained from retained contextual episodes | Representationally faithful; tree-induction algorithm inferred |
| `CreatureActionOpinions` | Learned global desire/action preference values | Functional reconstruction; exact original representation unresolved |
| `CreatureAgenda` / `CreaturePlanState` | Explicit motive/action/target plans, plan competition, short commitment hysteresis, interruption and resumption | Structurally faithful; scoring/hysteresis inferred |
| `CreatureLearning` / previous contexts | Bounded action/context history and temporally decayed credit assignment | Structurally faithful; exact credit-assignment constants inferred |
| `CreatureAttitudeToPlayer` | Persistent trust, affection, fear, respect and inferred player desires | Functional reconstruction; exact original fields/update equations unresolved |
| `CreatureMimicState` | Player demonstrations retained with inferred goals; inferred goal can generate nonliteral goal-equivalent behavior | Functional reconstruction consistent with primary descriptions |
| `CreatureVisionState` / `CreatureLookState` | Percept-only input plus salience/novelty/threat attention with focus persistence | Functional reconstruction |
| `CreatureExplorationMap` | Spatial visit map feeding curiosity/wanderlust | Functional reconstruction; original map encoding unresolved |
| `CreatureObjectsInspected` | Inspection count and revealed attributes on beliefs | Functional reconstruction |
| `CreaturePreviousActions` | Bounded previous-action history used for repetition pressure and learning | Structurally faithful |
| `CreatureInnatePersonality` | Niceness, aggression, playfulness, curiosity, laziness, friendliness, communicativeness, obedience, wanderlust, acquisitiveness | Semantics inferred from recovered desire-source names and historical behavior |
| `CreatureFaceState` | Derived valence/arousal/dominant-motive expression state | Functional placeholder until exact face-state update paths are recovered |
| `CreatureMental::SaveMind` | Mind-only JSON persistence, separate from supplied body state/species | Experimental analogue, not original `.erc` format |
| Action knowledge | Per-action known/unknown state and teaching API | Structurally faithful to recovered script hooks |

## Recovered vocabulary

The exact desire indices are preserved from the original enum, including `TO_IMPRESS=0` through `TO_STEAL=39`. `STAY_NEAR_HOME=28` is preserved as the historical name, with `GO_HOME` retained only as a compatibility alias. All 61 recovered `CREATURE_DESIRE_SOURCE` entries are also represented and mapped to their associated desire.

Every desire has at least one manifestable action in the default action catalog. The action catalog is intentionally data-driven. The original game had hundreds of concrete actions, many of which are animation or world-interaction primitives. Adding them does not require changing the cognitive engine.

## Tests currently passing

The v0.1 suite currently covers:

- exact 40-desire / 61-source vocabulary coverage;
- no action toward unseen objects (epistemic verisimilitude);
- hunger selecting perceived edible targets;
- motive competition and threat interruption;
- online reward/punishment changing later action preference;
- reinforcement reversal;
- decision-tree generalization over contextual attributes;
- different histories producing persistent divergent minds;
- player goal inference across different surface demonstrations;
- inferred player purpose driving a nonliteral goal-equivalent action;
- plan interruption and resumption;
- mind save/load and transplant onto a different creature type;
- threat-biased attention and exploration-map updates;
- a 250-tick mixed-condition anti-collapse run with diversity/entropy bounds.

## What is not yet historically exact

The exact equations for desire integration, desire dependency interactions, source weighting, suppression duration, plan scoring, decision-tree induction/pruning, feedback credit assignment, forgetting, player-attitude updates, developmental-stage effects, and expression are not yet fully recovered from the executable. v0.1 makes each of these operational so the full loop can be tested, but they remain Challenger mechanisms that should be replaced when exact implementation evidence becomes available.

## Validation rule

Functional completeness is not success by itself. The original Black & White Creature remains the Champion until this reconstruction is run through the same behavioral protocol and reproduces or improves the original behavioral signatures. Any inferred mechanism that fails that comparison should be revised or removed, even if it appears cognitively elegant.
