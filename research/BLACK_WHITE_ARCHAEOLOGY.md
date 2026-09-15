# Black & White Creature AI Archaeology

Status: 2026-09-14

This repository is being used to determine how much of the original Black & White creature architecture can be recovered from surviving code, reverse-engineering work, contemporary technical writing, and executable instrumentation. The immediate goal is not to reproduce the game. The goal is to recover the cognitive mechanisms that made the Creature feel like an entity with its own experience, then test those mechanisms against the symptoms-of-artificiality framework before deciding what belongs in a new standalone engine.

## Current conclusion

The surviving material is much stronger than a normal historical reconstruction. The openblack `bw1-decomp` project contains named class layouts, function signatures, scripting hooks, partially recovered implementations, and a build system designed to reach byte-identical behavior with the original executable. The recovered architecture maps closely onto Richard Evans' published account of Black & White as an augmented belief-desire-intention system using different representations for different cognitive jobs.

The architecture is not simply a utility AI with reinforcement values. The recovered mental object contains persistent desires, an agenda and planning layer, object-specific beliefs, decision-tree structures, learned action opinions, a large learning subsystem, attitude toward the player, innate personality, vision state, exploration memory, previous actions, look state, face state, inspected-object memory, and debugging state. This strongly supports treating Black & White as a serious cognitive-engine donor rather than only a historical curiosity.

## Architecture reconstruction

| Published concept | Recovered implementation evidence | Current interpretation | Confidence |
| --- | --- | --- | --- |
| Epistemic verisimilitude | `CreatureMental::AddBeliefAboutObject`, `CreatureBeliefList`, `CreatureVisionState`, inspected-object state | Object beliefs are acquired through creature-facing systems rather than arbitrary omniscient world access. The exact perceptual gating path still needs function-level tracing. | High for structure, medium for exact data flow |
| Object-specific beliefs | `CreatureBeliefs`, `CreatureBeliefList::GetBeliefAboutObject`, `AddBeliefAboutObject` | Individual entities have explicit belief records. | High |
| Generalized opinions | `DecisionTreeCollection`, `DecisionTreeAgenda`, `DecisionTree`, `AttributeTest` | Generalization is organized around decision trees. Constructors bind tests to a desire and action, matching Evans' account of learned opinions about what kinds of objects are appropriate for satisfying a motive. | High |
| Learning examples for generalization | `AttributeTest` owns linked `CreatureLearningEpisode` records | Decision-tree learning appears to operate over retained learning episodes rather than fixed designer rules alone. The tree induction functions remain an extraction target. | High for representation, medium for algorithm |
| Desires | `CreatureDesires` stores per-desire state, increase time, sources, suppression, dominant-desire selection, feedback modification, satisfaction checks, and post-action updates | Motives are continuous, sourced, competing, suppressible, temporally changing, and trainable. They are not merely one-shot goals. | High |
| Desire individuality | `CreatureInitialDesireInfo` supplies initial ranges, decay and growth parameters; `CreatureDesireForType` varies timing by creature type | Two creatures can begin and develop with different motivational dynamics even before player learning. | High |
| Intention and planning | `CreaturePlan` binds a desire, an action, several belief pointers, and evaluation values; `CreaturePlanState` tracks many plans; `CreatureAgenda` holds plan state, active plans and subactions | The system transforms motivation plus beliefs into selected plans and then decomposes plans toward executable behavior. | High |
| Action memory | `CreaturePreviousActions`, `PreviousActionContextStack` | Recent and accumulated action context is explicitly represented rather than discarded after execution. | High |
| Learning history | `CreatureLearning` contains previous context stacks, previous action-context stacks and a previous lesson | Learning can refer back to what the Creature was trying to do and the context in which it acted. | High |
| Motivational provenance | `CreatureContext` stores a plan and its `CREATURE_DESIRE_SOURCE` | The system preserves why a context existed, not only what action occurred. This is potentially important for credit assignment. | High |
| Player modeling | `CreatureAttitudeToPlayer` contains a large `CreaturePerceivedPlayerDesires` structure | The Creature appears to maintain a model of what the player wants. This is consistent with historical descriptions of inferring player intention rather than only copying observed motor behavior. Exact update rules remain to be recovered. | High for representation, medium for algorithm |
| Imitation and observational learning | `CreatureMimicState` records a detected player action, magic type, target object and coordinates | The system has an explicit state for interpreting and reproducing observed player activity. | High |
| Innate personality | `CreatureInnatePersonality` is embedded directly in `CreatureMental` | Personality is represented below the visible behavior layer. Field semantics are still largely unnamed. | Medium |
| Embodied attention and exploration | `CreatureVisionState`, `CreatureExplorationMap`, `CreatureLookState`, `CreatureObjectsInspected` | The Creature has a partial, situated interaction history with the world rather than a pure global-state controller. | High for structure, medium for semantics |
| Behavioral expression | `CreatureFaceState`, look state and agenda state coexist with cognition | Internal state has dedicated channels into nonverbal expression, which may contribute substantially to perceived life-likeness. | Medium until update paths are traced |

## Recovered desire mechanics

The decompiled `CreatureDesires` interface exposes a more sophisticated motive system than the short historical descriptions suggest. Desires can be suppressed and unsuppressed, updated continuously, changed after actions, ranked, made dominant or weak, modified following feedback, tested for satisfaction, driven by multiple sources, and cleared or changed after satisfaction. Each desire also has growth and decay information and creature-type-dependent timing. The recovered desire enumeration includes psychologically and bodily meaningful categories such as compassion, anger, play, hunger, fear, curiosity, and elimination urges.

A partially decompiled initializer provides further evidence about the design. Each desire receives initial values from a configured range, creature-type-specific increase timing, explicit decay and growth parameters, and source initialization. Some initial variation is randomized. This means apparent individual differences are partly generated from parameterized motivational dynamics before experiential learning alters them.

## Recovered learning and generalization structure

Richard Evans described the architecture as representationally heterogeneous: individual beliefs were symbolic, generalized opinions were decision trees, desires were perceptron-like structures, and intentions were plans. The current decomp strongly corroborates the symbolic-belief, decision-tree and plan portions directly. The desire structures also show multiple weighted or sourced inputs and feedback-driven modification, although the exact original perceptron computation still needs to be recovered at instruction level before we should claim an exact reimplementation.

The learning subsystem is especially important. `CreatureLearning` is large and retains previous contexts and action contexts. `AttributeTest` stores learning episodes and an attribute stack, while decision-tree constructors are parameterized by desire and action. This suggests that a lesson is not merely stored as a scalar reward against an action. The system appears designed to generalize from contextual episodes into opinions about when an action or target is suitable for a particular desire.

## Player-intention modeling

One of the highest-value findings is the explicit `CreaturePerceivedPlayerDesires` state inside `CreatureAttitudeToPlayer`. Historical descriptions say the Creature attempted to infer the intention behind player behavior during observational learning. The recovered `CreatureMimicState` additionally stores detected player action, magic, an object reference and spatial coordinates. Together these structures suggest a pipeline in which player behavior is perceived, classified, related to a target and location, interpreted motivationally, and then used by the Creature's own behavior system.

This may be more important to our project than literal reinforcement learning. A lifelike artificial character should not merely remember that a person performed an action. It should form an imperfect model of what that person was trying to accomplish and allow that model to influence future behavior.

## Experimental access to the original runtime

The original game exposes useful cognitive controls through its CHL native scripting interface. The recovered native-function table includes a creature desire query, action-performance counters, an operation that grants complete learning, per-action knowledge control, agenda-priority control, and desire disabling. This creates a plausible path to repeatable experiments inside the original engine.

Community tools make that path more practical. Daniels118 maintains CHL compilation, decompilation and assembly tools for Black & White and Creature Isle. The related `BWCI_debugger` can debug Black & White 1 and Creature Isle CHL scripts and provides a debugger abstraction with a GDB-like interface. The same author's mod loader loads additional DLLs and can expose a runtime console. This toolchain could let us build scripted training histories, query selected internal states, count behavior, and potentially add our own instrumentation without changing the cognitive rules under test.

`BW-Ultimate` is also a potentially important archaeological source. Its repository contains original and Creature Isle scripts, DLL work, and a roughly 30 MB archived IDA database. That database may preserve names, annotations or reverse-engineering knowledge that has not yet migrated into `bw1-decomp`. It should be compared against the modern decomp before we spend time rediscovering symbols manually.

## Source hierarchy

| Source | Role in the project | Reuse status |
| --- | --- | --- |
| https://github.com/openblack/bw1-decomp | Primary implementation archaeology. Named structures, functions, symbols, partial C/C++ decompilation and byte-matching workflow. | Repository is CC0 1.0, but any use must still respect third-party rights and original game assets. |
| https://github.com/openblack/openblack | Modern engine reimplementation, LHVM work, file formats and a possible future host for testing. It is not currently a faithful implementation of the full Creature AI. | GPL-3.0. Treat as tooling/reference unless the standalone engine adopts compatible licensing. |
| https://github.com/openblack/bw1-patches | Reproducible binary patch infrastructure for modern systems. Potentially useful for an experimental build of the original game. | Check project license before copying code. |
| https://github.com/ShaneDoyle/BW-Ultimate | Historical Creature Isle reverse engineering, scripts, DLL work and IDA database archive. | Research source first. Verify licensing and provenance before code reuse. |
| https://github.com/Daniels118/blackandwhite | CHL compiler, assembler and disassembler for the original game. | GPL-3.0. Useful as external tooling. |
| https://github.com/Daniels118/blackandwhite_ci | CHL compiler, decompiler and assembler for Creature Isle. | GPL-3.0. Useful as external tooling. |
| https://github.com/Daniels118/BWCI_debugger | Runtime CHL debugger for Black & White 1 and Creature Isle. | GPL-3.0. Useful as external instrumentation. |
| https://github.com/Daniels118/BW_mods_loader | DLL loader and game debug console support. | GPL-3.0. Useful as external instrumentation. |
| Richard Evans, "The Future of AI in Games: A Personal View," Game Developer, August 2001 | Primary contemporary architectural description and source of the term epistemic verisimilitude. | Conceptual source. Cite rather than copy. |
| Richard Evans, "Varieties of Learning," AI Game Programming Wisdom, 2002, pp. 567-578 | Primary technical description of learning, including the hybrid representation strategy. | Conceptual source. Obtain and cite the chapter legally. |
| Peter Molyneux, "Postmortem: Lionhead Studios' Black & White," 2001 | Primary production account and evidence about design goals, individuality, learning, villager AI and performance constraints. | Conceptual source. |
| Noah Wardrip-Fruin, "Beyond Anthropomorphic Intelligence," 2008 | Useful secondary synthesis of Evans' architecture and representational promiscuity. | Secondary source. |
| The Making of Black & White, Prima strategy guide and official clue/manual material | Potential behavioral documentation, training rules and historical implementation clues not necessarily exposed in source. | Acquisition and review target. |

## What should be recovered before implementation begins

The next archaeological pass should focus on function behavior rather than adding more architecture speculation. The highest-value targets are the exact desire activation computation, feedback weight update, decision-tree induction and pruning logic, belief creation and invalidation, target scoring, plan competition, satisfaction and credit assignment, perceived-player-desire updates, mimic-learning transitions, forgetting or decay, and any development-stage changes to learning rates or motive dynamics.

The key standard should be provenance. Every mechanism in a Black & White reconstruction should be labeled as directly recovered from code, strongly supported by contemporary documentation, inferred from structure, or newly designed by us. That will prevent a modern reconstruction from quietly turning into an architecture we invented and then incorrectly attributed to Lionhead.

## Recommended experimental sequence

Before constructing a standalone clone, the strongest experiment is to run the original cognition as a black-box and gray-box system. We can create controlled CHL scenarios, reset or manipulate specific known states, expose desire and action counters, apply reproducible reward or punishment histories, and compare later behavior under matched test conditions. The same scenarios can then be reproduced in a standalone reconstruction. If the reconstructed engine matches both the internal architecture and the original behavioral signatures, we have much stronger evidence that we recovered the important mechanism rather than merely building something inspired by it.

This repository should therefore serve three roles at once: an evidence ledger, a behavioral test specification, and eventually a clean standalone implementation. The evidence ledger should remain separate from implementation so that historical findings and our own extensions never become conflated.