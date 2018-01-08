import click
from upmcli import cli
import logging
import os
from click.testing import CliRunner

from upmcli.package_specification import from_file

runner = CliRunner()
with runner.isolated_filesystem():
    result = runner.invoke(cli.main, ['init'],
                           input='test project\nferi,mehdi\ntesting for upm\n0.0.1\nn\nrun\nnpm start\nn')
    assert os.path.exists('upm.yml')
    specification = from_file(os.getcwd())
    assert specification.name == 'test project'
    assert specification.author == 'feri,mehdi'
    assert specification.description == 'testing for upm'
    assert specification.version == '0.0.1'
    assert specification.entrypoints['run'] == 'npm start'
    logging.debug(specification)
    logging.debug(result.output)
