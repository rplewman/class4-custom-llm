# Prediction: extension runs (opposites + negation), written before showing any results

Written 2026-09-22. The extension eval and loss numbers had been computed for run v1 but
had NOT been shown to me when I wrote this; run v2 (fixed) had not been trained yet.

## Settings
- Same as the starter run: 3000 steps, learning rate 0.001, same seed.
- Corpus: classroom sentences plus `corpus/opposites.txt` and `corpus/negation.txt`.
- Extension categories chosen: **opposites** (easier) and **negation** (harder).

## My prediction (my words)
"The model will do better on opposites, worse on negations."

Interpretation recorded by the assistant (not my wording; correct me if wrong): opposites
cases will score better than negation cases. The starter model scored 0/24 on all extension
cases (all unscorable), so "worse" cannot mean worse than the starter.

## What actually happened
Runs: extension v1 `llm_runs/20260922T001103_572234Z` (negation stories were split into
separate sentences by the notebook, so the pattern was never seen together) and extension v2
`llm_runs/20260922T001708_046660Z` (fixed, used for the comparison). Both 3000 steps,
learning rate 0.001.

**On the fixed 48-case eval (v2, trained):**
- Opposites: 1 of 3 cases scorable, and that one was correct (1/1). The other 2 contained
  words the model does not have.
- Negation: 0 of 3 cases scorable. All 3 contained words the model does not have.
- So the eval alone cannot really test your prediction: 23 of the 24 extension cases stayed
  unscorable.

**On my own separate probe** (`tools/negation_probe.py`, results in
`evidence/probe_results.json`; not part of the eval and never used for training). Items are
new combinations of my own template words, unseen in both runs' training text:

| model (trained) | opposites: right opposite beats wrong word | negation: word actually done beats negated word |
|---|---|---|
| extension v1 (split bug) | 288/288 | 146/300 (49%, chance is 50%) |
| extension v2 (fixed) | 284/288 | 176/300 (59%) |

Prediction check: **consistent with your prediction.** The model does clearly better on
opposites than on negation. Negation only rose from chance to modestly above chance once the
stories were kept together, and it is still weak. Caveat: the opposites probe reuses the same
23 word pairs and templates as training, so it shows the pairs were learned, not a general
understanding of opposites.
