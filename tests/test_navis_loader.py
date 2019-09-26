from navis_loader import __version__
from click.testing import CliRunner
from navis_loader.cli import main


def test_version():
    assert __version__ == '0.1.0'

def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert result.output == "hello world\n"
