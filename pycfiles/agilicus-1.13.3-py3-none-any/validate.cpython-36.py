# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/github/validate.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 409 bytes
import click
from ..repo import RepoManager

@click.command()
@click.option('--sandbox',
  is_flag=True, help='Validate only on sandbox/deploy branch',
  default=False)
@click.pass_context
def validate(ctx, sandbox):
    """Check if version of repository is semantic
    """
    m = RepoManager(ctx.obj['agile'])
    if not sandbox or m.can_release('sandbox'):
        click.echo(m.validate_version())