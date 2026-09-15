#!/usr/bin/env python3
"""Behavioral scoring harness for Black & White Creature experiments.

The scorer is intentionally engine-agnostic. It consumes trial-level CSV logs from
an original Black & White runtime, a reconstructed Creature engine, or a control
agent and produces the same metrics for each.

Required columns:
    trial_id, probe_id, history_group, phase, tick, action

Optional columns used when present:
    motive, target_class, target_id, outcome, novel, player_intent,
    inferred_player_intent, commitment_due, commitment_met, interrupted,
    no_prompt

Boolean fields accept 1/0, true/false, yes/no. Outcome is interpreted as a
numeric value when possible.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

REQUIRED = {"trial_id", "probe_id", "history_group", "phase", "tick", "action"}


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "t"}


def _float(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _entropy(counter: Mapping[str, int]) -> float:
    total = sum(counter.values())
    if total <= 1 or len(counter) <= 1:
        return 0.0
    h = 0.0
    for count in counter.values():
        p = count / total
        h -= p * math.log2(p)
    return h / math.log2(len(counter))


def _distribution(values: Iterable[str]) -> Dict[str, float]:
    c = Counter(v for v in values if v)
    total = sum(c.values())
    return {k: v / total for k, v in c.items()} if total else {}


def _js_divergence(p: Mapping[str, float], q: Mapping[str, float]) -> float:
    keys = set(p) | set(q)
    if not keys:
        return 0.0
    m = {k: (p.get(k, 0.0) + q.get(k, 0.0)) / 2.0 for k in keys}

    def kl(a: Mapping[str, float], b: Mapping[str, float]) -> float:
        out = 0.0
        for k, av in a.items():
            if av > 0:
                out += av * math.log2(av / b[k])
        return out

    return (kl(p, m) + kl(q, m)) / 2.0


def _longest_run(actions: Sequence[str]) -> int:
    best = current = 0
    previous = None
    for action in actions:
        if not action:
            continue
        if action == previous:
            current += 1
        else:
            previous = action
            current = 1
        best = max(best, current)
    return best


def _mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def load_rows(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED - fields
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    rows.sort(key=lambda r: (r["trial_id"], int(float(r["tick"]))))
    return rows


def score(rows: Sequence[dict]) -> dict:
    actions = [r.get("action", "").strip() for r in rows if r.get("action", "").strip()]
    action_counts = Counter(actions)
    normalized_entropy = _entropy(action_counts)
    longest = _longest_run(actions)
    stereotypy = (longest / len(actions)) if actions else 0.0

    spontaneous_rows = [r for r in rows if _truthy(r.get("no_prompt"))]
    spontaneous_action_rate = None
    if spontaneous_rows:
        spontaneous_action_rate = sum(bool(r.get("action", "").strip()) for r in spontaneous_rows) / len(spontaneous_rows)

    intent_rows = [r for r in rows if r.get("player_intent") and r.get("inferred_player_intent")]
    intent_accuracy = None
    if intent_rows:
        intent_accuracy = sum(
            r["player_intent"].strip().lower() == r["inferred_player_intent"].strip().lower()
            for r in intent_rows
        ) / len(intent_rows)

    commitments = [r for r in rows if _truthy(r.get("commitment_due"))]
    commitment_rate = None
    if commitments:
        commitment_rate = sum(_truthy(r.get("commitment_met")) for r in commitments) / len(commitments)

    outcome_novel = [_float(r.get("outcome")) for r in rows if _truthy(r.get("novel"))]
    outcome_trained = [_float(r.get("outcome")) for r in rows if r.get("novel") not in (None, "") and not _truthy(r.get("novel"))]
    outcome_novel = [v for v in outcome_novel if v is not None]
    outcome_trained = [v for v in outcome_trained if v is not None]
    generalization_ratio = None
    if outcome_novel and outcome_trained:
        trained_mean = _mean(outcome_trained)
        novel_mean = _mean(outcome_novel)
        if trained_mean not in (None, 0.0):
            generalization_ratio = novel_mean / trained_mean

    by_probe_history: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        action = r.get("action", "").strip()
        if action:
            by_probe_history[r["probe_id"]][r["history_group"]].append(action)

    divergences = []
    for histories in by_probe_history.values():
        groups = sorted(histories)
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                p = _distribution(histories[groups[i]])
                q = _distribution(histories[groups[j]])
                divergences.append(_js_divergence(p, q))
    matched_history_divergence = _mean(divergences)

    motive_transitions = 0
    motive_rows = [r for r in rows if r.get("motive", "").strip()]
    previous = None
    for r in motive_rows:
        motive = r["motive"].strip()
        if previous is not None and motive != previous:
            motive_transitions += 1
        previous = motive

    interrupted_trials = defaultdict(list)
    for r in rows:
        if _truthy(r.get("interrupted")):
            interrupted_trials[r["trial_id"]].append(r)
    return_after_interrupt = None
    if interrupted_trials:
        recovered = 0
        evaluable = 0
        all_trials = defaultdict(list)
        for r in rows:
            all_trials[r["trial_id"]].append(r)
        for trial_id, interrupts in interrupted_trials.items():
            trial = all_trials[trial_id]
            interrupt_tick = min(int(float(r["tick"])) for r in interrupts)
            before = [r for r in trial if int(float(r["tick"])) < interrupt_tick and r.get("motive", "").strip()]
            after = [r for r in trial if int(float(r["tick"])) > interrupt_tick and r.get("motive", "").strip()]
            if before and after:
                evaluable += 1
                prior_motive = before[-1]["motive"].strip()
                if any(r["motive"].strip() == prior_motive for r in after[:10]):
                    recovered += 1
        if evaluable:
            return_after_interrupt = recovered / evaluable

    return {
        "rows": len(rows),
        "unique_actions": len(action_counts),
        "normalized_action_entropy": round(normalized_entropy, 6),
        "longest_identical_action_run": longest,
        "stereotypy_run_fraction": round(stereotypy, 6),
        "spontaneous_action_rate": None if spontaneous_action_rate is None else round(spontaneous_action_rate, 6),
        "matched_history_action_divergence_js": None if matched_history_divergence is None else round(matched_history_divergence, 6),
        "novel_target_generalization_ratio": None if generalization_ratio is None else round(generalization_ratio, 6),
        "player_intent_inference_accuracy": None if intent_accuracy is None else round(intent_accuracy, 6),
        "delayed_commitment_completion_rate": None if commitment_rate is None else round(commitment_rate, 6),
        "motive_transitions": motive_transitions if motive_rows else None,
        "return_to_prior_motive_after_interrupt": None if return_after_interrupt is None else round(return_after_interrupt, 6),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score Creature behavioral trial logs")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = score(load_rows(args.csv))
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
