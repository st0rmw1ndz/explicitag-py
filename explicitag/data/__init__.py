import os
from dataclasses import dataclass
from enum import Enum
from typing import List


class MP4Rating(Enum):
    CLEAN = 0
    EXPLICIT = 1


@dataclass
class MP4Tags:
    lyrics: str = "©lyr"
    title: str = "©nam"
    artist: str = "©ART"
    rating: str = "rtng"


explicit_words_path: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "explicit_words.txt"
)


with open(explicit_words_path, "r") as t:
    explicit_words: List[str] = t.read().splitlines()
