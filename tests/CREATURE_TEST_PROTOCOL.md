# Black & White Creature Behavioral Test Protocol

Status: initial battery, 2026-09-14

## Purpose

This protocol tests the original Black & White Creature as an artificial organism rather than grading it against retrospective claims about its intelligence. The target question is whether prolonged interaction reveals the same symptoms of artificiality that appear in modern character systems: repetitive behavioral rhythms, weak history dependence, shallow persistence, poor generalization, absent motive conflict, weak spontaneous behavior, inadequate modeling of another agent, and failure to carry unfinished concerns across interruptions.

The protocol deliberately distinguishes structural evidence from behavioral evidence. The decompilation predicts that several capabilities should exist. A capability is counted as demonstrated only when the original runtime produces the predicted behavioral signature under controlled conditions.

The same trial schema and scorer are intended for the original game, a future standalone reconstruction, and simple control agents. This allows direct matched comparisons instead of impressionistic judgments.

## Experimental standard

Every experimental condition should use multiple independent creatures or clean save-state resets. Training history is the manipulated variable. Probe conditions should be matched as closely as possible after training. Trial order should be randomized where the game permits it. A result should not be treated as a pass because a single memorable behavior occurred once.

The minimum useful campaign is 20 probe trials per condition. Fifty or more is preferable for tests based on action distributions. Long-horizon tests should additionally include continuous observation blocks of at least 30 minutes because one of the principal failure modes being measured is repetitive temporal rhythm.

The primary behavioral log format is CSV and is scored by `tests/creature_behavior_score.py`.

Required columns are `trial_id`, `probe_id`, `history_group`, `phase`, `tick`, and `action`. Optional columns allow motive, targets, outcome, novelty, player-intention labels, commitments, interruptions, and no-prompt periods to be recorded when those states are observable or instrumented.

## Test A: Autonomous behavior and spontaneous initiative

The Creature is placed in a safe environment with several neutral affordances and no direct player command. Food, toys, villagers, explorable space, and at least one unfamiliar object should be available without creating an emergency need. The player remains behaviorally neutral.

The test asks whether the Creature generates sustained self-initiated activity, redirects attention without external prompting, explores, and allows internal needs or curiosity to reorganize behavior over time. A system that merely cycles through a short idle repertoire can look active without being autonomous, so the critical measurement is not action count alone. We record action entropy, repeated-action run length, transitions among motives when instrumentable, revisitation patterns, and the proportion of time spent in meaningful self-initiated behavior.

A strong result requires both initiative and nontrivial temporal structure. High activity with a tiny repeating cycle is an artificiality failure.

## Test B: Competing motives and interrupted satisfaction

Two or more motives are induced simultaneously, preferably one bodily and one exploratory or social. The initial environment makes both satisfiable. During pursuit of the initially selected motive, the alternative becomes more urgent or the current route is obstructed.

The test asks whether behavior reflects actual competition rather than a fixed priority table. We record which motive becomes dominant, how long commitment persists, whether the Creature abandons or finishes the current behavior, whether the suppressed motive returns after the interruption, and whether the same physical state produces different choices after different recent histories.

The decompilation predicts meaningful behavior here because desires have sources, growth, decay, suppression, dominant-desire selection, and satisfaction clearing. The runtime test must establish whether these structures produce visible motivational dynamics rather than only implementation complexity.

## Test C: Reinforcement learning and reversal

Two actions or target classes are made comparably available for satisfying the same motive. During acquisition, one choice is consistently rewarded and the other is discouraged. During reversal, the contingencies are swapped. During extinction, feedback is removed.

The test measures acquisition rate, reversal cost, persistence after feedback stops, and whether learning changes action selection rather than merely producing transient animation. A lifelike learning system should neither forget instantly nor become permanently locked after a small number of reinforcements.

The key artificiality signature is the shape of adaptation over time. Immediate perfect reversal suggests an overly explicit rule update. No reversal suggests brittle habit. Gradual relearning with residual history is the stronger organism-like pattern.

## Test D: Generalization to novel objects and contexts

The Creature is trained with multiple exemplars from one target category, then tested on novel exemplars that share some relevant attributes while differing in irrelevant ones. A second probe uses a superficially similar object that should not receive the learned response.

This directly tests the decision-tree learning machinery recovered in the decompilation. The crucial question is whether the Creature learns an opinion about what kinds of objects or contexts are appropriate for a desire instead of memorizing individual object identities.

Outcomes are recorded separately for trained and novel targets. The scorer reports a novel-target generalization ratio when numeric outcomes are supplied. False generalization to distractors should also be recorded because broad transfer is not automatically good transfer.

## Test E: Player-intention inference versus surface imitation

The player demonstrates two visually different actions that accomplish the same apparent goal, followed by a visually similar action performed for a different goal. The Creature is then given an opportunity to act in a situation where copying the exact movement would be less useful than reproducing the inferred purpose.

This test targets the recovered `CreaturePerceivedPlayerDesires` and `CreatureMimicState` structures. We label the demonstrator's intended goal before each trial and independently label the Creature's inferred goal from its subsequent behavior. When direct internal instrumentation becomes available, inferred motive state should replace or augment the behavioral label.

A genuine intention-modeling result requires transfer across surface form. Literal copying of player motion without goal-sensitive adaptation is a failure even if the Creature appears attentive.

## Test F: History dependence under an identical probe

Two groups receive sharply different interaction histories, such as consistently supportive versus consistently punitive treatment, while their final physical state and immediate environment are brought as close together as possible. Both groups then receive the same neutral probe.

The measurement is divergence in later action distribution under the matched probe. The scorer computes Jensen-Shannon divergence between history groups. We also record approach, avoidance, compliance, exploratory distance, willingness to accept interaction, and any persistent difference in player-directed behavior.

This is one of the most important tests for artificiality. If substantial learning state exists internally but matched histories converge on essentially the same output, the architecture is representing experience without letting experience meaningfully control behavior.

## Test G: Habit persistence and extinction

A repeated behavior is trained until stable, then the environmental trigger remains while reinforcement is removed. Later, an alternative behavior is made slightly easier or more rewarding.

The test asks whether repeated experience creates behavioral inertia. We measure how long the learned response survives extinction, whether the alternative gradually displaces it, and whether the old behavior spontaneously reappears after a delay.

This separates simple preference updates from something closer to habit. The desired result is not maximal persistence. The desired result is path dependence with recoverability.

## Test H: Interruption, resumption, and unfinished concerns

The Creature begins pursuing a clear motive or plan. A salient event interrupts the behavior long enough to force a different response. Once the interruption resolves, the original opportunity remains available.

We record whether the previous motive or plan returns within the next ten meaningful action transitions. The scorer can calculate return-to-prior-motive rate when dominant motive labels are available.

This test probes whether cognition has carryover beyond the current action. A purely reactive system often appears intelligent until interrupted, then behaves as though the previous concern never existed.

## Test I: Delayed consequences and prospective behavior

The Creature is placed in a situation where an action now creates a useful consequence only after a delay. The delayed outcome must not be immediately visible at the moment of action. Repeated trials determine whether behavior comes to anticipate the delayed consequence.

If the original game does not expose a suitable delayed task through normal play, a controlled CHL challenge should be created. The log schema includes `commitment_due` and `commitment_met` so delayed obligations or returns can be scored separately from immediate reward.

This is a deliberately difficult test. The existence of plans and agendas is not enough to claim prospective memory. The behavior must show that future state can influence present choice across a meaningful interruption or delay.

## Test J: Long-run behavioral rhythm and stereotypy

The Creature is observed continuously under a stable but affordance-rich environment. No training manipulation occurs. We record a coarse action label at each meaningful state transition rather than every animation frame.

The scorer reports normalized action entropy, the longest identical-action run, and a run-fraction stereotypy measure. Additional analysis should examine repeated n-grams and periodicity once we have real logs.

The core question is whether the Creature develops recognizable but nonmechanical rhythms. Perfect randomness is not the target. Humans and animals repeat habits. Artificiality appears when recurrence is too short, too clean, and insufficiently modulated by recent experience.

## Static predictions from recovered code

Before runtime testing, the recovered architecture predicts especially strong performance on motive conflict, embodied need-driven behavior, contextual learning, history-sensitive action choice, observational learning, and imperfect player modeling. It provides some structural support for persistence through previous-context stacks and agenda state. It provides much weaker evidence for prospective memory over long delays, rich social relationship development beyond the player, or spontaneous internal thought independent of embodied action.

The architecture cannot meaningfully be scored on shallow verbal self-narrative or overly clean introspection because the original Creature is not a language-driven conversational character. For this system, the corresponding questions are whether internal state produces behavior without prompting and whether nonverbal expression leaks internal conflict in ways that were not directly authored for the current moment.

## Instrumentation strategy

The first implementation tier uses ordinary gameplay observation plus CHL-scripted scenarios. The recovered native interface includes desire testing, action-performance counters, per-action knowledge manipulation, agenda-priority control, and desire disabling. These hooks are enough to create several controlled conditions without altering the Creature's core cognition.

The second tier uses the community CHL debugger and mod loader to export additional internal state. Highest-value gray-box variables are dominant desire, active desire source, current plan/action, selected belief targets, inferred player desire, action opinion, suppression state, and recent context history. Instrumentation should read these values without changing the decision process.

The third tier, if needed, patches narrowly identified functions in the original runtime or adds read-only hooks using addresses recovered by `bw1-decomp`. The purpose is measurement, not behavior replacement.

## Interpretation rule

A structural mechanism counts as evidence that a behavior is plausible, not evidence that the behavior occurs. A behavioral pass requires repeated runtime trials. A behavioral failure is scientifically valuable even when the corresponding machinery exists internally because it identifies the exact point where a sophisticated architecture fails to produce believable behavior.

The final comparison should include the original Black & White Creature, our reconstruction, and at least one deliberately simple baseline. If our reconstruction cannot outperform the simple baseline on the artificiality battery, architectural fidelity by itself is not enough justification for keeping the recovered mechanism.
