# Prediction: 3000-step runs (written before training)

Written 2026-09-21, before any 3000-step training or eval. The first setup run
(10 steps, `llm_runs/20260921T232818_017855Z`) is the baseline for comparison.

## Settings
- TRAINING_STEPS: 3000
- LEARNING_RATE: 0.001
- Starter run: classroom corpus only. Extension run: classroom corpus plus new files.

## What I expect from the starter run
1. **Validation loss:** lower than the 10-step value of 4.21. (I did not give a number.)
2. **Starter-pattern cases (16):** scores will be higher than in the 10-step run.
3. **New-phrasing cases (8):** scores will be slightly lower than in the 10-step run
   (which was 4/8).
4. **Extension cases (24):** these will stay below the other groups, because the
   classroom corpus does not contain the words or patterns they need.

## What actually happened (starter run)
Run: `llm_runs/20260922T000008_123080Z`. 3000 steps completed, not interrupted; 18.3 s of
training on CPU (Windows 11, torch 2.14.0+cpu), 111,872 parameters, 136-token vocabulary,
4,132 training and 460 validation passages, unknown-token rate 0.0 for both.

| step | training loss | validation loss |
|---|---|---|
| 0 | 4.9263 | 4.9275 |
| 1500 | 0.6821 | 0.7182 |
| 3000 | 0.6783 | 0.7061 |

(Fixed panels of 20 training and 20 validation documents.)

| group | untrained | trained (3000 steps) |
|---|---|---|
| Starter patterns (16) | 6/16 | 16/16 |
| New phrasings (8) | 3/8 | 4/8 |
| Extension (24) | 0/24, unscorable | 0/24, unscorable |
| All cases (48) | 9/48 | 20/48 |

Scorable cases: 24 of 48 (coverage 0.5). Accuracy among scorable cases: 37.5% before,
83.3% after.

Prediction check:
1. Validation loss lower than 4.21: **right** (0.706). It barely moved between step 1500
   and 3000 (0.718 to 0.706).
2. Starter-pattern score higher than the 10-step run (5/16): **right** (16/16).
3. New-phrasing score slightly lower than the 10-step run (4/8): **wrong.** It stayed at
   4/8, the same as the 10-step run. Training did not help new phrasings.
4. Extension cases below the other groups: **right**, but they were unscorable (missing
   vocabulary), not answered wrongly.

Leakage check: no eval prompt, and no prompt plus any of its four choices, appears verbatim
in `corpus.txt`. Some 5-word fragments of the starter-pattern and new-phrasing prompts do
appear, because the corpus contains sibling sentences built from the same templates (the
exact test prefixes are withheld). The 16/16 therefore shows a narrow learned template, not
general understanding.
