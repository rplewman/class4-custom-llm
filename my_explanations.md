# My explanations (my own words)

Written 2026-09-21 after the 10-step setup run (`llm_runs/20260921T232818_017855Z`),
after working through the ideas with the assistant. Text below is mine; numbers refer to
that run's `inspection.json`.

## Probabilities, loss, gradient and weight change

1. Probabilities are nearly equal because the model has no preference yet.
2. Loss is defined as how surprised the model is by the real next word.
3. The gradient says, for each weight, which way the loss changes if you nudge it. A
   positive gradient means nudging up increases surprise.
4. The weight would move down with a positive gradient.
5. The probability on the words that really follow "the customer" goes up and loss goes
   down.

Real example from the run: the first coordinate of the "customer" embedding started at
-0.05759, had gradient +0.00069, and was -0.05859 after step 1 (learning rate 0.001).

## Token, token ID, and embedding

The fact that token IDs are adjacent to one another does not mean that the words are
similar. Two similar words would point in similar directions via the embedding process.
(Example from the run: "customer" is token ID 28. A word with ID 29 could be completely
unrelated in meaning; the ID is just a slot number, not a measure of similarity.)

## Why training steps and learning rate were chosen

I ran a 10-step setup check first, to confirm the pipeline worked before spending time on
a real run. For both real experiments I used 3000 steps, so the only difference between
them is the corpus, not the training budget. I kept the learning rate at 0.001, the
notebook's default, since I had no reason to move it before seeing a baseline. An oversized
learning rate would overshoot the low point of the loss instead of settling into it, like
taking huge steps downhill and walking past the bottom of the valley; a rate that's too
small barely moves the weights and would need far more steps to get anywhere.

## Probabilities becoming a generated word, and temperature

The model doesn't always output the top-probability word, instead it generates samples
where a word with 30% probability is picked 30% of the time. Temperature shapes the
lottery before drawing: high and low temperatures mean the text will be more and less
predictable. This only changes how a word is picked at generation time; it does not change
any weights.

## Why attention cannot see future tokens

Allowing the model to peek at the word it is trying to guess would defeat the purpose. It
would have learned nothing from training, and the prediction wouldn't actually be a
prediction. Blocking future tokens during training keeps training consistent and relevant
to how the model is actually used afterward, when future words genuinely don't exist yet.
