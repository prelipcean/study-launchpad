# Page map template

Copy this structure to `notes/00-toc-page-map.md`. The values below are a
worked example from a fictional book — replace every one of them. Keep the
headings and the table columns as they are, so `learn-chapter` and
`diagram-chapter` can find the PDF page range the same way in every project.

---

# Page map — *Building Agentic Systems*

| | |
|---|---|
| **Author** | A. Example |
| **ISBN** | 978-1-23456-789-0 |
| **PDF file** | `building-agentic-systems.pdf` |
| **Total PDF pages** | 412 |
| **Chapters** | 14 (in 4 parts) |

## Page offsets

PDF page indices (what the `Read` tool's `pages` parameter addresses) differ
from the printed page numbers shown in the book. Offsets found:

| Region | Offset | Derivation | Verified against |
|---|---|---|---|
| Front matter (roman) | +12 | `xiv` found at PDF page 26 | Preface `xi` → PDF 23 ✓ |
| Main body (arabic) | +18 | Ch. 1 printed p. 3 found at PDF page 21 | Ch. 7 printed p. 142 → PDF 160 ✓; Ch. 14 printed p. 331 → PDF 349 ✓ |

> If a spot-check fails, the book has **multiple offset regions** (usually
> from unnumbered blanks inserted to start chapters on a recto page). Add one
> row per region with the PDF page where it starts, and use the right region's
> offset per chapter in the table below rather than forcing one constant.

## Chapters

`Pages` is the PDF page count for the chapter. Flag `>20pp` means
`learn-chapter` and `diagram-chapter` need more than one `Read` call to cover
the range.

| Ch | Title | Printed | PDF range | Pages | Flag |
|---:|---|---|---|---:|---|
| 1 | What Makes a System Agentic | 3–18 | 21–36 | 16 | |
| 2 | The Decide–Act–Observe Loop | 19–44 | 37–62 | 26 | `>20pp` |
| 3 | Tools as an Interface | 45–61 | 63–79 | 17 | |
| … | … | … | … | … | |
| 14 | Evaluating Agents in Production | 331–352 | 349–370 | 22 | `>20pp` |

## Parts

Omit this section entirely if the book has no part/section groupings.

| Part | Title | Chapters | PDF range |
|---|---|---|---|
| I | Foundations | 1–3 | 21–79 |
| II | Building Blocks | 4–8 | 80–196 |
| III | Orchestration | 9–11 | 197–280 |
| IV | Production Concerns | 12–14 | 281–370 |

## Back matter

Not chapters — recorded so the last chapter's range has a bound.

| Section | PDF range |
|---|---|
| Appendix A: Reference | 371–388 |
| Glossary | 389–396 |
| Index | 397–412 |
