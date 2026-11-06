---
name: plan-book
description: Bootstrap a new book-study project from a PDF before any chapter work starts — builds the chapter/page map, the progress tracker, project folders, and the OCR fallback script. Use once per book, at the very start (e.g. "/plan-book", "set up this book for studying", "plan out this PDF before we start").
---

# plan-book

One-time setup skill that turns a bare book PDF into a ready-to-study
project: the folder structure, the chapter→page map, the OCR fallback
script, and an initialized progress tracker. Run this once, before the
first `/learn-chapter`. Everything here is book-agnostic — no chapter
count, title, or page numbers are assumed; they're all discovered from the
PDF itself, so this skill works the same way for any book dropped into a
project directory.

## Steps

1. **Locate the PDF.** If the user named a path, use it. Otherwise look for
   a single PDF file in the project root. If there's more than one or
   none, ask the user which file to use rather than guessing.

2. **Create the project folders** (if missing): `notes/`, `quizzes/`,
   `practice/`, `reviews/`, `scripts/`.

3. **Check the helper scripts** are present: `scripts/page_count.py` (used
   in step 6) and `scripts/ocr_page.py` (the fallback for when a rendered
   PDF page is too illegible to read directly — low-contrast diagrams,
   scanned text). Both ship with this toolkit and are copied in alongside
   `.claude/`, so they should already be there. If either is missing, tell
   the user to copy it from the toolkit rather than writing a replacement
   from scratch — a hand-rolled version will drift from what the other
   skills expect. Don't test-run `ocr_page.py` here; chapter reading goes
   through the `Read` tool and most books never need it.

4. **Find the Table of Contents and build the chapter list.** Read the
   PDF's front matter in batches of up to 20 pages via the `Read` tool
   until you've located and fully captured the Table of Contents: every
   chapter's title and its *printed* page number (and Part/section
   groupings, if the book has them). Also note the book's title, author,
   and ISBN if shown on the title/copyright pages — useful for the page
   map's header, not required.

5. **Determine the printed-page → PDF-page offset.** Printed page numbers
   (what's shown in the book's running header/footer) and PDF page indices
   (what the `Read` tool's `pages` parameter actually addresses) usually
   differ by a constant offset — but front matter (roman numerals) and the
   main body (arabic numerals) often have *different* offsets from each
   other, since the numbering scheme resets at Chapter 1. Determine both:
   - **Roman offset:** read a front-matter page with a visible roman-numeral
     page number (e.g. in the Preface/Acknowledgments). `offset_roman =
     pdf_page_index - roman_value`.
   - **Arabic offset:** continue reading forward from the end of the Table
     of Contents until the first chapter heading appears. Note its printed
     page number and the PDF page index it was found at.
     `offset_arabic = pdf_page_index - printed_page_number`.
   - **Verify it holds.** Spot-check `offset_arabic` against at least two
     more chapters elsewhere in the book (e.g. one roughly in the middle,
     one near the end) by reading at `printed_start + offset_arabic` and
     confirming the chapter heading matches. Some books insert unnumbered
     blank pages to force chapters onto odd/recto pages, which can shift
     the offset partway through — if a spot-check doesn't match, treat the
     book as having multiple offset regions and note where each one starts
     rather than forcing one constant across the whole book.

6. **Compute every chapter's PDF page range.** For each chapter:
   `pdf_start = printed_start + offset_arabic` (adjusted per region if the
   offset isn't constant), `pdf_end = next_chapter's pdf_start - 1` (or,
   for the last chapter, up to wherever back matter — glossary,
   bibliography, index — begins). Get the PDF's total page count with
   `python3 scripts/page_count.py` to bound the final chapter and back
   matter. Flag any chapter whose range exceeds
   20 pages — `learn-chapter` and `diagram-chapter` need multiple `Read`
   calls for those.

7. **Write `notes/00-toc-page-map.md`.** Read
   `references/page-map-template.md` (next to this skill file) and follow
   its structure exactly — headings and table columns verbatim, every value
   replaced with this book's. The template's values are a worked example
   from a fictional book; none of them carry over. The other skills locate
   a chapter's PDF range by reading this file, so the format holding steady
   across books is what keeps them working.

8. **Initialize `progress.md`** at the project root: one row per chapter
   (chapter number, title) with five empty date columns, plus a short
   footer note that cells get filled with the completion date
   (`YYYY-MM-DD`) by the corresponding skill. Keep the column names exactly
   as below — every other skill looks them up by name, and
   `study-chapter`'s batch mode reads `Notes`/`Diagrams` to decide what's
   already done:

   | Column | Filled by |
   |---|---|
   | `Notes` | `learn-chapter` |
   | `Diagrams` | `diagram-chapter` |
   | `Quizzed` | `quiz-chapter` |
   | `Practiced` | `practice-chapter` |
   | `Reviewed` | `review-book` (last cross-chapter review that covered it) |

   Unlike the others, `Reviewed` is overwritten each time rather than filled
   once — it's a "last seen" date that drives which chapters come up for
   review next.

9. **Tell the user** setup is complete, name the chapter count found, and
   point to `notes/00-toc-page-map.md` and `progress.md`. Suggest
   `/learn-chapter 1` or the `study-chapter` agent as the next step, and
   mention `/study-status` as the way to see what's next at any point.
   Don't start reading a chapter yourself — this skill's job ends at a ready
   project.
