import argparse
import logging
import os

from mutagen.mp4 import MP4, MP4StreamInfoError

from .argparser import get_args
from .data import MP4Rating, MP4Tags
from .mp4 import get_display_text, is_explicit_lyrics, mark_rating

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main() -> int:
    args: argparse.Namespace = get_args()

    skipped: int = 0

    for file in args.path:
        file_name: str = os.path.basename(file)

        if not os.path.isfile(file):
            logger.debug(f'Skipping "{file_name}": file does not exist')
            continue

        try:
            audio: MP4 = MP4(file)
        except MP4StreamInfoError:
            logger.debug(f'Skipping "{file_name}": not an MP4 file')
            skipped += 1
            continue
        except Exception as e:
            logger.debug(f'Skipping "{file_name}": {e}')
            skipped += 1
            continue

        if MP4Tags.lyrics not in audio:
            logger.debug(f'Skipping "{get_display_text(audio)}": no lyrics')
            skipped += 1
            continue

        rating: MP4Rating = is_explicit_lyrics(audio)
        mark_rating(audio, rating)

        logger.info(
            f'Marked "{get_display_text(audio)}" as '
            f'{"explicit" if rating is MP4Rating.EXPLICIT else "clean"}'
        )

    print("Skipped", skipped)

    return 0
