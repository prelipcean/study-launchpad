---
name: diagram-chapter
description: Turn a chapter's concepts into Mermaid diagrams saved alongside the notes. Use when the user wants a visual/diagram for a chapter (e.g. "/diagram-chapter", "/diagram-chapter 5", "draw the RAG flow", "make a diagram for this").
---

# diagram-chapter

Produces Mermaid diagrams for a chapter that's already been read, saved as a
companion markdown file next to that chapter's notes. This is a visual aid,
not a replacement for the notes — only diagram concepts where a picture
genuinely clarifies something a paragraph doesn't (a flow, a loop, a
hierarchy, a decision boundary). Skip concepts that are just lists or
definitions; those don't need a diagram.

## Steps

1. **Determine the chapter.** If the user named one, use it. Otherwise open
   `progress.md` and pick the most recent chapter with notes done.

2. **Read that chapter's notes** at `notes/NN-slug.md` (run `/learn-chapter`
   first if missing — don't diagram from the raw PDF, work from the notes
   so diagrams stay consistent with what's already been written up).

3. **Decide which concepts deserve a diagram.** Good candidates:
   - A described **process or loop** (e.g. an agent's decide→act→observe
     cycle) → flowchart, with the loop-back edge drawn explicitly.
   - A **request/response flow across components** (e.g. user → app → tool
     → model → response) → flowchart or sequence diagram, whichever reads
     clearer for that exact interaction.
   - A **nested/hierarchical relationship** (e.g. AI ⊃ ML ⊃ DL ⊃ GenAI ⊃
     LLM) → a graph with subgraphs, or a simple top-down tree.
   - A **comparison or boundary** (e.g. one-shot vs. agent loop, RAG vs.
     tool use vs. agent) → two small diagrams side by side beat one
     cluttered one.
   If the chapter's own "Diagrams & Figures" notes section already
   describes a book figure, prefer re-rendering that one in Mermaid (it's
   proven useful) over inventing a new one for the same idea. Also feel
   free to add new diagrams for concepts the book explained only in prose
   where a picture would help. If nothing in the chapter earns a diagram,
   say so plainly instead of forcing one — not every chapter needs this.

4. **Write good Mermaid, not just correct Mermaid.** Keep each diagram
   small enough to read at a glance (roughly 5-10 nodes); split a sprawling
   process into two linked diagrams rather than one dense one. Label edges
   with the actual verb/decision ("validates", "decides next step"), not
   just arrows. Use the diagram type that matches the shape of the idea —
   `flowchart` for processes/loops, `sequenceDiagram` for
   request/response across named actors, `graph`/subgraphs for
   hierarchies and boundaries. If useful, the `artifact-diagramming` skill
   has deeper guidance on drawing diagrams that show the real mechanism
   instead of decoration — consult it for non-obvious layout or clarity
   problems.

5. **Save the file** at `notes/NN-slug-diagrams.md`, one Mermaid fenced
   block per diagram, each preceded by a one-line caption explaining what
   it shows and why it's drawn that way (same spirit as the notes file's
   "Diagrams & Figures" section). These render natively in VS Code,
   Obsidian, GitHub, and most Markdown viewers — no publishing step needed.

6. **Update `progress.md`** — fill in today's date in the "Diagrams" column
   for this chapter. If nothing in the chapter earned a diagram (step 3),
   still mark it done — there's no separate file to point to, but the
   chapter has been considered.

7. **Tell the user** what was created and how many diagrams, and name a
   viewer if they don't already have one open (e.g. "open it in VS Code or
   any Mermaid-aware Markdown viewer to see them rendered").
