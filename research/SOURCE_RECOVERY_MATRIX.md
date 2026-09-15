# Black & White Creature AI Source Recovery Matrix

Status: 2026-09-14

## Purpose

The reconstruction target is no longer only the published architecture. The surviving evidence supports recovering the original Black & White Creature cognition from four independent views: executable structure, serialized CreatureMind state, runtime behavior, and contemporary technical descriptions. A mechanism should be treated as high-confidence when two or more independent evidence channels agree.

## Evidence hierarchy

### Tier 1: implementation evidence

**openblack/bw1-decomp** is the primary structural source. It exposes named classes, data layouts, function addresses and partially matched C/C++ for the original executable. It currently provides direct evidence for `CreatureMental`, desires, beliefs, agenda/planning, decision trees, action opinions, learning contexts, player attitude/modeling, vision, exploration, look/face state and related subsystems.

**ShaneDoyle/BW-Ultimate** is a second implementation source. Its mod DLL already hooks original Creature runtime functions including `CreatureMental::SaveMind`, `Creature::Load`, `Creature::LoadFullyQualified` and file reads. It reads and writes known fields in serialized `.erc` CreatureMind files. This establishes that the mind-file format is tractable and gives us existing instrumentation code and function addresses to compare with the modern decomp.

Historical utilities such as **Kong**, **CreatureStats**, **BWEdit**, Cache's creature tools and related trainers are high-priority recovery targets. These programs modified `.erc` files directly. Even when source is unavailable, their binaries may encode field offsets, ranges, labels and transformation rules that can accelerate reconstruction of the serialization schema.

## Serialized-mind evidence

The Windows game stores player Creature minds as `.erc` files associated with a separate `Physique*.erc` file. Community documentation and scripting examples show that a trained mind can be loaded using `CREATE_CREATURE_FROM_FILE` while choosing a creature species independently. This gives us a critical experimental capability: hold cognition constant while changing body/species, or hold body constant while changing learned mind.

Community reports identify the ordinary `.erc` as carrying learned knowledge/behavior and at least some appearance-related state, while the `Physique*.erc` companion carries body/physique data. This separation should be tested rather than assumed perfectly clean.

`BW-Ultimate` provides direct code evidence that the serialized mind can be intercepted at `CreatureMental::SaveMind` and `Creature::Load`. It already reads/writes individual bytes at known positions, including a field at offset 8 and another located 17 bytes from the end of the file. These known fields are not necessarily cognitive variables, but they prove that targeted binary-field recovery is practical.

### Differential mind-file experiment

The fastest route to the complete serialization schema is controlled differential analysis.

1. Create a clean baseline Creature mind and save its `.erc`.
2. Make exactly one controlled change.
3. Save a new snapshot.
4. Binary-diff the two files.
5. Repeat the same manipulation from multiple independent baselines.
6. Correlate stable changed regions with decompiled save/load functions and runtime state.

High-value one-variable manipulations include one reward after a specified action, one punishment, teaching one action, teaching one miracle, changing one desire state, changing player treatment while holding physical state constant, observing one new object class, learning one object-specific preference and advancing one developmental stage.

Because the file is likely a structured serialization rather than a raw dump of `CreatureMental`, offsets must be mapped through the save/load order instead of naively matched to in-memory object offsets.

## Primary contemporary sources

**Richard Evans, "The Future of AI in Games: A Personal View," Game Developer, August 2001.** This is the most important accessible primary architecture article. Evans explicitly says its conclusions come from developing the Black & White Creature minds. It establishes the design target that users should feel they are dealing with a person and describes the system in terms of believable, malleable and useful creatures. It is also the primary source for the epistemic-verisimilitude design principle discussed elsewhere in this project.

**Richard Evans, "Varieties of Learning," AI Game Programming Wisdom, 2002, pp. 567-578.** This remains the highest-priority missing technical chapter. Secondary quotations and the current decomp agree on the heterogeneous representation strategy: symbolic beliefs about individual objects, decision trees for generalized opinions, perceptron-like desires and explicit plans/intentions. A legal copy of the chapter should be obtained and audited line by line against the decomp.

**Peter Molyneux, Black & White postmortem, 2001.** This is primary production evidence for the intended behavior. It states that the Creature was designed to learn, operate independently and be useful; that Evans investigated learning, practice and reinforcement; that learning produces individual personality; and that the team deliberately avoided adding randomness merely to create the appearance of a mind. It also says related AI principles were used for villagers, although some cooperative control was centralized for performance.

**Prima's Official Strategy Guide.** This is not implementation documentation but is valuable behavioral documentation. It includes creature-specific learning/reaction differences and concrete training procedures. Those claims can become runtime tests and can identify behavior that must be represented in the reconstructed parameter tables.

## Secondary technical source: Ian Millington

Ian Millington's *Artificial Intelligence for Games* chapter on teaching characters explicitly uses Black & White as the best-known example of the genre, but it should not be treated as a dump of Lionhead's source design. Its value is as a technical interpretation and experimental hypothesis generator.

Important mechanisms in the chapter include action representations containing action/object/indirect-object structure; contextual observational learning; the need to distinguish the observer's state from the demonstrated actor's state; recent input-output histories for feedback credit assignment; temporally decayed feedback across recent actions; pathological overgeneralization; and protected instincts/default behaviors that prevent learned agents from becoming nonfunctional.

These ideas should only be labeled "original Black & White" where the decomp, Evans, runtime behavior or serialized-state analysis independently confirms them.

## Independent comparison: MIT Synthetic Characters c4

Bruce Blumberg and colleagues' 2001 GDC paper, *Creature Smarts: The Art and Architecture of a Virtual Brain*, is not documentation of Black & White. It is an independent same-era architecture and must remain separated from the historical reconstruction.

It is valuable as a comparator because c4 integrates sensory processing, perception, attention/working memory, action selection, navigation, motor control and proprioception; uses creature-specific mental representations rather than an omniscient world model; and demonstrates animal-style action learning and clicker training. Once the Black & White reconstruction is stable, c4 mechanisms can be tested as alternative donors rather than silently attributed to Lionhead.

## Lower-confidence sources

The Medium article "Black & White: A Game of Reinforcement Learning" is a secondary simplification. Its author states that he had not played the game and was retelling another article. It is useful for discovering citations but should not establish implementation claims.

Community forum posts are operational evidence rather than authoritative architecture documentation. They become especially valuable when a claim can be reproduced, such as loading one mind into another species, direct `.erc` editing, persistent behavior after copying a mind file, or training differences between stock and experienced minds.

Later retrospectives and interviews can preserve details not published in 2001. Claims from them should be triangulated against contemporary material and code whenever possible.

## Current reconstruction strategy

The project should recover the Creature AI in the following order of confidence:

1. Trace `CreatureMental::SaveMind` and `Creature::Load` to reconstruct the `.erc` serialization schema.
2. Recover and inspect old `.erc` editors/trainers for field names, offsets and ranges.
3. Generate controlled mind snapshots and binary-diff one-variable training changes.
4. Map serialized changes to in-memory `CreatureMental` components and decompiled update functions.
5. Recover exact algorithms for desire activation/source integration, feedback credit assignment, action opinions, decision-tree learning, belief formation/invalidation, target scoring, plan competition, perceived-player-desire updates, mimic/intention learning, developmental changes, forgetting/decay and attitude-to-player effects.
6. Run the behavioral artificiality battery on the original runtime.
7. Build a standalone reconstruction with every mechanism tagged as recovered-code, primary-documented, inferred or newly-designed.
8. Validate the reconstruction against both state-change signatures and original behavioral distributions.

## Completion criterion

A "complete copy of the AI" should not mean reproducing every animation or game-specific class. For this project, completion means reproducing the cognitive causal chain closely enough that the standalone engine matches the original on:

- state transitions produced by controlled training histories,
- learned generalization across object/context probes,
- motive competition and satisfaction,
- player feedback effects and credit assignment,
- player-intention/observational learning,
- persistence across save/load,
- action selection under matched probes,
- developmental/personality variation where demonstrated,
- and long-run behavioral signatures measured by the artificiality harness.

If a subsystem can be omitted without changing those signatures, it is probably game infrastructure rather than part of the cognitive core we need to reproduce.