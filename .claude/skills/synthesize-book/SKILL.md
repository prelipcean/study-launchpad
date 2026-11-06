---
name: synthesize-book
description: Tie a finished (or mostly finished) book together — the through-line across chapters, a concept map, and one capstone project spec. Use at the end of a book, or when the user wants the big picture rather than another chapter (e.g. "/synthesize-book", "how does the whole book fit together", "give me a capstone project").
---

# synthesize-book

Per-chapter notes answer "what did chapter 7 say". They can't answer "what
did this book argue, and what can I now build". This skill works across every
chapter's notes at once to produce that, plus a capstone spec big enough to
need several chapters working together.

Run at the end of a book. It works on a partial book too (useful at the end
of a Part) — just scope every claim to the chapters that actually have notes
and say so.

## Steps

1. **Read `progress.md`** and `notes/00-toc-page-map.md`. If fewer than
   about half the chapters have notes, say the book isn't far enough along
   for synthesis to be worth much and offer to scope it to a completed Part
   instead — then do that if the user agrees, rather than refusing outright.

2. **Read every chapter's notes** (`notes/NN-*.md`, excluding the page map
   and the `-diagrams.md` companions). This is the one skill that needs the
   whole set in view at once — don't sample a few and extrapolate, since the
   through-line is exactly what's invisible from any single chapter.

3. **Write `notes/99-synthesis.md`** with these sections:
   - **The Through-Line** — the book's actual argument in a few paragraphs,
     following how it's built across the Parts. Not a chapter-by-chapter
     recap; the recap is what the notes already are. Where the book's
     structure makes an argument of its own (a concept deliberately deferred
     until the reader has the groundwork), say so.
   - **Concept Map** — one Mermaid `graph` showing how the book's major
     concepts depend on each other, with chapter numbers on the nodes
     (`Retrieval<br/>ch. 4`). Dependency edges, not a table of contents in
     graph form: an edge means "you can't understand this without that".
     Keep it legible — group into subgraphs per Part if it exceeds ~15
     nodes.
   - **Threads Across Chapters** — 3-5 ideas the book returns to repeatedly
     under different names, each with the chapters where it surfaces. These
     are usually the real takeaways and are structurally invisible in
     per-chapter notes.
   - **Open Questions** — what the book left unresolved, assumed, or dated
     (especially where a fast-moving field has moved since publication).
     Be specific; "the field evolves" is not a finding.
   - **If You Remember Five Things** — the whole book compressed to five
     bullets.

4. **Write the capstone spec** to `practice/capstone/README.md`: one project
   that forces at least four chapters' concepts to work together, sized at a
   few sittings rather than a few weeks. Include what to build, the concepts
   it exercises with their chapter numbers, a suggested build order of
   milestones that each run on their own, and how to tell it works. Same
   constraints as `practice-chapter`: stdlib only, no API keys, no external
   services.

   **Spec only — write no code.** Not even scaffolding or stubs. The point
   of a capstone is an empty directory and a clear target; handing over a
   skeleton removes the design work that makes it worth doing.

5. **Tell the user** what was written and point to both files. Suggest
   `/review-book` if any chapter still has no `Reviewed` date — synthesis
   reads well but doesn't test retention.
