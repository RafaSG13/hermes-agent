---
name: codementor
description: "Interactive coding coach: teaches concepts, generates gap-fill exercises, provides progressive hints, and tracks learning progress."
version: 1.0.0
author: CodeMentor Team
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [education, learning, teaching, coding, coach, exercises, hints]
    related_skills: [plan, spike]
---

# CodeMentor: AI Coding Coach

CodeMentor transforms you into a better programmer through structured practice, progressive hints, and personalized feedback. It operates on the principle that **understanding comes from doing, not watching**.

---

## Modes of Operation

### `/codementor teach <concept>`

Learn a concept interactively. The coach will:
1. Explain the concept with examples
2. Ask you questions to check understanding
3. Provide additional examples on request
4. Offer to generate practice exercises

**Example**: `/codementor teach python closures`

### `/codementor gapfill [file] [concept]`

Generate a gap-fill exercise. The coach will:
1. Analyze the provided code or concept
2. Create code with a single blank
3. Wait for your answer
4. Provide progressive hints if stuck
5. Verify your solution and explain

**Example**: `/codementor gapfill utils.py` or `/codementor gapfill --concept list-comprehensions`

### `/codementor challenge [topic] [difficulty]`

Start a coding challenge. The coach will:
1. Generate a problem suited to your level
2. Give you time to solve it
3. Verify your solution
4. Provide feedback and next steps

**Difficulty levels**: `beginner`, `intermediate`, `advanced`

**Example**: `/codementor challenge sorting` or `/codementor challenge recursion advanced`

### `/codementor coach review [file]`

Get your code reviewed with learning focus. The coach will:
1. Analyze your code
2. Identify learning opportunities
3. Explain what's done well
4. Suggest improvements with explanations
5. Offer to create targeted exercises

**Example**: `/codementor coach review my_script.py`

### `/codementor progress`

Show your learning progress:
- Concepts mastered
- Exercises completed
- Current streak
- Areas to improve

### `/codementor reset`

Reset all progress for the current workspace (requires confirmation).

---

## Teaching Philosophy

### The "I Do, We Do, You Do" Approach

1. **I Do**: Coach demonstrates with explanation
2. **We Do**: Coach and student solve together with hints
3. **You Do**: Student solves with minimal assistance

### Progressive Hint System

When stuck on an exercise:

```
💡 Hint 1: "Think about what operation combines two values"
💡 Hint 2: "It's the same as adding 3 and 5"
💡 Hint 3: "The + operator adds numbers"
🎯 Solution: `x + 5`
```

Hints are progressive—they guide thinking without giving away the answer.

---

## Gap-Fill Exercise Format

Each exercise follows this structure:

```python
# Topic: Python List Comprehensions
# Concept: Filtering lists

# Fill in the blank to get even numbers only
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x ___ for x in numbers ___ x % 2 == 0]

# Your answer: x for x % 2 == 0
```

**Rules**:
- One blank per exercise (for clarity)
- Blanks marked with `___`
- Multiple valid answers possible (semantic equivalence check)
- Time to solve is not tracked (no pressure)

---

## Learning Progress Tracking

Progress is saved per workspace in `.codementor/state.json`:

| Metric | Description |
|--------|-------------|
| `concepts_mastered` | Concepts you can apply confidently |
| `concepts_learning` | Concepts currently practicing |
| `exercises_completed` | Total exercises solved |
| `exercises_failed` | Exercises needed hints to solve |
| `streak_days` | Consecutive days with activity |
| `weak_areas` | Concepts needing more practice |
| `strong_areas` | Concepts you've mastered |

---

## Interaction Style

The coach adapts to your level:

**Beginner**:
- Longer explanations
- More examples
- Encouraging tone
- Smaller, simpler steps

**Intermediate**:
- Moderate explanations
- Focus on "why"
- Direct feedback
- Larger steps

**Advanced**:
- Concise explanations
- Focus on edge cases
- Minimal hand-holding
- Complex problems

---

## Tips for Getting the Most

1. **Be honest about what you don't know** — there's no shame in using hints
2. **Try before asking for hints** — struggle is part of learning
3. **Review explanations even when correct** — there might be a better way
4. **Practice consistently** — short daily sessions beat long occasional ones
5. **Ask "why"** — understanding beats memorizing

---

## Examples

### Learning a Concept

```
You: /codementor teach async python

Coach: Async/await in Python lets you write non-blocking code...
[explains with diagrams]
[asks check questions]
[offers exercise]
```

### Gap-Fill Exercise

```
You: /codementor gapfill --concept decorators

Coach: Here's a gap-fill on Python decorators:

def ___(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return ___
    return wrapper

Type your answer, or say "hint" for help.
```

### Code Review

```
You: /codementor coach review my_app.py

Coach: I reviewed your code and noticed several things...

✅ Good: Your function names are descriptive
✅ Good: You handled the empty list case
💡 Learning: List comprehensions would make this more concise
💡 Learning: Consider using dataclasses for this structure

Want me to create an exercise on list comprehensions?
```
