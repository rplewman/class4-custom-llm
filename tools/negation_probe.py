"""Own diagnostic probe (NOT the 48-case eval, and never used for training).

Negation: for stories built from my own template words that do not appear in a run's training
text, compare the model's next-word probability for the object actually done (o2) with the
object that was negated (o1) at the end of
    "<name> did not <verb> the <o1> , <pro> <past> the <o2> , <name> <past> the"
Opposites: for "the <na> was <a> but the <nb> was", compare P(b) with P(a).
Chance for each pairwise comparison is 50%.
Run: python tools/negation_probe.py
"""
import json
import random
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from run_evals import load_model, word_tokens  # noqa: E402
from make_extension_corpus import PEOPLE, VERBS, PAIRS  # noqa: E402

RUNS = {"extension_v1_split_bug": "llm_runs/20260922T001103_572234Z",
        "extension_v2_fixed": "llm_runs/20260922T001708_046660Z"}
rng = random.Random(7)


def training_text(run):
    return " ".join((ROOT / run / "corpus.txt").read_text(encoding="utf-8").lower().split())


def negation_items(texts):
    items = []
    for name, pr in PEOPLE.items():
        for base, past, objs in VERBS:
            for o1 in objs:
                for o2 in objs:
                    if o1 == o2:
                        continue
                    story = f"{name} did not {base} the {o1} , {pr} {past} the {o2} ,"
                    if any(story in t for t in texts):
                        continue
                    items.append((f"{story} {name} {past} the", o1, o2))
    rng.shuffle(items)
    return items[:300]


def opposites_items(texts):
    items = []
    for a, b, an, bn in PAIRS:
        for x, y, na_list, nb_list in ((a, b, an, bn), (b, a, bn, an)):
            for na in na_list:
                for nb in nb_list:
                    sentence = f"the {na} was {x} but the {nb} was {y} ."
                    if any(sentence in t for t in texts):
                        continue
                    items.append((f"the {na} was {x} but the {nb} was", x, y))
    rng.shuffle(items)
    return items[:300]


@torch.inference_mode()
def pairwise(model, vocab, items):
    stoi = {w: i for i, w in enumerate(vocab)}
    right = top = 0
    for prompt, wrong, right_word in items:
        ids = [stoi["<BOS>"]] + [stoi[t] for t in word_tokens(prompt)]
        probs = torch.softmax(model(torch.tensor([ids]))[0][0, -1].float(), -1)
        right += int(probs[stoi[right_word]] > probs[stoi[wrong]])
        top += int(vocab[int(probs.argmax())] == right_word)
    return {"n": len(items), "right_word_beats_other_word": right, "right_word_is_top_of_all_words": top}


def in_both_vocabs(items, vocabs):
    keep = lambda it: all(t in v for v in vocabs for t in word_tokens(" ".join(it)))
    return [it for it in items if keep(it)]


def main():
    texts = [training_text(r) for r in RUNS.values()]  # held out from BOTH runs
    vocabs = [set(load_model(ROOT / r / "model.pt")[1]) for r in RUNS.values()]
    neg = in_both_vocabs(negation_items(texts), vocabs)
    opp = in_both_vocabs(opposites_items(texts), vocabs)
    out = {"note": "own diagnostic probe, not the 48-case eval; items unseen in both extension runs' training text",
           "n_negation_items": len(neg), "n_opposites_items": len(opp), "results": {}}
    for label, run in RUNS.items():
        for stage, fname in (("untrained", "model_untrained.pt"), ("final", "model.pt")):
            model, vocab, _ = load_model(ROOT / run / fname)
            out["results"][f"{label}/{stage}"] = {"negation_copy": pairwise(model, vocab, neg),
                                                  "opposites": pairwise(model, vocab, opp)}
    (ROOT / "evidence" / "probe_results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
