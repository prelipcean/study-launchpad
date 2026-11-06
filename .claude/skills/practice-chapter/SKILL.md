---
name: practice-chapter
description: Generate small hands-on coding exercises tied to a chapter's concepts, then review the user's attempt. Use when the user wants to practice or code something from a chapter (e.g. "/practice-chapter", "/practice-chapter 5", "give me an exercise for RAG", "review my attempt at chapter 5").
---

# practice-chapter

Turns a chapter's concepts into 1-3 small, runnable exercises, then acts as a
reviewer when the user attempts them. This is deliberately small in scope per
chapter — toy implementations that make a concept concrete, not production
code.

The skill has **two modes**, and step 2 decides which one you're in. Getting
this right matters: the user may invoke this skill days after the exercises
were generated, with a half-finished attempt sitting on disk. Generating
fresh exercises at that point would overwrite their work.

## Steps

1. **Determine the chapter.** If named, use it. Otherwise open `progress.md`
   and pick the most recent chapter with notes done but not yet practiced.

2. **Pick the mode: check whether `practice/NN-slug/` already exists.**
   - **Doesn't exist** → generate mode, continue to step 3.
   - **Exists** → review mode, skip to step 7. Never regenerate over an
     existing folder. If the user explicitly asked for *different* or
     *additional* exercises for a chapter they've already got a folder for,
     add new files alongside the existing ones (next free number) rather
     than rewriting what's there.

### Generate mode

3. **Read that chapter's notes** at `notes/NN-slug.md` (run `/learn-chapter`
   first if missing).

4. **Design 1-3 exercises** directly tied to the chapter's concepts, sized
   to finish in a sitting. Favor exercises that make an abstract idea
   concrete by building a tiny version of it. Examples of the right scope:
   - RAG chapter → implement cosine-similarity retrieval over ~5 hardcoded
     text snippets, no real vector DB.
   - Prompting chapter → write a function that assembles a prompt from a
     template + few-shot examples and enforces a token budget.
   - Tool orchestration / MCP chapter → mock a tool-calling loop against a
     couple of fake tools with a stop condition.

   **Stdlib only.** No external services, no API keys, no pip installs — not
   even numpy. If an exercise seems to need numpy, that's a signal it's too
   big; shrink it (a hand-written dot product over two lists *is* the
   exercise in a vectors chapter). This keeps every exercise runnable on a
   bare Python install, which is the difference between the user practicing
   and the user debugging an environment.

   Default to Python. If the book teaches a different language, use that
   language instead and adapt the file layout and test runner below to its
   conventions.

5. **Write the exercise files** to `practice/NN-slug/`:
   - One `NN_name.py` per exercise with a module docstring explaining the
     task, stubbed function signatures with type hints, and `# TODO`
     markers — not a blank page, but not the solution either. Every stub
     should `raise NotImplementedError` so an unattempted exercise fails
     its test loudly rather than passing vacuously on a `None` return.
   - One `test_NN_name.py` per exercise: plain `assert` statements in
     functions named `test_*`, runnable *without* pytest via an
     `if __name__ == "__main__":` block that calls each test and prints
     pass/fail per case. These tests are the spec — write them so that
     passing them means the concept was actually implemented, not that a
     signature exists. Cover the normal case plus at least one edge case
     the chapter's concept implies (empty input, a tie, a budget exactly
     hit).
   - A `README.md` in that folder: one section per exercise naming the
     concept from the notes it exercises, how to run the tests
     (`python3 test_NN_name.py`), and what "done" looks like.

   Do not write a solutions file. The tests define correctness; a solution
   sitting next to the stub defeats the exercise.

6. **Hand it off and stop.** Tell the user what's in the folder and how to
   run the tests. Do not write the solution, do not fill in the TODOs, and
   do not mark `Practiced` in `progress.md` — nothing has been practiced
   yet. End the skill here.

### Review mode

7. **Read the chapter's notes** (`notes/NN-slug.md`) and everything in
   `practice/NN-slug/` — the exercise stubs, the tests, and the user's
   current code.

8. **Check whether there's actually an attempt.** If the files are still
   untouched stubs (every function still raising `NotImplementedError`),
   don't review — tell the user the exercises are still waiting, remind
   them how to run the tests, and stop without touching `progress.md`.

9. **Run the tests** (`python3 practice/NN-slug/test_NN_name.py` for each)
   and read the actual output. Review against what the tests report, not
   against what the code looks like it should do.

10. **Review the attempt.** Lead with what's right. Then, for each problem,
    name the specific concept from the notes it relates to and explain why
    the code diverges from it — a failing test is the symptom, the concept
    is the diagnosis. Point at the line. Don't rewrite their code wholesale;
    if a fix needs showing, show the smallest possible snippet and let them
    apply it. If a test fails for a reason that's the test's fault rather
    than theirs, say so plainly and fix the test.

11. **Update `progress.md`** — fill in today's date in the "Practiced"
    column, now that a real attempt has been made and reviewed. If the
    attempt is still substantially incomplete (most tests failing, large
    parts unstarted), leave the column empty and say what's left instead;
    the column means "practiced", not "opened".
