# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/github/remote.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 277 bytes
import click
from ..utils import command
from ..repo import RepoManager

@click.command()
@click.pass_context
def remote(ctx):
    """Display repo github path
    """
    with command():
        m = RepoManager(ctx.obj['agile'])
        click.echo(m.github_repo().repo_path)