---
name: quiz-chapter
description: Interactively quiz the user on a chapter they've already read, one question at a time. Use when the user wants to be tested or check their understanding (e.g. "/quiz-chapter", "/quiz-chapter 3", "quiz me on memory").
---

# quiz-chapter

Socratic, turn-by-turn quizzing on a chapter's notes. This must be genuinely
interactive — never dump a list of questions at once. The whole point is
back-and-forth: ask, wait, react, ask again.

## Steps

1. **Determine the chapter.** If the user named one, use it. Otherwise open
   `progress.md` and pick the most recent chapter with notes done but not
   yet quizzed (or the most recently noted chapter if several are unquizzed).

2. **Read that chapter's notes** at `notes/NN-slug.md`. If it doesn't exist,
   tell the user to run `/learn-chapter` first — don't try to quiz from the
   raw PDF.

3. **Ask one question at a time.** Aim for 5-8 questions total, mixing:
   - **Recall** — "What does X mean?" / "What's the difference between X
     and Y?"
   - **Applied / why** — "Why would you choose X over Y in a production
     system?" / "What breaks if you skip X?"

   Pull questions from the chapter's Key Concepts and Key Takeaways. After
   each question, **wait for the user's answer** before doing anything else.

4. **React to each answer** before moving on: confirm what's right, correct
   what's off (briefly — point to the concept, don't re-teach the whole
   chapter), then ask the next question. Don't pre-plan and print the full
   question list up front.

5. **After the last question**, give a short summary: what they clearly
   understand, what's shaky, and 1-2 things worth re-reading if any gaps
   showed up.

6. **Save a transcript** at `quizzes/NN-slug.md`: each question, the user's
   answer (verbatim or lightly trimmed), and your reaction/correction, in
   order, followed by the closing summary from step 5. This is a record of
   what they actually said, not a cleaned-up answer key — keep their
   answers as given, including wrong ones, so re-reading it later shows
   real gaps rather than a flattering recap. If `quizzes/NN-slug.md`
   already exists (a repeat quiz on this chapter), append a new dated
   section rather than overwriting the earlier attempt — that history is
   useful for seeing whether a gap actually closed.

   This file is also `review-book`'s main input: it mines these transcripts
   for the concepts to re-test weeks later. A transcript that smooths over
   a wrong answer silently removes that concept from future review, so
   record misses plainly.

7. **Update `progress.md`** — fill in today's date in the "Quizzed" column
   for this chapter.
