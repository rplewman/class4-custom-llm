# Prediction: starter-corpus run (written before training)

Written 2026-09-21, before any training or eval was run.

## Settings
- Corpus: classroom (starter), no extra files
- TRAINING_STEPS: 10 (a setup check to see whether the pipeline works)
- LEARNING_RATE: 0.001

## Why these choices
I chose 10 steps to check that the pipeline works, not to get a meaningful model.
I do not think 10 steps is enough to meaningfully move the needle.

## What I expect
1. **Loss:** Still substantial after 10 steps; it will go down a little. Training loss
   will be lower after 10 steps because the model is still learning. Validation loss
   will be basically the same.
2. **Generated text:** Still word salad after 10 steps. I do not think it will use
   meaningful sentence patterns from the corpus.
3. **Four-choice eval score:** Slightly higher than 25% after 10 steps, but still
   essentially random.
4. **Hardest and easiest groups:** The 16 tests using classroom-corpus sentence
   patterns will score highest. The 24 extension tests the corpus does not teach will
   score lowest, since they are net new.

## What actually happened
Run: `llm_runs/20260921T232818_017855Z` (10 steps, learning rate 0.001, classroom corpus,
CPU, Windows 11, torch 2.14.0+cpu, 111,872 parameters). Training took 0.18 s of compute.
A first attempt failed before training (NumPy missing) and is kept as
`llm_runs/FAILED_numpy_missing_20260921T232740_042624Z`.

1. **Loss.** Measured on fixed panels of 20 training and 20 validation documents:

   | step | training loss | validation loss |
   |---|---|---|
   | 0 | 4.9263 | 4.9275 |
   | 5 | 4.3415 | 4.3228 |
   | 10 | 4.2076 | 4.2073 |

   Prediction check: loss went down and stayed substantial (right). Training loss fell,
   as predicted. **Validation loss also fell by about the same amount (wrong: I predicted
   it would stay basically the same).**
2. **Generated text.** Samples at steps 0, 5 and 10 are all word salad with the same
   generation settings (right). No meaningful sentence pattern appears.
3. **Four-choice eval score.** 9/48 correct before and 9/48 after (18.75% of all cases).
   Among the 24 scorable cases, accuracy was 37.5% both before and after. That is above
   25%, but the untrained model already scored 37.5%, so training changed nothing overall.
   With only 24 scorable cases this is within noise (partly right, but no change was seen).
4. **Groups.** Trained model: starter patterns 5/16, new phrasings 4/8, extension 0/24.
   Untrained: 6/16, 3/8, 0/24. The extension group was lowest (right), but only because
   all 24 cases contain words missing from the vocabulary (coverage 0.0), so they were
   unscorable, not answered wrongly. **The highest group was new phrasings, not starter
   patterns (wrong).**

Vocabulary: the model has 136 tokens (133 training word types plus special tokens); the
509 in the assignment is only a cap. Initial loss is about ln(136) = 4.9, which is why it
starts near 4.9 and not the ~6.2 the assistant estimated earlier for a 509-word vocabulary.
