# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/cli/test.py
# Compiled at: 2020-03-13 12:49:48
# Size of source mod 2**32: 1879 bytes
import subprocess as sp, yaml
from pathlib import Path
import click

def testkraken_specs(workflow_path):
    """reading spec.yml and creating testkraken yml file"""
    with (workflow_path / 'spec.yml').open() as (f):
        params = yaml.safe_load(f)
    params_tkraken = params['test']
    fixed_envs_tkraken = params_tkraken.get('fixed_env', [])
    fixed_envs_tkraken.append(params['build']['required_env'])
    params_tkraken['fixed_env'] = fixed_envs_tkraken
    if params.get('post_build', None):
        params_tkraken['post_build'] = params['post_build']
    else:
        params_tkraken['post_build'] = {}
        params_tkraken['post_build']['copy'] = ['.', '/nfm']
        params_tkraken['post_build']['miniconda'] = {'pip_install': ['niflow-manager', '/nfm/package/']}
    with (workflow_path / 'testkraken_spec.yml').open('w') as (f):
        yaml.dump(params_tkraken, f, default_flow_style=False, sort_keys=False)


def testkraken_run(workflow_path, working_dir=None):
    if working_dir:
        sp.run(['testkraken', workflow_path, '-w', working_dir], check=True)
    else:
        sp.run(['testkraken', workflow_path], check=True)


@click.argument('workflow_path', type=(click.Path()), default='.')
@click.option('-w',
  '--working-dir',
  type=(click.Path()),
  help='Working directory, default is a temporary directory.')
def test(workflow_path, working_dir=None):
    print(f"testing {workflow_path}")
    testkraken_specs(workflow_path=(Path(workflow_path)))
    testkraken_run(workflow_path=workflow_path, working_dir=working_dir)