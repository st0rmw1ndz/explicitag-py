import argparse
import os
from pathlib import Path


def flatten_files_list(files_list: list[str]) -> list[str]:
    """Flattens a list of files, directories, and subdirectories into a single list of files.

    :param files_list: List of files, directories, and subdirectories
    :return: Flattened list of files
    """

    flattened_list = []
    for item in files_list:
        if isinstance(item, list):
            flattened_list.extend(flatten_files_list(item))
        else:
            flattened_list.append(item)
    return flattened_list


def validate_path_format(input_path: str) -> list[str]:
    """Validates the input path format and returns a list of files to process.

    Accepts a path to a file or directory.

    :param input_path: Path to a file or directory
    :return: List of files to process
    """

    input_path = input_path.strip("'\"")
    input_path = os.path.expanduser(input_path)

    if os.path.isdir(input_path):
        path_obj: Path = Path(input_path)
        files_list = [str(file) for file in path_obj.glob("*") if file.is_file()]
    elif os.path.isfile(input_path):
        files_list = [input_path]
    else:
        raise argparse.ArgumentTypeError(f'"{input_path}" is not a valid path.')

    return flatten_files_list(files_list)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="explicitag",
        description="MP4 rating tagger based on lyrics",
        epilog="Source code: https://codeberg.org/frosty/explicitag",
    )
    parser.add_argument(
        "path",
        help="file or directory to process",
        nargs="+",
        type=validate_path_format,
    )
    args: argparse.Namespace = parser.parse_args()
    args.path = flatten_files_list(args.path)
    return args
