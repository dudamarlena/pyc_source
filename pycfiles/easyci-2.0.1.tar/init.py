# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/naphatkrit/Dropbox/Documents/code/easyci/easyci/commands/init.py
# Compiled at: 2015-09-08 20:10:34
import click, os, yaml, easyci
from easyci import locking
from easyci.hooks import hooks_manager
from easyci.utils import decorators
from easyci.version import set_installed_version

@click.command()
@click.pass_context
@decorators.print_markers
def init(ctx):
    """Initialize the project for use with EasyCI. This installs the necessary
    git hooks (pre-commit + pre-push) and add a config file if one does not
    already exists.
    """
    git = ctx.obj['vcs']
    click.echo('Installing hooks...', nl=False)
    for old in ['commit-msg']:
        path = os.path.join(git.path, '.git/hooks', old)
        if os.path.exists(path):
            os.remove(path)

    for new in ['pre-commit', 'pre-push']:
        git.install_hook(new, hooks_manager.get_hook(new))

    click.echo('Done.')
    config_path = os.path.join(git.path, 'eci.yaml')
    if not os.path.exists(config_path):
        click.echo('Placing a trivial config file in your project...', nl=False)
        with open(config_path, 'w') as (f):
            f.write(yaml.safe_dump({'tests': ['echo please modify to run your tests', 'true']}))
        click.echo('Done.')
    locking.init(git)
    click.echo('Updating installed version...', nl=False)
    set_installed_version(git, easyci.__version__)
    click.echo('Done.')