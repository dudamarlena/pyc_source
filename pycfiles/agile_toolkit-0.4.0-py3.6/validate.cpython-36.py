# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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