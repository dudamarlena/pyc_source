# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/commands/django.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import click
from sentry.runner.decorators import configuration

@click.command(add_help_option=False, context_settings=dict(ignore_unknown_options=True))
@click.argument('management_args', nargs=-1, type=click.UNPROCESSED)
@configuration
@click.pass_context
def django(ctx, management_args):
    """Execute Django subcommands."""
    from django.core.management import execute_from_command_line
    execute_from_command_line(argv=[ctx.command_path] + list(management_args))