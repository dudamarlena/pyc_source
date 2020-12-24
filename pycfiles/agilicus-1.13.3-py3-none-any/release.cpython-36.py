# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/github/release.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 1176 bytes
import click
from ..utils import niceJson
from ..repo import RepoManager

@click.command()
@click.pass_context
@click.option('--yes',
  is_flag=True, help='Commit changes to github',
  default=False)
@click.option('--latest',
  is_flag=True, help='Show latest release in github',
  default=False)
def release(ctx, yes, latest):
    """Create a new release in github
    """
    m = RepoManager(ctx.obj['agile'])
    api = m.github_repo()
    if latest:
        latest = api.releases.latest()
        if latest:
            click.echo(latest['tag_name'])
    else:
        if m.can_release('sandbox'):
            branch = m.info['branch']
            version = m.validate_version()
            name = 'v%s' % version
            body = ['Release %s from agiletoolkit' % name]
            data = dict(tag_name=name,
              target_commitish=branch,
              name=name,
              body=('\n\n'.join(body)),
              draft=False,
              prerelease=False)
            if yes:
                data = api.releases.create(data=data)
                m.message('Successfully created a new Github release')
            click.echo(niceJson(data))
        else:
            click.echo('skipped')