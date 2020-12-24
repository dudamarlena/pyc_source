# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/github/labels.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 886 bytes
import click
from ..api import GithubApi
from ..utils import CommandError

@click.command()
@click.pass_context
def labels(ctx):
    """Crate or update labels in github
    """
    config = ctx.obj['agile']
    repos = config.get('repositories')
    labels = config.get('labels')
    if not isinstance(repos, list):
        raise CommandError('You need to specify the "repos" list in the config')
    if not isinstance(labels, dict):
        raise CommandError('You need to specify the "labels" dictionary in the config')
    git = GithubApi()
    for repo in repos:
        repo = git.repo(repo)
        for label, color in labels.items():
            if repo.label(label, color):
                click.echo('Created label "%s" @ %s' % (label, repo))
            else:
                click.echo('Updated label "%s" @ %s' % (label, repo))