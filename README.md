# Epistemic Verisimilitude Engine

This repository investigates architectures for artificial characters whose beliefs, motives, learning, memory, attention, and behavior arise from their own simulated experience rather than privileged access to implementation state.

The first research track is a code-level archaeology of Lionhead Studios' Black & White Creature AI. The aim is to reconstruct what the original system actually did from decompilation evidence, contemporary technical writing, reverse-engineering projects, and controlled experiments against the original runtime. Historical mechanisms will be kept explicitly separate from mechanisms designed by this project.

The current working dossier is [`research/BLACK_WHITE_ARCHAEOLOGY.md`](research/BLACK_WHITE_ARCHAEOLOGY.md). It maps Richard Evans' published architecture to recovered Black & White structures, identifies supporting modding and debugging tools, records provenance and licensing concerns, and defines the highest-value mechanisms to recover before implementation begins.

The long-term goal is not a Black & White clone. It is a standalone, testable character engine that can determine which recovered mechanisms meaningfully reduce observable symptoms of artificiality.