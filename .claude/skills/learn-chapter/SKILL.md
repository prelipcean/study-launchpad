---
name: learn-chapter
description: Read a chapter of the current study book from its PDF and turn it into structured notes. Use when the user wants to start, resume, or re-read a chapter (e.g. "/learn-chapter", "/learn-chapter 5", "let's do the next chapter").
---

# learn-chapter

Reads one chapter of the book being studied directly from its PDF and writes
it up as structured notes. This is the "absorb the material" step — it does
not quiz or generate exercises (see `quiz-chapter` and `practice-chapter` for
that).

This skill is written generically (book path, page map, and chapter number
are all inputs/lookups, not hardcoded) so it works for any book dropped into
a project directory. Run `/plan-book` first if `notes/00-toc-page-map.md`
and `progress.md` don't exist yet — this skill depends on both.

## Steps

1. **Determine the chapter number.** If the user passed one as an argument,
   use it. Otherwise open `progress.md` in the project root and pick the
   first chapter whose "Notes" column is still empty.

2. **Look up the page range.** Read `notes/00-toc-page-map.md` for this
   project — it has a table of chapter → PDF page range (already adjusted
   for the offset between printed and PDF page numbers; use the PDF page
   numbers, not the printed ones). If this file is missing, stop and tell
   the user to run `/plan-book` — don't rebuild the page map here. Working
   the offset out properly means verifying it against several chapters, and
   a quick guess made mid-chapter is how you end up writing notes for the
   wrong pages.

3. **Read the chapter.** Use the `Read` tool directly on the PDF with the
   `pages` parameter set to the chapter's PDF range. The Read tool renders
   PDF pages as images Claude can see directly (text, diagrams, code
   listings) — this is the primary path. If a chapter spans more than 20
   pages, make multiple `Read` calls to cover the full range. Only fall back
   to `scripts/ocr_page.py <page_number>` if a specific page renders too
   illegibly to read (e.g. a low-contrast diagram) — it OCRs that one page
   via tesseract.

4. **Write the notes file.** Create `notes/NN-slug.md` (zero-padded chapter
   number, kebab-case title slug) with these sections:
   - **Overview** — 2-4 sentences on what the chapter covers and why it
     matters in the book's overall arc.
   - **Key Concepts** — the chapter's core ideas, each with a short
     definition in your own words (not copied verbatim from the book).
   - **Glossary** — terms introduced in this chapter worth remembering,
     one line each.
   - **Diagrams & Figures** — for any non-trivial diagram or figure, describe
     in words what it shows and why it's drawn that way.
   - **Key Takeaways** — a short bulleted list, the "if you remember nothing
     else" points.

   Keep it tight — this is a study reference, not a transcription. Favor
   clear prose over copying the book's sentences.

5. **Update `progress.md`.** Fill in today's date in the "Notes" column for
   this chapter.

6. **Tell the user** notes are ready, point to the file, and suggest running
   `/quiz-chapter` or `/practice-chapter` next. Don't start quizzing
   automatically — this skill's job ends at notes.
