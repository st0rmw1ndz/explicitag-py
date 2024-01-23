from pathlib import Path
from typing import List

import click

from explicitag import __version__
from explicitag.explicitag import flatten_paths, process_files_in_parallel


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
@click.pass_context
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
def cli(ctx: click.Context, paths: List[Path]) -> None:
    """An MP4 rating tagger based on lyrics.

    Copyright (c) 2024 frosty.
    """
    if not paths:
        click.echo(cli.get_help(ctx))
        ctx.exit(1)
    files = flatten_paths(paths)
    process_files_in_parallel(files)
