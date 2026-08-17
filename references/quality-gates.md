# Writing and Quality Gates

A chapter is not "done" merely because text exists. Use these gates before export.

## Book-level gates

- The title/subtitle match the actual promise.
- The outline has a clear progression rather than a collection of articles.
- Each chapter has a distinct job.
- Terminology is consistent.
- Cross-references point to real chapters/sections.
- The introduction does not over-promise what the book never delivers.
- The conclusion closes the main promise rather than simply summarizing headings.

## Chapter-level gates

### Structure
- Opening establishes why the chapter matters.
- Sections follow a logical order.
- Examples support the point instead of replacing it.
- Ending provides synthesis, action, or transition.

### Repetition
- No repeated explanation of the same concept across adjacent chapters.
- Recaps are shorter than the original explanation.
- Anecdotes and examples are not reused accidentally.

### Factual integrity
- Material factual claims are supported when the project requires sourcing.
- Dates, names, statistics, units, and product/platform rules are checked.
- Uncertainty is not rewritten as certainty.

### Style
- Voice follows `style-guide.md`.
- Sentence rhythm is varied naturally.
- Remove generic AI throat-clearing and empty transitions.
- Avoid inflated claims such as "revolutionary" unless justified.
- Prefer concrete nouns, verbs, examples, and constraints.

### Reader usefulness
- The reader can tell what to do with the information.
- Definitions appear before jargon-heavy use.
- Examples match the target reader's level.
- Lists are used for true collections, not as a substitute for explanation.

## Final mechanical checks

Run `scripts/check_manuscript.py`. Manually inspect:

- TOC ordering
- heading hierarchy
- image placement and captions
- tables on narrow screens
- code blocks / equations
- footnotes and links
- front matter and copyright page if applicable
- final chapter order
