"""Generate the extension teaching files (opposites + negation) into corpus/.

Content is written from the two category ideas (opposites, negation), not from the eval
cases. The eval file is read ONLY to delete any generated line that contains a whole eval
prompt; no eval text is ever written to the corpus. Run: python tools/make_extension_corpus.py
"""
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rng = random.Random(4)
norm = lambda s: re.sub(r"\s+", " ", s.lower()).strip()

PEOPLE = {"kofi": "he", "lena": "she", "omar": "he", "priya": "she", "tomas": "he",
          "mei": "she", "sam": "they", "rosa": "she", "jin": "he", "nadia": "she",
          "hugo": "he", "ines": "she"}

# (adjective a, adjective b, nouns that are usually a, nouns that are usually b)
PAIRS = [
    ("hot", "cold", ["soup", "bath", "oven"], ["ice", "lake", "wind"]),
    ("big", "small", ["elephant", "house", "truck"], ["mouse", "coin", "seed"]),
    ("tall", "short", ["tower", "giraffe", "tree"], ["stool", "bush", "fence"]),
    ("fast", "slow", ["horse", "rocket", "rabbit"], ["snail", "turtle", "tractor"]),
    ("heavy", "light", ["rock", "anvil", "suitcase"], ["feather", "balloon", "leaf"]),
    ("loud", "quiet", ["drum", "storm", "crowd"], ["library", "night", "snow"]),
    ("early", "late", ["sunrise", "breakfast", "morning"], ["sunset", "dinner", "midnight"]),
    ("full", "empty", ["bucket", "stadium", "jar"], ["attic", "cupboard", "bottle"]),
    ("open", "closed", ["window", "gate", "museum"], ["door", "lid", "bakery"]),
    ("wet", "dry", ["towel", "grass", "sponge"], ["sand", "desert", "paper"]),
    ("hard", "soft", ["rock", "floor", "wall"], ["pillow", "blanket", "cotton"]),
    ("clean", "dirty", ["kitchen", "plate", "shirt"], ["boots", "puddle", "sock"]),
    ("happy", "sad", ["child", "puppy", "singer"], ["girl", "kitten", "traveler"]),
    ("strong", "weak", ["ox", "rope", "bridge"], ["thread", "twig", "candle"]),
    ("thick", "thin", ["wall", "book", "blanket"], ["paper", "wire", "ice"]),
    ("near", "far", ["school", "park", "market"], ["moon", "mountain", "island"]),
    ("high", "low", ["cloud", "shelf", "bird"], ["valley", "ditch", "fog"]),
    ("bright", "dark", ["sun", "lamp", "star"], ["cave", "cellar", "tunnel"]),
    ("rich", "poor", ["banker", "king", "landlord"], ["beggar", "peasant", "servant"]),
    ("easy", "difficult", ["game", "song", "lesson"], ["exam", "maze", "riddle"]),
    ("safe", "dangerous", ["harbor", "shelter", "bridge"], ["cliff", "storm", "jungle"]),
    ("cheap", "expensive", ["pencil", "pebble", "candle"], ["diamond", "castle", "yacht"]),
    ("young", "old", ["puppy", "sapling", "baby"], ["oak", "grandfather", "ruin"]),
]

VERBS = [  # (base, past, objects)
    ("buy", "bought", ["jacket", "lamp", "ticket", "radio", "scarf", "kettle"]),
    ("choose", "chose", ["carpet", "painting", "hat", "ring", "chair"]),
    ("pick", "picked", ["plum", "cherry", "lemon", "melon", "pumpkin"]),
    ("take", "took", ["umbrella", "ladder", "map", "torch", "coat"]),
    ("cook", "cooked", ["fish", "beans", "pasta", "eggs", "stew"]),
    ("paint", "painted", ["fence", "door", "wall", "boat", "shed"]),
    ("borrow", "borrowed", ["book", "ladder", "bucket", "drill", "spade"]),
    ("bring", "brought", ["cake", "flowers", "candles", "blanket", "guitar"]),
]
PLACES = ["library", "park", "harbor", "bakery", "museum", "cinema", "garden", "market"]
ANIMALS = ["fox", "owl", "deer", "hare", "heron", "badger"]
CONTAINERS = ["box", "bag", "basket", "cupboard", "drawer"]


def opposites_line():
    a, b, an, bn = rng.choice(PAIRS)
    if rng.random() < 0.5:  # swap roles so both directions are taught
        a, b, an, bn = b, a, bn, an
    na, nb = rng.choice(an), rng.choice(bn)
    name = rng.choice(list(PEOPLE))
    return rng.choice([
        f"{a} is the opposite of {b} .",
        f"{a} and {b} are opposites .",
        f"the words {a} and {b} mean opposite things .",
        f"the {na} was {a} but the {nb} was {b} .",
        f"a {na} is {a} while a {nb} is {b} .",
        f"{name} felt the {na} was {a} , not {b} .",
        f"next to the {nb} , the {na} looked {a} .",
        f"if the {nb} is {b} , it is not {a} .",
        f"{name} wanted something {a} , but the {nb} was {b} .",
        f"we describe the {na} as {a} and the {nb} as {b} , which are opposites .",
        f"the {na} is {a} , so its opposite would be {b} .",
        f"you say {b} for the {nb} and {a} for the {na} .",
    ])


def negation_line():
    """Negation stories. Sentences inside a story are joined with commas, because the
    notebook splits every file at each '.', '!' or '?' and would otherwise break a story
    into separate passages (this happened in extension run v1)."""
    name = rng.choice(list(PEOPLE))
    pr = PEOPLE[name]
    kind = rng.random()
    if kind < 0.6:
        base, past, objs = rng.choice(VERBS)
        o1, o2 = rng.sample(objs, 2)
        if rng.random() < 0.6:  # story whose last step repeats the thing actually done
            return rng.choice([
                f"{name} did not {base} the {o1} , {pr} {past} the {o2} , {name} {past} the {o2} .",
                f"{name} did not {base} the {o1} , {pr} {past} the {o2} , so {name} {past} the {o2} .",
            ])
        return rng.choice([
            f"the shop did not have the {o1} , so {name} {past} the {o2} instead .",
            f"{name} wanted the {o1} , but it was gone , so {pr} {past} the {o2} .",
            f"{name} said no to the {o1} and yes to the {o2} .",
            f"it was not the {o1} that {name} {past} , it was the {o2} .",
        ])
    if kind < 0.8:
        p1, p2 = rng.sample(PLACES, 2)
        if rng.random() < 0.7:
            return f"{name} did not go to the {p1} , {pr} went to the {p2} , {name} went to the {p2} ."
        return f"{name} did not go to the {p1} , {pr} went to the {p2} ."
    if kind < 0.88:
        a1, a2 = rng.sample(ANIMALS, 2)
        if rng.random() < 0.7:
            return f"{name} did not see the {a1} , {pr} saw the {a2} , {name} saw the {a2} ."
        return f"{name} did not see the {a1} , {pr} saw the {a2} ."
    if kind < 0.94:
        c = rng.choice(CONTAINERS)
        o1, o2 = rng.sample(rng.choice(VERBS)[2], 2)
        return f"there was no {o1} in the {c} , only the {o2} ."
    a, b, an, bn = rng.choice(PAIRS)
    if rng.random() < 0.5:
        a, b, an, bn = b, a, bn, an
    na = rng.choice(an)
    return f"the {na} was not {b} , it was {a} ."


def build(maker, target):
    lines = set()
    while len(lines) < target:
        lines.add(maker())
    return sorted(lines)


def main():
    suite = json.loads((ROOT / "evals" / "language_evals.json").read_text(encoding="utf-8"))["cases"]
    prompts = [norm(c["prompt"]) for c in suite]
    out = {"opposites.txt": build(opposites_line, 420), "negation.txt": build(negation_line, 420)}
    (ROOT / "corpus").mkdir(exist_ok=True)
    for fname, lines in out.items():
        kept = [ln for ln in lines if not any(p in norm(ln) for p in prompts)]
        dropped = len(lines) - len(kept)
        (ROOT / "corpus" / fname).write_text("\n".join(kept) + "\n", encoding="utf-8")
        print(f"{fname}: wrote {len(kept)} unique lines; dropped {dropped} that contained a whole eval prompt")


if __name__ == "__main__":
    main()
