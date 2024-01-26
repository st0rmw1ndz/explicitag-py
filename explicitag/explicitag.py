import asyncio
import re
from pathlib import Path
from typing import List, Tuple

import click
from mutagen.mp4 import MP4, MP4StreamInfoError

from explicitag.data import MP4Rating, MP4Tags, explicit_words
from explicitag.mp4 import is_explicit_lyrics, mark_rating


def flatten_paths(paths: List[Path]) -> List[Path]:
    """Flattens a directory structure into a single file list.

    :param files_list: List of paths to flatten (files or directories).
    :return: Flattened file list as a list of Path objects.
    """
    file_list = []

    for path in paths:
        path_obj = Path(path)

        if path_obj.is_dir():
            for file_path in path_obj.rglob("*"):
                if file_path.is_file():
                    file_list.append(file_path)
        elif path_obj.is_file():
            file_list.append(path_obj)

    return file_list


async def process_files(files: List[Path]) -> None:
    skipped = 0

    explicit_pattern = re.compile(
        r"\b(?:"
        + "|".join(re.escape(word) for word in explicit_words)
        + r")\b",
        re.IGNORECASE,
    )

    async def process_file(file: Path) -> Tuple[MP4, MP4Rating]:
        nonlocal skipped

        try:
            audio = MP4(file)
        except MP4StreamInfoError:
            click.echo(f"Skipping '{file.name}': not an MP4 file.")
            skipped += 1
            return None, None
        except Exception as e:
            click.echo(f"Skipped '{file.name}':\n{e}")
            skipped += 1
            return None, None

        if MP4Tags.lyrics not in audio:
            rating = MP4Rating.CLEAN
        else:
            rating = is_explicit_lyrics(audio, explicit_pattern)

        return audio, rating

    async def save_audio(audio: MP4) -> None:
        await asyncio.to_thread(audio.save)

    click.echo("Processing files...")

    results = await asyncio.gather(*[process_file(file) for file in files])

    for audio, rating in results:
        if audio is not None:
            mark_rating(audio, rating)
            click.echo(
                f"Marked '{Path(audio.filename).name}' as "
                f"{'explicit' if rating is MP4Rating.EXPLICIT else 'clean'}."
            )

    click.echo("Saving files...")

    await asyncio.gather(
        *[save_audio(audio) for audio, _ in results if audio is not None]
    )

    click.echo(f"{len(files)} files processed. {skipped} files skipped.")
