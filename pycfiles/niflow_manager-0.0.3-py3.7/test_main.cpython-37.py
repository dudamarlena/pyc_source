# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/cli/tests/test_main.py
# Compiled at: 2020-03-13 12:49:48
# Size of source mod 2**32: 1796 bytes
import pytest
from click.testing import CliRunner
from pathlib import Path
import subprocess as sp
from .. import main

@pytest.mark.parametrize('option', ['--help', '--version'])
def test_utility_options(option):
    runner = CliRunner()
    result = runner.invoke(main, [option])
    assert result.exit_code == 0


@pytest.mark.parametrize('command', ['test', 'install', 'build'])
def test_commads_help(command):
    runner = CliRunner()
    result = runner.invoke(main, [command, '--help'])
    assert result.exit_code == 0


def test_default_python():
    """ initilize a niflow for python, and build/test a container using the default spec"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        res_init = runner.invoke(main, ['init', '--language', 'python', 'wf'], '\n'.join(['org', 'wf', 'y']))
        niflow_path = Path.cwd() / 'niflow-org-wf'
        spec_path = niflow_path / 'spec.yml'
        assert res_init.exit_code == 0
        assert spec_path.exists()
        res_build = runner.invoke(main, ['build', str(niflow_path)])
        assert res_build.exit_code == 0
        dockerrun = sp.run([
         'docker', 'run', '--rm', 'nfm-niflow-org-wf:latest'],
          stdout=(sp.PIPE),
          stderr=(sp.PIPE))
        assert dockerrun.returncode == 0
        res_test = runner.invoke(main, ['test', str(niflow_path)])
        assert res_test.exit_code == 0
        working_dir = Path.cwd() / 'output'
        res_test_w = runner.invoke(main, ['test', '-w', str(working_dir), str(niflow_path)])
        assert res_test_w.exit_code == 0
        assert (working_dir / 'output_all.csv').exists()