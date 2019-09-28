""" Test the Navis Loader CLI """
import os
import glob

from navis_loader import __version__
from click.testing import CliRunner
from navis_loader.cli import main


def test_version():
    assert __version__ == "0.1.0"


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Usage" in result.output


def test_create_sample_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["sample", os.getcwd(), "--file-count=3"])
        print(result.output)
        assert result.exit_code == 0
        file_list = glob.glob(os.path.join(os.getcwd(), "file_*"))
        assert len(file_list) == 3
