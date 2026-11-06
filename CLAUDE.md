# StudyLaunchpad — working on the toolkit

This repo is a **reusable toolkit**, not a study project. It holds skills, an
agent, and two helper scripts that get copied into a separate directory per
book (see `init.sh`). Nothing here is specific to any one book.

## The two rules that matter

**1. Never commit book content.** Notes, diagrams, quiz transcripts, reviews,
practice folders, `progress.md`, and PDFs belong to the project built *with*
this toolkit. `.gitignore` covers them. If you find yourself writing a
`notes/` file in this repo, you're in the wrong directory.

**2. Nothing is hardcoded per book.** No title, author, chapter count, page
number, or filename appears in any skill. `plan-book` discovers all of it from
the PDF and writes it to `notes/00-toc-page-map.md`; every other skill looks
it up there. A chapter count in a skill file is a bug.

## Shared contract between skills

Skills don't call each other — they coordinate through two files in the study
project, and both formats are load-bearing:

- **`notes/00-toc-page-map.md`** — chapter → PDF page range. Written by
  `plan-book` following `.claude/skills/plan-book/references/page-map-template.md`.
  Change the template and the table columns, not individual skills' parsing.
- **`progress.md`** — one row per chapter, columns `Notes`, `Diagrams`,
  `Quizzed`, `Practiced`, `Reviewed`, each a `YYYY-MM-DD` completion date.
  Column names are an API; renaming one breaks every skill that reads it.
  `Reviewed` is the exception to "fill once" — `review-book` overwrites it as
  a last-seen date.

State is always **re-read from these files**, never carried in conversation.
That's what makes an interrupted batch resumable.

- **`logs/study-chapter.log`** — supplementary, not load-bearing. One line
  per chapter the `study-chapter` agent processes (timestamp, chapter,
  per-skill outcome, elapsed time). Nothing reads this file back to decide
  behavior — `progress.md` stays the only source of truth for what's done.
  It exists purely so a long batch run leaves evidence of what happened and
  roughly how long it took, instead of only the conversation transcript.

## Conventions when editing skills

- **PDF reading** goes through the `Read` tool with `pages` — it renders pages
  as images Claude sees directly. Max 20 pages per call, so a longer chapter
  needs several. `scripts/ocr_page.py` is a single-page fallback for an
  illegible page, not a reading path.
- **Each phase stays a separate, user-triggered skill.** Reading, diagramming,
  quizzing, and practicing are deliberately not one pipeline — the user sets
  the pace. The `study-chapter` agent bundles notes+diagrams only; don't add
  quiz or practice to it.
- **Interactive skills must actually be interactive.** `quiz-chapter` and
  `review-book` ask one question and wait. Printing a question list defeats
  them entirely.
- **Practice exercises are stdlib-only** — no numpy, no API keys, no network.
  An exercise that needs a dependency is too big; shrink it.
- **A skill writes the files its own steps name, and stops there.** Skills end
  by *suggesting* the next command, never by running it.
- **A loop needs a failure policy, not just a stopping condition.**
  `study-chapter`'s batch mode retries a failed step once, then logs and
  skips that chapter rather than letting one bad chapter block the rest —
  but stops the whole batch if two chapters fail in a row, since that's a
  signal something structural broke, not noise from one unlucky chapter.
  Any future loop (another batch-style skill, a multi-step skill) should
  have an equally explicit answer to "what happens when a step fails
  twice," not just "what happens when the work runs out."

## Agent tool permissions

`Skill` loads a skill's instructions into the calling agent's context; the
agent then carries them out with **its own** tools. So any agent invoking
`learn-chapter` or `diagram-chapter` needs `Write` and `Edit` — without them
it reads the chapter and silently has no way to save it. This is why
`.claude/agents/study-chapter.md` lists `Skill, Read, Write, Edit, Glob, Bash`.

## Verifying a change

There's no test suite. The scripts are checkable directly:

```sh
python3 -c "import fitz; d=fitz.open(); d.new_page().insert_text((72,120),'Chapter 7',fontsize=28); d.save('/tmp/s.pdf')"
python3 scripts/page_count.py /tmp/s.pdf   # -> 1
python3 scripts/ocr_page.py 1 /tmp/s.pdf   # -> Chapter 7
./init.sh /tmp/probe /tmp/s.pdf && ./init.sh /tmp/probe /tmp/s.pdf  # 2nd run: all "skip"
```

Skill changes are prose and can only really be verified by running the skill
against a real book.
