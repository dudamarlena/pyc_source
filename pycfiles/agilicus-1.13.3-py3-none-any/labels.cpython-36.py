# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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