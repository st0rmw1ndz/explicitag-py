import re

from mutagen.mp4 import MP4

from explicitag.data import MP4Rating, MP4Tags


def mark_rating(audio: MP4, rating: MP4Rating) -> None:
    audio[MP4Tags.rating] = [rating.value]


def is_explicit_lyrics(audio: MP4, explicit_pattern: re.Pattern) -> MP4Rating:
    lyrics = str(audio[MP4Tags.lyrics]).lower()
    return (
        MP4Rating.EXPLICIT
        if explicit_pattern.search(lyrics)
        else MP4Rating.CLEAN
    )
