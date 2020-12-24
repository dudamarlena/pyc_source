# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thinman/__main__.py
# Compiled at: 2015-04-06 17:43:23
""" Command line interface.
"""
from __future__ import absolute_import, unicode_literals, print_function
import os, re, sys, click
__app_name__ = b'thin-man'
CONTEXT_SETTINGS = dict(help_option_names=[
 b'-h', b'--help'])
try:
    CLI_PATH = sys.modules[b'__main__'].__file__
except (KeyError, AttributeError):
    CLI_PATH = __file__

CLI_PATH = os.path.dirname(CLI_PATH)
if CLI_PATH.endswith(b'/bin'):
    CLI_PATH = CLI_PATH[:-4]
CLI_PATH = re.sub(b'^' + os.path.expanduser(b'~'), b'~', CLI_PATH)
VERSION_INFO = (b'%(prog)s %(version)s from {} [Python {}]').format(CLI_PATH, (b' ').join(sys.version.split()[:1]))

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(message=VERSION_INFO)
@click.option(b'-q', b'--quiet', is_flag=True, default=False, help=b'Be quiet (show only errors).')
@click.option(b'-v', b'--verbose', is_flag=True, default=False, help=b'Create extra verbose output.')
@click.pass_context
def cli(ctx, version=False, quiet=False, verbose=False):
    """'thin-man' command line tool."""
    appdir = click.get_app_dir(__app_name__)


@cli.command(name=b'help')
def help_command():
    """Print some helpful message."""
    click.echo(b'Helpful message.')


if __name__ == b'__main__':
    __package__ = b'thinman'
    cli()