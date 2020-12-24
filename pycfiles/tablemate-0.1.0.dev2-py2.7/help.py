# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tablemate/commands/help.py
# Compiled at: 2015-04-12 20:22:55
""" 'help' command.
"""
from __future__ import absolute_import, unicode_literals, print_function
import os, click
from .. import config
from ..util.dclick import pretty_path

@config.cli.command(name=b'help')
@click.pass_context
def help_command(ctx):
    """Print some information on the system environment."""

    def banner(title):
        """Helper"""
        click.echo(b'')
        click.secho((b'~~~ {} ~~~').format(title), fg=b'green', bg=b'black', bold=True)

    app_name = ctx.find_root().info_name
    click.secho((b'*** "{}" Help & Information ***').format(app_name), fg=b'white', bg=b'blue', bold=True)
    banner(b'Version Information')
    click.echo(config.version_info(ctx))
    banner(b'Configuration')
    locations = config.locations(exists=False, extras=ctx.find_root().params.get(b'config', None))
    locations = [ (b'✔' if os.path.exists(i) else b'✘', pretty_path(i)) for i in locations ]
    click.echo((b'The following configuration files are merged in order, if they exist:\n    {0}').format((b'\n    ').join((b'{}   {}').format(*i) for i in locations)))
    banner(b'More Help')
    click.echo((b"Call '{} --help' to get a list of available commands & options.").format(app_name))
    click.echo((b"Call '{} «command» --help' to get help on a specific command.").format(app_name))
    click.echo((b"Call '{} --version' to get the above version information separately.").format(app_name))
    click.echo((b"Call '{} --license' to get licensing informatioon.").format(app_name))
    return