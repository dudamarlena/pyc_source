# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/commands/help.py
# Compiled at: 2019-08-16 12:27:41
from __future__ import absolute_import, print_function
import click

@click.command()
@click.pass_context
def help(ctx):
    """Show this message and exit."""
    click.echo(ctx.parent.get_help())