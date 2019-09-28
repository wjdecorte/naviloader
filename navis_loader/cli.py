""" Navis Loader CLI """
import random

import click

from navis_loader.loader import process_files


@click.group()
def main():
    """ main """
    pass


@main.command()
@click.argument(
    "data_directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True, resolve_path=True),
)
@click.option("--file-count", default=1, help="Number of files to create")
@click.option("--file-prefix", default="file_", help="Prefix of file name")
@click.option("--record-count", default=0, help="Number of records per file (0=random)")
@click.option("--make-duplicates", is_flag=True, help="T/F: add duplicate records")
def sample(data_directory, file_count, file_prefix, record_count, make_duplicates):
    """ Create one or more sample files """
    from navis_loader.create_sample_data import create_file

    for i in range(file_count):
        if record_count == 0:
            record_count = random.randint(1, 1000)
        create_file(
            record_count, data_directory, f"{file_prefix}_{str(i)}", make_duplicates
        )


@main.command()
@click.argument(
    "source_data_directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True, resolve_path=True),
)
@click.argument(
    "target_data_directory",
    type=click.Path(dir_okay=True, file_okay=False, exists=True, resolve_path=True),
)
@click.option("-d", "--daemon", is_flag=True, help="Run in daemon mode (def: False)")
@click.option(
    "-e", "--file-extension", default="json", help="Source file extension (def: json)"
)
def loader(
    source_data_directory: str,
    target_data_directory: str,
    daemon: bool,
    file_extension: str,
):
    """ Load data files """
    if daemon:
        # todo: add continuous loop with interrupt/signal watch
        pass
    else:
        process_files(source_data_directory, target_data_directory, file_extension)
