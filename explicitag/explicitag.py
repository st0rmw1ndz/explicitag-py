import threading
from pathlib import Path
from typing import List

import click
from mutagen.mp4 import MP4, MP4StreamInfoError

from explicitag.data import MP4Rating, MP4Tags
from explicitag.mp4 import is_explicit_lyrics, mark_rating


def flatten_paths(paths_list: List[Path]) -> List[Path]:
    """Flattens a directory structure into a single file list.

    :param files_list: List of paths to flatten (files or directories).
    :return: Flattened file list as a list of Path objects.
    """
    file_list = []

    for path in paths_list:
        path_obj = Path(path)

        if path_obj.is_dir():
            for file_path in path_obj.rglob("*"):
                if file_path.is_file():
                    file_list.append(file_path)
        elif path_obj.is_file():
            file_list.append(path_obj)

    return file_list


def process_files(files: List[Path]) -> None:
    skipped = 0

    def process_file(file: Path) -> None:
        nonlocal skipped
        try:
            audio = MP4(file)
        except MP4StreamInfoError:
            click.echo(f"Skipping '{file.name}': not an MP4 file.")
            skipped += 1
            return
        except Exception as e:
            click.echo(f"Skipped '{file.name}':\n{e}")
            skipped += 1
            return

        if MP4Tags.lyrics not in audio:
            rating = MP4Rating.CLEAN
        else:
            rating = is_explicit_lyrics(audio)

        mark_rating(audio, rating)
        click.echo(
            f"Marked '{file.name}' as "
            f"{'explicit' if rating is MP4Rating.EXPLICIT else 'clean'}."
        )

    for file in files:
        process_file(file)

    click.echo(f"{len(files)} files processed. {skipped} files skipped.")
