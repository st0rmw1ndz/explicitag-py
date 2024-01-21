import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from functools import partial
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


def process_file(file: Path, skipped: multiprocessing.Value) -> None:
    """The process ran on every MP4 file.

    First, it tries to read the stream as MP4 data, then checks if it has any
    lyrics, and if it does, it checks if there are any explicit words in them.
    Lastly, it marks the rating accordingly.

    :param file: Path to MP4 file to process.
    :param skipped: Amount of files skipped.
    """
    try:
        audio = MP4(file)
    except MP4StreamInfoError:
        click.echo(f"Skipping '{file.name}': not an MP4 file.")
        with skipped.get_lock():
            skipped.value += 1
        return

    except Exception as e:
        click.echo(f"Skipped '{file.name}':\n{e}")
        with skipped.get_lock():
            skipped.value += 1
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


def process_files_in_parallel(files: List[Path]) -> None:
    """Processes a list of files in parallel using multithreading.

    :param files: List of files to process.
    """
    skipped = multiprocessing.Value("i", 0)

    with ThreadPoolExecutor() as executor:
        process_file_partial = partial(process_file, skipped=skipped)
        executor.map(process_file_partial, files)

    click.echo(f"\nComplete. {skipped.value} files skipped.")
