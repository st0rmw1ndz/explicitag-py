import argparse
import os
import sys
from typing import List

from loguru import logger
from mutagen.mp4 import MP4, MP4StreamInfoError  # noqa: I201

from .data import MP4Rating, MP4Tags
from .mp4 import is_explicit_lyrics, mark_rating


def setup_log_handlers() -> None:
    """Sets up the logging configuration, such as output format and level."""
    logger.remove()
    logger.add(
        sys.stdout,
        format="[{time:HH:mm:ss}] {level} - {message}",
        level="INFO",
    )


def flatten_paths(paths_list: List[str]) -> List[str]:
    """Flattens a directory structure into a single file list.

    :param files_list: List of paths to flatten (files or directories)
    :return: Flattened file list
    """
    file_list: List[str] = []

    for path in paths_list:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                file_list.extend([os.path.join(root, file) for file in files])
        elif os.path.isfile(path):
            file_list.append(path)

    return file_list


def get_args() -> argparse.Namespace:
    """Parses the command-line arguments and flattens the path(s) given.

    :return: Argparse namespace for the command-line arguments
    """
    parser = argparse.ArgumentParser(
        prog="explicitag",
        description="MP4 rating tagger based on lyrics",
        epilog="Source code: https://codeberg.org/frosty/explicitag",
    )
    parser.add_argument(
        "path",
        help="file or directory to process",
        nargs="+",
    )

    args: argparse.Namespace = parser.parse_args()
    args.path = flatten_paths(args.path)

    return args


def main() -> int:
    """Main function ran.

    :return: Exit code
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


if __name__ == "__main__":
    setup_log_handlers()
    sys.exit(main())
