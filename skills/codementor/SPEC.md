# CodeMentor - AI Coding Coach Agent

## Concept

CodeMentor transforms Hermes into an interactive coding tutor that doesn't just write code for you—it **teaches you to write it yourself**. The agent provides progressive hints, identifies knowledge gaps, generates fill-in-the-blank exercises, and tracks your learning journey across sessions.

Unlike traditional coding assistants that complete tasks for you, CodeMentor operates on the principle of **"I do, we do, you do"**—gradually reducing assistance as the student gains proficiency.

---

## Philosophy

### Core Teaching Principles

1. **Scaffolded Learning**: Provide just enough help to keep the student in their "zone of proximal development"
2. **Concept Before Code**: Explain *why* before *how*
3. **Active Recall**: Generate exercises that force the student to retrieve knowledge
4. **Progressive Disclosure**: Start simple, add complexity incrementally
5. **Failure as Learning**: Treat mistakes as opportunities, not setbacks

### Teaching Modes

| Mode | Purpose | Student Agency |
|------|---------|---------------|
| `gapfill` | Complete partially-written code | High |
| `challenge` | Solve problems with verification | High |
| `teach` | Explain concepts interactively | Medium |
| `coach` | Review and guide real code | Medium |
| `explain` | Deep dive into "why" | Low |

---

## Architecture

```
codementor/
├── SKILL.md              # Main skill definition
├── learning_state.py     # Tracks student progress
├── exercises/
│   └── gaps/
│       └── generator.py  # Gap-fill exercise generator
├── progress/
│   └── tracker.py        # JSON-based progress persistence
└── storage/
    └── state.json        # Per-project learning state
```

---

## Learning State

Persisted per workspace in `.codementor/state.json`:

```json
{
  "student_id": "local",
  "workspace": "/path/to/project",
  "concepts_mastered": ["python-closures", "async-await"],
  "concepts_learning": ["python-decorators"],
  "exercises_completed": 15,
  "exercises_failed": 3,
  "streak_days": 7,
  "last_session": "2026-05-29T10:30:00Z",
  "weak_areas": ["recursion", "list-comprehensions"],
  "strong_areas": ["functions", "classes"]
}
```

---

## GapFill Mode (MVP)

### How It Works

1. **Analyze** target code or concept
2. **Generate** code with intentional gaps (single blank per exercise)
3. **Present** with progressive hints (hint 1 → hint 2 → solution)
4. **Verify** student's answer
5. **Track** success/failure for concept

### Gap Types

| Type | Example | Purpose |
|------|---------|---------|
| Function body | `def add(a, b): ___` | Core logic |
| Variable name | `___, age = 25` | Naming conventions |
| Operator | `x ___ 5 > 10` | Syntax knowledge |
| Parameter | `def greet(___):` | API comprehension |
| Import | `import ___` | Module knowledge |
| Control flow | `if x > 0: ___` | Logic structures |

### Hint System

```
Hint 1: "Think about what operation combines two numbers"
Hint 2: "It's the same as 3 + 5"
Hint 3: "The answer is ___" (solution shown)
```

---

## Challenge Mode

### How It Works

1. **Assess** student's current level
2. **Generate** problem matched to skill level
3. **Student** writes solution
4. **Verify** correctness (exact match + semantic equivalence)
5. **Feedback** with explanation
6. **Progression** to harder/easier problems

### Problem Types

- **Completion**: Complete the function
- **Debug**: Find and fix the bug
- **Optimize**: Make it more efficient
- **Refactor**: Improve structure without changing behavior
- **Explain**: Write the documentation

---

## Coach Mode

### How It Works

1. **Review** student's code (real project or exercise)
2. **Identify** patterns (good and bad)
3. **Suggest** improvements with explanations
4. **Create** targeted exercises for weak areas

### Code Review Focus Areas

- **Clarity**: Can you explain what this does?
- **Correctness**: Does it handle edge cases?
- **Efficiency**: Any performance issues?
- **Style**: Does it follow conventions?
- **Learning**: What concepts does it demonstrate?

---

## Command Interface

```
/codementor teach <concept>     # Learn about a concept
/codementor gapfill <file>     # Generate gap-fill from file
/codementor challenge <topic>  # Start a challenge
/codementor coach review <file> # Review your code
/codementor progress            # Show learning progress
/codementor reset               # Reset progress for workspace
```

---

## Integration Points

### Hermes Personas

Reuse existing personality system:
- `teacher` - Patient, explains step-by-step
- `kawaii` - Encouraging, uses positive reinforcement
- `concise` - Direct hints, less explanation

### Skills Hub

- Bundled skill (installed by default)
- Activated via `/codementor` or natural language

### Memory System

- Persist learning state across sessions
- Build concept dependency graph

---

## Future Enhancements

1. **Spaced Repetition**: Review concepts at optimal intervals
2. **Adaptive Difficulty**: ML-based problem generation
3. **Collaborative Learning**: Multi-student sessions
4. **Video Explanations**: AI-generated video walkthroughs
5. **Assessment Tests**: Formal quizzes with certification

---

## Success Metrics

- Student exercises completed
- Concepts mastered vs attempted
- Time to complete similar exercises (decreasing = learning)
- Student-reported confidence levels
- Code quality improvement in coached projects
