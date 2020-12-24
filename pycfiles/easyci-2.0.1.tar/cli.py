# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/naphatkrit/Dropbox/Documents/code/easyci/easyci/cli.py
# Compiled at: 2015-09-07 18:03:35
import click, easyci
from easyci.commands.clear_history import clear_history
from easyci.commands.gc import gc
from easyci.commands.init import init
from easyci.commands.test import test
from easyci.commands.watch import watch
from easyci.vcs.git import GitVcs
from easyci.version import get_installed_version, VersionNotInstalledError
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=easyci.__version__, prog_name='EasyCI')
@click.pass_context
def cli(ctx):
    git = GitVcs()
    if ctx.args[0] != 'init':
        try:
            version = get_installed_version(git)
        except VersionNotInstalledError:
            click.echo('Please run `eci init` first.')
            ctx.abort()

        if version != easyci.__version__:
            click.echo('EasyCI version mismatch. Please rerun `eci init`.')
            ctx.abort()
    ctx.obj = dict()
    ctx.obj['vcs'] = git


cli.add_command(clear_history)
cli.add_command(gc)
cli.add_command(init)
cli.add_command(test)
cli.add_command(watch)