---
name: study-status
description: Report where the book stands and recommend the single next action. Use when the user asks what's next, how far along they are, or wants an overview of the study project (e.g. "/study-status", "where am I", "what should I do next", "how much of the book is left").
---

# study-status

The front door to a book-study project. Reads the state files and answers two
questions: **where am I**, and **what's the one thing to do next**. This skill
only reads — it never advances the project itself.

## Steps

1. **Read `progress.md`** and `notes/00-toc-page-map.md`. If either is
   missing, the project hasn't been set up — tell the user to run
   `/plan-book` and stop here.

2. **Glob `notes/`, `quizzes/`, `practice/`, and `reviews/`** to cross-check
   what's actually on disk against what `progress.md` claims. They can
   diverge — a skill interrupted mid-run, or files deleted by hand. Where
   they disagree, trust the files and flag the mismatch; `progress.md` is
   the tracker, not the territory.

3. **Report the state** compactly — a few lines, not a wall of text:
   - Book title and `N of M chapters` with notes done.
   - A short per-stage count: notes / diagrams / quizzed / practiced.
   - Anything half-finished: a chapter with notes but no diagrams, a
     `practice/NN-slug/` folder whose stubs are untouched, a chapter quizzed
     once with known gaps.

4. **Recommend exactly one next action**, with the command to run. Resolve
   competing candidates in this order:
   1. A **blocked or half-finished** item — an untouched practice folder, a
      chapter with notes but no diagrams. Finishing beats starting.
   2. **Review is overdue** — three or more chapters have notes but no
      `Reviewed` date, or the oldest `Reviewed` date is more than two weeks
      old while the book has moved on since. → `/review-book`.
   3. The **next unread chapter** → `/learn-chapter` or the
      `study-chapter` agent.
   4. All chapters done but no synthesis yet → `/synthesize-book`.

   Name the runner-up in one clause so the user can override, but lead with
   a single recommendation rather than a menu.

5. **Don't run the recommended action.** Report, recommend, stop — even if
   the next step seems obvious. The user asked where they stand, not for the
   work to begin.
