from mutagen.mp4 import MP4

from explicitag.data import MP4Rating, MP4Tags, explicit_words


def mark_rating(audio: MP4, rating: MP4Rating) -> None:
    """Marks an MP4 audio file as explicit or clean.

    :param audio: MP4 audio file.
    :param rating: Rating to mark the file with.
    """
    audio[MP4Tags.rating] = [rating.value]
    audio.save()


def is_explicit_lyrics(audio: MP4) -> MP4Rating:
    """Checks if an MP4 audio file contains any explicit words in the lyrics.

    :param audio: MP4 audio file.
    :return: Rating on whether it contains any explicit words.
    """
    lyrics = str(audio[MP4Tags.lyrics]).lower()
    if any(word in lyrics for word in explicit_words):
        return MP4Rating.EXPLICIT
    else:
        return MP4Rating.CLEAN
