"""
Gap-Fill Exercise Generator

Creates code exercises with single blanks and progressive hints.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GapType(Enum):
    """Types of gaps that can be created."""
    FUNCTION_BODY = "function_body"
    VARIABLE_NAME = "variable_name"
    OPERATOR = "operator"
    PARAMETER = "parameter"
    IMPORT = "import"
    CONTROL_FLOW = "control_flow"
    RETURN_VALUE = "return_value"
    CONDITION = "condition"
    LIST_COMPREHENSION = "list_comprehension"


@dataclass
class GapExercise:
    """A single gap-fill exercise."""
    original_code: str
    gap_code: str
    solution: str
    gap_type: GapType
    hint_1: str
    hint_2: str
    hint_3: str
    concept: str
    explanation: str


class GapFillGenerator:
    """Generates gap-fill exercises from code."""

    # Patterns for different gap types
    PATTERNS = {
        GapType.OPERATOR: [
            (r'(\w+)\s+(\w+)\s*=\s*\d+\s*>\s*\d+', r'\1 ___ \2 = 5 > 3'),
            (r'if\s+.*\s*([!=<>]+)\s*.*:', r'if x ___ 5:'),
            (r'for\s+\w+\s+in\s+range\(\s*\d+\s*,\s*\d+\s*\):', r'for i in ___(1, 10):'),
        ],
        GapType.FUNCTION_BODY: [
            (r'def\s+\w+\([^)]*\):\s*\n\s*""".*?"""', 'def func():\n    """Docstring"""\n    ___'),
            (r'def\s+\w+\([^)]*\):\s*\n(\s*)return\s+\w+', r'def func():\n\1___'),
        ],
        GapType.PARAMETER: [
            (r'def\s+\w+\(([^)]*)\):', r'def func(___):'),
            (r'def\s+\w+\([^)]*\):\s*\n\s*""".*?"""\s*\n(\s*)(\w+)', r'def func():\n    """Docstring"""\n    \1___'),
        ],
        GapType.RETURN_VALUE: [
            (r'return\s+(\w+)', r'return ___'),
            (r'return\s+(\w+\s*[\+\-\*/]\s*\w+)', r'return ___'),
        ],
        GapType.CONDITION: [
            (r'if\s+(.+):', r'if ___ :'),
            (r'elif\s+(.+):', r'elif ___ :'),
            (r'while\s+(.+):', r'while ___ :'),
        ],
        GapType.VARIABLE_NAME: [
            (r'(def\s+\w+\([^)]*\):\s*\n\s*)(\w+)(\s*=)', r'\1___\3'),
        ],
        GapType.LIST_COMPREHENSION: [
            (r'\[(\w+)\s+for\s+(\w+)\s+in\s+(\w+)\s+if\s+(.+)\]', r'[___ for x in items if condition]'),
        ],
    }

    # Hints by gap type
    HINTS = {
        GapType.OPERATOR: [
            "Think about what operation combines or compares values",
            "It's the same as: 3 + 5 = 8 or 10 > 5",
            "The operator is one of: +, -, *, /, ==, !=, >, <, >=, <="
        ],
        GapType.FUNCTION_BODY: [
            "Think about what this function should return",
            "The function needs to compute or return something",
            "Look at the function name and parameters for clues"
        ],
        GapType.PARAMETER: [
            "This parameter receives data from outside",
            "What data does the function need to work with?",
            "The parameter name should describe what it holds"
        ],
        GapType.RETURN_VALUE: [
            "What should this function give back to the caller?",
            "The return value represents the function's result",
            "Think about what x + y produces"
        ],
        GapType.CONDITION: [
            "This condition determines whether the code runs",
            "Think about what makes this condition true or false",
            "Try substituting: x > 5 or len(items) > 0"
        ],
        GapType.VARIABLE_NAME: [
            "This is a variable that will store something",
            "The name should describe what it holds",
            "Common names: result, total, count, item, value"
        ],
        GapType.LIST_COMPREHENSION: [
            "This creates a new list by transforming each item",
            "The pattern is: [expression for item in iterable]",
            "Fill in what to do with each item"
        ],
        GapType.IMPORT: [
            "This module provides the functionality you need",
            "Think about what library handles this task",
            "Common imports: os, sys, json, requests, datetime"
        ],
        GapType.CONTROL_FLOW: [
            "This keyword controls which code runs",
            "Think about: if/else, for, while, try/except",
            "The keyword starts a block of code"
        ],
    }

    def generate_from_code(self, code: str, concept: Optional[str] = None) -> Optional[GapExercise]:
        """Generate a gap-fill exercise from code."""
        gap_type = self._detect_gap_type(code)
        if not gap_type:
            return None

        pattern = self.PATTERNS.get(gap_type, [])
        for regex, replacement in pattern:
            if re.search(regex, code):
                gap_code = re.sub(regex, replacement, code, count=1)
                solution = self._extract_solution(code, regex)

                return GapExercise(
                    original_code=code,
                    gap_code=gap_code,
                    solution=solution,
                    gap_type=gap_type,
                    hint_1=self.HINTS[gap_type][0],
                    hint_2=self.HINTS[gap_type][1],
                    hint_3=self.HINTS[gap_type][2],
                    concept=concept or gap_type.value,
                    explanation=self._explain_gap(gap_type)
                )

        return None

    def _detect_gap_type(self, code: str) -> Optional[GapType]:
        """Detect what type of gap would work best for this code."""
        if 'def ' in code and ':' in code:
            if 'return ' in code:
                return GapType.RETURN_VALUE
            return GapType.FUNCTION_BODY
        if 'if ' in code or 'elif ' in code or 'while ' in code:
            return GapType.CONDITION
        if 'for ' in code and 'in ' in code:
            return GapType.OPERATOR
        if '[' in code and ' for ' in code and ' in ' in code:
            return GapType.LIST_COMPREHENSION
        if 'import ' in code or 'from ' in code:
            return GapType.IMPORT
        if '+' in code or '-' in code or '*' in code or '/' in code:
            return GapType.OPERATOR
        return GapType.VARIABLE_NAME

    def _extract_solution(self, code: str, regex: str) -> str:
        """Extract what should go in the blank."""
        match = re.search(regex, code)
        if not match:
            return "???"

        # Return the first capturing group content
        groups = match.groups()
        if groups:
            return groups[0].strip()
        return "???"

    def _explain_gap(self, gap_type: GapType) -> str:
        """Explain what this type of gap teaches."""
        explanations = {
            GapType.OPERATOR: "Understanding operators is fundamental— they're how you manipulate data",
            GapType.FUNCTION_BODY: "Functions are building blocks— learn to write them correctly",
            GapType.PARAMETER: "Parameters are how functions receive input",
            GapType.RETURN_VALUE: "Return values are how functions give output",
            GapType.CONDITION: "Conditions control what your code does",
            GapType.VARIABLE_NAME: "Good variable names make code readable",
            GapType.LIST_COMPREHENSION: "List comprehensions are Pythonic and concise",
            GapType.IMPORT: "Imports connect your code to libraries",
            GapType.CONTROL_FLOW: "Control flow determines program structure",
        }
        return explanations.get(gap_type, "Practice makes perfect")


def format_exercise(exercise: GapExercise) -> str:
    """Format a gap exercise for display."""
    lines = [
        f"📝 Gap-Fill Exercise",
        f"   Concept: {exercise.concept}",
        "=" * 40,
        "",
        "Fill in the blank (marked with ___):",
        "",
        "```python",
        exercise.gap_code,
        "```",
        "",
        "Type your answer, or say 'hint' for help.",
        "",
        f"(Solution: {exercise.solution})" if False else "",  # Hidden
    ]
    return "\n".join(filter(None, lines))
