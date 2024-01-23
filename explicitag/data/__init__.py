from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class MP4Rating(Enum):
    CLEAN = 0
    EXPLICIT = 1


@dataclass
class MP4Tags:
    lyrics = "©lyr"
    title = "©nam"
    artist = "©ART"
    rating = "rtng"


explicit_words_path = Path(__file__).resolve().parent / "explicit_words.txt"

with explicit_words_path.open(mode="r") as f:
    explicit_words = f.read().splitlines()
