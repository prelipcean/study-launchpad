---
name: review-book
description: Cross-chapter retention review that targets what the user actually got wrong before, pulling weak spots from past quiz transcripts and least-recently-reviewed chapters. Use when the user wants to revisit earlier material rather than a single chapter (e.g. "/review-book", "review what I've forgotten", "quiz me across chapters", "spaced review").
---

# review-book

Spaced, cross-chapter review. `quiz-chapter` tests one chapter right after
reading it, which measures short-term recall; this skill measures what
actually stuck weeks later, and deliberately targets the material the user
has already demonstrated they're shaky on.

Interactive, one question at a time — same rule as `quiz-chapter`. Never dump
a question list.

## Steps

1. **Read the state.** `progress.md` for which chapters have notes and each
   chapter's `Reviewed` date, plus every existing `quizzes/NN-slug.md`.
   Older projects may have a `progress.md` with no `Reviewed` column — if
   so, add the column (empty for all rows) and carry on; don't fail.

2. **Mine the quiz transcripts for real weak spots.** The transcripts record
   the user's answers verbatim, wrong ones included — that's the point of
   them. Pull out the specific concepts where an answer was corrected or
   partly wrong. These are worth far more than anything you'd invent, so
   gather them before looking at the notes.

3. **Pick 6-10 questions spanning at least three chapters**, weighted:
   - **~half on known weak spots** from step 2. Ask these from a different
     angle than last time — if the first attempt was a definition question
     they fumbled, ask them to apply the concept instead. Re-asking the
     identical question tests memory of the quiz, not of the material.
   - **~a quarter on least-recently-reviewed chapters** (oldest or empty
     `Reviewed` date), drawn from their Key Takeaways.
   - **~a quarter connecting two chapters** — "how does the retrieval step
     in ch. 4 interact with the tool loop in ch. 7?" These synthesis
     questions are the ones single-chapter quizzing structurally can't ask,
     and usually the most valuable here.

   Skip chapters with no notes — there's nothing to review against.

4. **Ask one question at a time**, naming which chapter it's from so the
   user can orient. Wait for the answer. React before moving on: confirm
   what's right, correct what's off briefly, pointing at the concept in the
   notes. If an answer reveals a gap big enough that the next question
   depends on it, close that gap first rather than pressing ahead.

5. **Close with a retention read**, not just a score: which previously-weak
   concepts have clearly firmed up, which are *still* shaky after a second
   pass, and which chapters are worth re-reading outright. A concept missed
   twice should be called out plainly as such — that's the signal the user
   can't get from any single quiz.

6. **Save the transcript** to `reviews/YYYY-MM-DD-review.md`: the chapters
   covered, each question with the chapter it came from, the user's answer
   as given, your reaction, and the closing retention read. Note explicitly
   which questions were repeat attempts at a known weak spot and whether
   they closed — the next `/review-book` run reads this file for exactly
   that.

7. **Update `progress.md`** — set `Reviewed` to today's date for every
   chapter this session actually asked about. Overwrite any earlier date;
   this column tracks last-seen, not first-seen. Chapters you didn't touch
   keep their old date, which is what floats them to the top next time.
