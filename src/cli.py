import argparse
import os

from loguru import logger
from mutagen.mp4 import MP4, MP4StreamInfoError

from .argparser import get_args
from .data import MP4Rating, MP4Tags
from .mp4 import is_explicit_lyrics, mark_rating


def main() -> int:
    """Main function ran.

    :return: Return code
    """
    args: argparse.Namespace = get_args()

    skipped: int = 0

    for file in args.path:
        file_name: str = os.path.basename(file)

        if not os.path.isfile(file):
            logger.info(f'Skipping "{file_name}": file does not exist')
            skipped += 1
            continue

        try:
            audio: MP4 = MP4(file)
        except MP4StreamInfoError:
            logger.warning(f'Skipping "{file_name}": not an MP4 file')
            skipped += 1
            continue
        except Exception as e:
            logger.warning(f'Skipping "{file_name}": {e}')
            skipped += 1
            continue

        rating: MP4Rating
        if MP4Tags.lyrics not in audio:
            rating = MP4Rating.CLEAN
        else:
            rating = is_explicit_lyrics(audio)

        mark_rating(audio, rating)

        logger.info(
            f'Marked "{file_name}" as '
            f'{"explicit" if rating is MP4Rating.EXPLICIT else "clean"}'
        )

    print(f"\nComplete. {skipped} file(s) skipped.")

    return 0
