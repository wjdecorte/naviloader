""" Test the Navis Loader CLI """
import os
import glob

from navis_loader import __version__
from click.testing import CliRunner
from navis_loader.cli import main
from navis_loader.create_sample_data import create_file


def test_version():
    assert __version__ == "0.1.0"


def test_main():
    """ Test Main group """
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Usage" in result.output


def test_create_sample_file():
    """ Test sample sub-command """
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["sample", os.getcwd(), "--file-count=3"])
        print(result.output)
        assert result.exit_code == 0
        file_list = glob.glob(os.path.join(os.getcwd(), "file_*"))
        assert len(file_list) == 3


def test_loader():
    """ Test loader sub-command """
    runner = CliRunner()
    with runner.isolated_filesystem():
        create_file(
            record_count=2,
            data_dir=os.getcwd(),
            filename="test_data",
            make_duplicates=False,
        )
        result = runner.invoke(main, ["loader", os.getcwd(), os.getcwd()])
        assert result.exit_code == 0
