from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any

from .model import LearningEpisode


@dataclass
class TreeNode:
    prediction: float
    feature: str | None = None
    threshold: float | None = None
    category: str | None = None
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None

    def predict(self, features: dict[str, Any]) -> float:
        if self.feature is None or self.left is None or self.right is None:
            return self.prediction
        value = features.get(self.feature)
        if self.category is not None:
            go_left = str(value) == self.category
        elif isinstance(value, (int, float)) and self.threshold is not None:
            go_left = float(value) <= self.threshold
        else:
            return self.prediction
        return (self.left if go_left else self.right).predict(features)

    def to_dict(self) -> dict[str, Any]:
        return {
            "prediction": self.prediction,
            "feature": self.feature,
            "threshold": self.threshold,
            "category": self.category,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TreeNode":
        node = cls(
            prediction=float(data["prediction"]),
            feature=data.get("feature"),
            threshold=data.get("threshold"),
            category=data.get("category"),
        )
        if data.get("left"):
            node.left = cls.from_dict(data["left"])
        if data.get("right"):
            node.right = cls.from_dict(data["right"])
        return node


class DecisionTreeOpinion:
    """Small online regression tree used as the reconstructed generalized opinion.

    Black & White's recovered structures tie decision trees to desire/action pairs and
    attach learning episodes to attribute tests. The exact induction routine is not yet
    recovered, so this implementation deliberately isolates the inferred algorithm.
    """

    def __init__(self, max_depth: int = 4, min_samples: int = 3, max_episodes: int = 256):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.max_episodes = max_episodes
        self.episodes: list[LearningEpisode] = []
        self.root = TreeNode(0.0)

    def add(self, features: dict[str, Any], reward: float) -> None:
        self.episodes.append(LearningEpisode(dict(features), float(reward)))
        if len(self.episodes) > self.max_episodes:
            self.episodes = self.episodes[-self.max_episodes :]
        self.root = self._build(self.episodes, 0)

    def predict(self, features: dict[str, Any]) -> float:
        return self.root.predict(features)

    @staticmethod
    def _sse(items: list[LearningEpisode]) -> float:
        if not items:
            return 0.0
        m = mean(e.reward for e in items)
        return sum((e.reward - m) ** 2 for e in items)

    def _build(self, items: list[LearningEpisode], depth: int) -> TreeNode:
        pred = mean(e.reward for e in items) if items else 0.0
        node = TreeNode(pred)
        if depth >= self.max_depth or len(items) < self.min_samples * 2:
            return node
        base = self._sse(items)
        best_gain = 0.0
        best: tuple[str, float | None, str | None, list[LearningEpisode], list[LearningEpisode]] | None = None
        features = sorted({k for e in items for k in e.features})
        for name in features:
            values = [e.features.get(name) for e in items if name in e.features]
            numeric = [float(v) for v in values if isinstance(v, (int, float))]
            if len(numeric) == len(values) and len(set(numeric)) > 1:
                unique = sorted(set(numeric))
                if len(unique) > 16:
                    step = max(1, len(unique) // 16)
                    unique = unique[::step]
                thresholds = [(a + b) / 2.0 for a, b in zip(unique, unique[1:])]
                for t in thresholds:
                    left = [e for e in items if isinstance(e.features.get(name), (int, float)) and float(e.features[name]) <= t]
                    right = [e for e in items if e not in left]
                    if len(left) < self.min_samples or len(right) < self.min_samples:
                        continue
                    gain = base - self._sse(left) - self._sse(right)
                    if gain > best_gain:
                        best_gain = gain
                        best = (name, t, None, left, right)
            else:
                for cat in sorted({str(v) for v in values}):
                    left = [e for e in items if str(e.features.get(name)) == cat]
                    right = [e for e in items if e not in left]
                    if len(left) < self.min_samples or len(right) < self.min_samples:
                        continue
                    gain = base - self._sse(left) - self._sse(right)
                    if gain > best_gain:
                        best_gain = gain
                        best = (name, None, cat, left, right)
        if best is None or best_gain <= 1e-9:
            return node
        name, threshold, category, left, right = best
        node.feature = name
        node.threshold = threshold
        node.category = category
        node.left = self._build(left, depth + 1)
        node.right = self._build(right, depth + 1)
        return node

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_depth": self.max_depth,
            "min_samples": self.min_samples,
            "max_episodes": self.max_episodes,
            "episodes": [{"features": e.features, "reward": e.reward} for e in self.episodes],
            "root": self.root.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DecisionTreeOpinion":
        obj = cls(int(data["max_depth"]), int(data["min_samples"]), int(data["max_episodes"]))
        obj.episodes = [LearningEpisode(dict(e["features"]), float(e["reward"])) for e in data.get("episodes", [])]
        obj.root = TreeNode.from_dict(data.get("root", {"prediction": 0.0}))
        return obj
