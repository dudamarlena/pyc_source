# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/commands/completion.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 1441 bytes
import click, click_completion, click_completion.core
from musicbot import helpers

@click.group(help='Shell completion', cls=(helpers.GroupWithHelp))
def cli():
    pass


@cli.command()
@click.option('-i', '--case-insensitive/--no-case-insensitive', help='Case insensitive completion')
@click.argument('shell', required=False, type=(click_completion.DocumentedChoice(click_completion.core.shells)))
def show(shell, case_insensitive):
    """Show the click-completion-command completion code"""
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    click.echo(click_completion.core.get_code(shell, extra_env=extra_env))


@cli.command()
@click.option('--append/--overwrite', help='Append the completion code to the file', default=None)
@click.option('-i', '--case-insensitive/--no-case-insensitive', help='Case insensitive completion')
@click.argument('shell', required=False, type=(click_completion.DocumentedChoice(click_completion.core.shells)))
@click.argument('path', required=False)
def install(append, case_insensitive, shell, path):
    """Install the click-completion-command completion"""
    extra_env = {'_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE': 'ON'} if case_insensitive else {}
    shell, path = click_completion.core.install(shell=shell, path=path, append=append, extra_env=extra_env)
    click.echo('%s completion installed in %s' % (shell, path))