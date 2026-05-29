"""
CodeMentor Learning State Tracker

Manages persistent learning state per workspace.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


STATE_FILE = ".codementor/state.json"


@dataclass
class LearningState:
    """Tracks a student's learning progress."""
    student_id: str = "local"
    workspace: str = ""
    concepts_mastered: list[str] = None
    concepts_learning: list[str] = None
    exercises_completed: int = 0
    exercises_failed: int = 0
    streak_days: int = 0
    last_session: Optional[str] = None
    weak_areas: list[str] = None
    strong_areas: list[str] = None

    def __post_init__(self):
        self.concepts_mastered = self.concepts_mastered or []
        self.concepts_learning = self.concepts_learning or []
        self.weak_areas = self.weak_areas or []
        self.strong_areas = self.strong_areas or []

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LearningState":
        return cls(**data)


class LearningStateManager:
    """Manages learning state persistence."""

    def __init__(self, workspace: Optional[str] = None):
        self.workspace = workspace or os.getcwd()
        self.state_file = Path(self.workspace) / STATE_FILE
        self._ensure_directory()

    def _ensure_directory(self):
        """Create .codementor directory if it doesn't exist."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> LearningState:
        """Load state from disk, or return default if none exists."""
        if not self.state_file.exists():
            return LearningState(workspace=self.workspace)

        try:
            with open(self.state_file, "r") as f:
                data = json.load(f)
            return LearningState.from_dict(data)
        except (json.JSONDecodeError, TypeError):
            return LearningState(workspace=self.workspace)

    def save(self, state: LearningState) -> None:
        """Persist state to disk."""
        state.workspace = self.workspace
        state.last_session = datetime.now(timezone.utc).isoformat()

        with open(self.state_file, "w") as f:
            json.dump(state.to_dict(), f, indent=2)

    def update_exercise(self, success: bool, concepts: list[str]) -> LearningState:
        """Update state after an exercise attempt."""
        state = self.load()

        if success:
            state.exercises_completed += 1
            for concept in concepts:
                if concept not in state.concepts_mastered:
                    state.concepts_mastered.append(concept)
                if concept in state.concepts_learning:
                    state.concepts_learning.remove(concept)
                if concept in state.weak_areas:
                    state.weak_areas.remove(concept)
                if concept not in state.strong_areas:
                    state.strong_areas.append(concept)
        else:
            state.exercises_failed += 1
            for concept in concepts:
                if concept not in state.concepts_learning:
                    state.concepts_learning.append(concept)
                if concept not in state.weak_areas:
                    state.weak_areas.append(concept)

        self.save(state)
        return state

    def start_learning_concept(self, concept: str) -> LearningState:
        """Mark a concept as currently being learned."""
        state = self.load()

        if concept not in state.concepts_learning:
            state.concepts_learning.append(concept)

        if concept in state.strong_areas:
            state.strong_areas.remove(concept)

        self.save(state)
        return state

    def reset(self) -> None:
        """Reset all progress."""
        self.save(LearningState(workspace=self.workspace))

    def get_summary(self) -> str:
        """Generate a text summary of current progress."""
        state = self.load()

        lines = [
            "📊 Your Learning Progress",
            "=" * 30,
            f"Exercises completed: {state.exercises_completed}",
            f"Exercises with hints: {state.exercises_failed}",
            f"Streak: {state.streak_days} days",
            "",
        ]

        if state.concepts_mastered:
            lines.append("✅ Mastered concepts:")
            for c in state.concepts_mastered[:5]:
                lines.append(f"   • {c}")
            if len(state.concepts_mastered) > 5:
                lines.append(f"   ... and {len(state.concepts_mastered) - 5} more")

        if state.concepts_learning:
            lines.append("\n📚 Currently learning:")
            for c in state.concepts_learning:
                lines.append(f"   • {c}")

        if state.weak_areas:
            lines.append("\n💪 Areas to practice:")
            for c in state.weak_areas[:3]:
                lines.append(f"   • {c}")

        return "\n".join(lines)
