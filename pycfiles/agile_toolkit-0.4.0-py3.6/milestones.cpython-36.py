# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/github/milestones.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 1338 bytes
import click
from ..api import GithubApi
from .utils import get_repos

@click.command()
@click.pass_context
@click.option('--list',
  is_flag=True, help='list open milestones',
  default=False)
@click.option('--close', help='milestone to close', default='')
def milestones(ctx, list, close):
    """View/edit/close milestones on github
    """
    repos = get_repos(ctx.parent.agile.get('labels'))
    if list:
        _list_milestones(repos)
    else:
        if close:
            click.echo('Closing milestones "%s"' % close)
            _close_milestone(repos, close)
        else:
            click.echo(ctx.get_help())


def _list_milestones(repos):
    git = GithubApi()
    milestones = set()
    for repo in repos:
        repo = git.repo(repo)
        stones = repo.milestones.get_list()
        milestones.update(data['title'] for data in stones)

    for title in sorted(milestones):
        click.echo(title)


def _close_milestone(repos, milestone):
    git = GithubApi()
    for repo in repos:
        repo = git.repo(repo)
        _close_repo_milestone(repo, milestone)


def _close_repo_milestone(repo, milestone):
    milestones = repo.milestones.get_list()
    for m in milestones:
        if m['title'] == milestone:
            repo.milestones.update(m, {'state': 'closed'})
            click.echo('Closed milestone %s' % m['html_url'])