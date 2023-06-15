import unicodedata
from collections import Counter
from typing import Dict, Iterable, List, Mapping, Optional

from espeak_phonemizer import Phonemizer

DEFAULT_PHONEME_ID_MAP: Dict[str, List[int]] = {
    "_": [0],
    "^": [1],
    "$": [2],
    " ": [3],
    "!": [4],
    "'": [5],
    "(": [6],
    ")": [7],
    ",": [8],
    "-": [9],
    ".": [10],
    ":": [11],
    ";": [12],
    "?": [13],

    "a0": [14],
    "a1": [15],
    "b": [16],
    "bj": [17],
    "c": [18],
    "ch": [19],
    "d": [20],
    "dj": [21],
    "e0": [22],
    "e1": [23],
    "f": [24],
    "fj": [25],
    "g": [26],
    "gj": [27],
    "h": [28],
    "hj": [29],
    "i0": [30],
    "i1": [31],
    "j": [32],
    "k": [33],
    "kj": [34],
    "l": [35],
    "lj": [36],
    "m": [37],
    "mj": [38],
    "n": [39],
    "nj": [40],
    "o0": [41],
    "o1": [42],
    "p": [43],
    "pj": [44],
    "r": [45],
    "rj": [46],
    "s": [47],
    "sch": [48],
    "sh": [49],
    "sj": [50],
    "t": [51],
    "tj": [52],
    "u0": [53],
    "u1": [54],
    "v": [55],
    "vj": [56],
    "y0": [57],
    "y1": [58],
    "z": [59],
    "zh": [60],
    "zj": [61],
}

from .ru_dictionary import convert
import re


wdic = {}
for line in open("db/dictionary"):
   items = line.split()
   if items[0] not in wdic:
       wdic[items[0]] = " ".join(items[1:])

def phonemize(text: str, phonemizer: Phonemizer) -> List[str]:

    text = re.sub("—", "-", text)
    text = re.sub("\"", " ", text)
    text = re.sub("([!'(),.:;?])", r' \1 ', text)

    phonemes = []
    for word in text.split():
        if re.match("[!'(),.:;?]", word) or word == '-':
            phonemes.append(word)
            continue

        word = word.lower()
        if len(phonemes) > 0: phonemes.append(' ')


        if word in wdic:
            phonemes.extend(wdic[word].split())
        else:
            print ("!!!!", word)
            phonemes.extend(convert(word).split())

    print (text, phonemes)

    # Phonemes are decomposed into unicode codepoints
    return phonemes


def phonemes_to_ids(
    phonemes: Iterable[str],
    phoneme_id_map: Optional[Mapping[str, Iterable[int]]] = None,
    missing_phonemes: "Optional[Counter[str]]" = None,
    pad: Optional[str] = "_",
    bos: Optional[str] = "^",
    eos: Optional[str] = "$",
) -> List[int]:
    if phoneme_id_map is None:
        phoneme_id_map = DEFAULT_PHONEME_ID_MAP

    phoneme_ids: List[int] = []

    if bos:
        phoneme_ids.extend(phoneme_id_map[bos])

    if pad:
        phoneme_ids.extend(phoneme_id_map[pad])

    for phoneme in phonemes:
        mapped_phoneme_ids = phoneme_id_map.get(phoneme)
        if mapped_phoneme_ids:
            phoneme_ids.extend(mapped_phoneme_ids)

            if pad:
                phoneme_ids.extend(phoneme_id_map[pad])
        elif missing_phonemes is not None:
            # Make note of missing phonemes
            missing_phonemes[phoneme] += 1

    if eos:
        phoneme_ids.extend(phoneme_id_map[eos])

    print (phoneme_ids)
    return phoneme_ids
