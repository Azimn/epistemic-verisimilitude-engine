# Preliminary Gray-Box Audit of the Black & White Creature

Status: 2026-09-14

## What this document is

This is the first test result for the original Black & White Creature using the symptoms-of-artificiality framework. It is a gray-box architectural audit, not yet a runtime behavioral verdict. The distinction is intentional. A recovered mechanism is evidence that a behavior can exist, but it is not evidence that the shipped Creature expressed that behavior robustly.

The audit uses four statuses. `Strong structural support` means the recovered implementation contains an explicit mechanism that should generate the target behavior. `Moderate structural support` means the relevant state exists but the controlling update path is incomplete or uncertain. `Weak structural support` means only indirect machinery has been found. `Not applicable` means the symptom assumes a language-driven agent and does not transfer cleanly to Black & White.

## Result

| Artificiality dimension | Preliminary status | Recovered evidence | Runtime question that remains |
| --- | --- | --- | --- |
| Autonomous initiative | Strong structural support | Continuous desires, multiple desire sources, dominant-desire selection, agenda, exploration map, vision, inspected-object state | Does the Creature generate sustained meaningful behavior without player prompting, or fall into a small idle/action cycle? |
| Conflicting motives | Strong structural support | Multiple concurrent desires, suppression, unsuppression, ranking, dominant desire, source-specific updates and satisfaction clearing | Do conflicts produce history-sensitive hesitation, switching, resumption and tradeoffs rather than deterministic priority changes? |
| Embodied need-driven behavior | Strong structural support | Hunger, fear, play, curiosity and bodily urges exist as explicit desires with growth, decay and creature-type timing | Are bodily dynamics visibly integrated with learned/social behavior over long runs? |
| Spontaneous thought | Not directly applicable | The Creature is primarily an embodied action system, not a language-based inner-monologue system | The behavioral analogue is spontaneous attention and self-initiated action, tested separately. |
| Shallow self-narrative | Not applicable | No conversational self-narrative is required by the architecture | A future language layer must not be credited to the original Creature. |
| Too-clean introspection | Not applicable | The original system does not present linguistic introspection to the player | Nonverbal leakage of conflict through gaze, face and action can be tested instead. |
| Contextual learning | Strong structural support | Large learning subsystem, previous contexts, previous action contexts, previous lesson, learning episodes linked to attribute tests | Does learning materially change later action selection under matched probes? |
| Generalization beyond memorized exemplars | Strong structural support | Decision trees are parameterized by desire/action and learn over attribute tests and learning episodes | How well does learned behavior transfer to novel objects, and how often does it overgeneralize? |
| Long-term consequence of experience | Moderate to strong structural support | Persistent beliefs, action opinions, previous-action state, learning history, attitude-to-player state and `SaveMind` entry point | What survives long delays, save/load cycles, changing physical state and extinction? |
| Prospective memory | Weak to moderate structural support | Agenda, plan state, current plans and subaction decomposition exist | Can an unfinished or delayed concern influence behavior after distraction, or are plans only short execution structures? |
| Habit formation | Moderate structural support | Repeated action context, action opinions, feedback-driven desire changes and learned decision structures can all create path dependence | Does repetition create gradual behavioral inertia distinct from immediate reward preference? |
| Prediction/modeling of another agent | Strong structural support for the player | `CreaturePerceivedPlayerDesires`, detected player actions, targets, magic and mimic state are explicit | Does the Creature infer player goals across different surface actions rather than merely imitate? |
| Rich relationship development | Moderate structural support | A dedicated `CreatureAttitudeToPlayer` structure is large and persistent | Does supportive versus punitive history alter neutral future interaction in a graded, durable way? The current decomp has not yet recovered the update algorithm. |
| Unconscious or implicit carryover | Strong structural support | Previous contexts, desire sources, action contexts, suppression state and learned opinions can influence later choice without requiring explicit current representation | Does interrupted behavior show residual influence after attention moves elsewhere? |
| Repetitive cognitive rhythm | Unknown | Architecture alone cannot reveal emergent temporal repetition | Requires long-run action-sequence logging and entropy/periodicity analysis. |
| Personality permeating behavior | Moderate structural support | `CreatureInnatePersonality` is embedded in `CreatureMental`, and desire dynamics vary by creature type | Which behaviors are actually modulated by these fields, and are differences stable enough to be experienced as personality? |
| Situated attention | Strong structural support | Vision state, look state, exploration map, inspected-object memory and object-specific beliefs | Is attention selectively history-dependent, or does perception effectively collapse back to globally available game state? |
| Nonverbal expression of internal state | Moderate structural support | Face state and look state coexist with desires, agenda and attention systems | Are expression changes driven by internal dynamics strongly enough to communicate state without scripted cues? |
| Consequence of developmental history | Moderate structural support | Development-phase data, creature-type desire timing, learning histories and innate personality all provide developmental variables | Does early experience create later differences that remain visible after immediate conditions are matched? |

## Preliminary interpretation

The Creature is a substantially stronger candidate for the artificiality harness than a normal legacy game NPC. It has explicit machinery for several dimensions that modern LLM characters often fake at the language layer: continuous motives, embodied needs, imperfect object knowledge, generalized learned opinions, player modeling, persistent history, and nonverbal expression.

The strongest predicted advantage is not conversational sophistication. It is causal depth. The architecture contains multiple pathways by which prior experience can alter future behavior before any presentation layer is involved.

The largest unresolved risk is behavioral collapse. The presence of beliefs, motives, plans and learning history does not guarantee that the final agenda/action selector preserves their differences. A sophisticated internal system can still funnel many distinct internal histories into the same small set of visible actions. The matched-history divergence test is therefore the highest-priority experiment.

A second major uncertainty is timescale. The code clearly supports immediate and intermediate context. It does not yet prove rich prospective memory, delayed commitments, gradual habits, or multi-hour unresolved concerns. Those dimensions should be treated as open rather than inferred from the existence of plans.

A third uncertainty is social scope. The recovered player model is unusually interesting, but it may be specialized to the god-player relationship rather than representing a general capacity to model arbitrary other agents. Our future engine should not silently generalize this historical mechanism beyond what the original system demonstrates.

## Current verdict

The Creature passes the architecture-admission threshold for full behavioral testing. It is not yet justified to say that it passes the symptoms-of-artificiality battery itself.

The most diagnostic first runtime campaign is a matched-history experiment with identical final probes, followed immediately by reinforcement reversal, novel-object generalization, player-intention inference, and interruption/resumption. Those five experiments can tell us whether the recovered architecture actually produces persistent causal individuality or mostly produces convincing local reactions.
