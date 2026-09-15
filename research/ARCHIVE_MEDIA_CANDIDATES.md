# Archive Media Candidates for Black & White Testing

Status: 2026-09-14

These Internet Archive items may help establish a reproducible Black & White test environment, but they should not be treated as equivalent evidence sources. This file records what each item is useful for and what should not be inferred from it.

## Best immediate candidate: original English Black & White Windows ISO

Source: https://archive.org/details/black-white-win

The item is identified as the English Windows 2001 release of Black & White and exposes a 611.7 MB archive containing an ISO image. This is the best current candidate for installing the original game and building the runtime behavioral harness.

Important limitation: `bw1-decomp` does not accept the SafeDisc-wrapped retail executable directly. Its documentation says that the Windows targets require a decrypted executable plus the original game DLLs. The decomp supports Windows 1.00, 1.10, and 1.20 and verifies the supplied files by SHA-1 before splitting or rebuilding.

Expected executable hashes from `openblack/bw1-decomp`:

- BW1W100 decrypted `runblack`: `d810fe43e2956f2b76533ab698632756ba99b44d`
- BW1W110 decrypted `runblack`: `44315eb19b6e2ab9023ea330b99bf5d471597402`
- BW1W120 decrypted `runblack`: `bccccbd3a08fe9a5d6cf59cd114e916401abfb51`

The original disc is still useful even if its executable remains SafeDisc-wrapped because it can provide authentic game data and the shipped DLLs. The DLL hashes can be compared to the decomp's expected files to establish which release/version is present.

For BW1W100 the expected DLL SHA-1 values are:

- `LHaudiodllR.dll`: `35f149cb77e9f770751112c0c814331c5b92bb4d`
- `LHLogR.dll`: `30a92037f5b0df604e5fa63aedb4633a6fcdb226`
- `LHMultiplayerR.dll`: `ef08506f38ea430b9c8348e0f9d44385964ff4d6`
- `LHDialogLib.dll`: `64a22b88a51adc4bc119777642263e419ea8d09e`

For BW1W120 the expected values are:

- `LHaudiodllR.dll`: `35f149cb77e9f770751112c0c814331c5b92bb4d`
- `LHLogR.dll`: `3c42f20350da2c54eb1ba0a61829b94d9883669a`
- `LHMultiplayerR.dll`: `4042119212fb6a5da6d736b059347f340eb4cd17`
- `LHDialogLib.dll`: `64a22b88a51adc4bc119777642263e419ea8d09e`

The version-specific DLL hashes give us a clean way to identify an install even when the protected executable is not directly usable by the decomp.

## Black & White Complete Collection PL

Source: https://archive.org/details/black-and-white-complete-collection-pl

This item is a 1.1 GB Polish "Complete Collection" containing Black & White and Creature Isle, but the Archive page identifies it as an ELAmigos repack. It may be useful as a convenient source for examining Creature Isle content or for comparing installed data, but it should not be used as a canonical binary reference because repacks can replace executables, alter installers, pre-apply patches, remove protection, or change support files.

Use it only as a secondary convenience source. Any executable or DLL taken from it must be hash-checked against known original releases before it is treated as historical evidence.

## Black & White 2 (USA)

Source: https://archive.org/details/BlackWhite2USA

This is the 2005 sequel, not the architecture currently being reconstructed. It is therefore not an input to the BW1 decomp campaign.

It is nevertheless useful as a later comparative experiment. The Archive description explicitly characterizes the sequel's Creature learning in terms of lessons and player encouragement/discouragement of candidate actions. Once the BW1 harness is working, the same behavioral tests could be adapted to BW2 to determine what Lionhead retained, simplified, or changed between the two generations.

Keep all BW2 data and conclusions in a separate experiment so that no BW2 behavior is accidentally attributed to the 2001 architecture.

## `BlackWhiteUSA`

Source supplied: https://archive.org/details/BlackWhiteUSA

The item page did not resolve reliably through the current research tooling, so its exact contents and provenance are not yet verified. If it is a Redump-style or otherwise unmodified USA retail image of Black & White 1, it may be even more valuable than the `black-white-win` upload because preservation-oriented disc images provide stronger provenance. It should be inspected for uploader metadata, format, disc hashes, and file listing before use.

## Recommended use sequence

1. Use an original or preservation-grade Black & White 1 disc image as installation media.
2. Install without using a modern repack as the reference environment.
3. Hash the installed Lionhead DLLs and compare them with the known `bw1-decomp` version hashes.
4. Determine whether the installation is 1.00, 1.10, or 1.20.
5. Keep the retail protected executable separate from any decrypted reference executable used by `bw1-decomp`.
6. Use the original runtime for behavioral testing and CHL instrumentation.
7. Use the decrypted, hash-matched executable only for decomp/reconstruction work.
8. Treat Creature Isle and Black & White 2 as separate follow-up experiments.

## Provenance rule

Do not commit commercial game binaries, disc images, extracted copyrighted assets, or decrypted executables to this repository. Store only hashes, version information, experimental scripts written for this project, test logs, architectural findings, and reproducible instructions. This keeps the research repository focused on evidence and our own work rather than redistributing the original game.
