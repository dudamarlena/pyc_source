# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tablemate/util/dclick.py
# Compiled at: 2015-04-12 20:22:55
""" ‘Double Click’ – Extensions to Click.
"""
from __future__ import absolute_import, unicode_literals, print_function
import os, re, click

def pretty_path(path, _home_re=re.compile(b'^' + re.escape(os.path.expanduser(b'~') + os.sep))):
    """Prettify path for humans, and make it Unicode."""
    path = click.format_filename(path)
    path = _home_re.sub(b'~' + os.sep, path)
    return path


def serror(message, *args, **kwargs):
    """Print a styled error message."""
    if args or kwargs:
        message = message.format(*args, **kwargs)
    return click.secho(message, fg=b'white', bg=b'red', bold=True)


class LoggedFailure(click.UsageError):
    """Report a failure condition to the user."""

    def __init__(self, message):
        message = click.style(message, fg=b'white', bg=b'red', bold=True)
        click.UsageError.__init__(self, message)


class AliasedGroup(click.Group):
    """ A command group with alias names.

        Inherit from this class and define a ``MAP`` class variable,
        which is a mapping from alias names to canonical command names.
        Then use that derived class as the ``cls`` parameter for a
        ``click.group`` decorator.
    """
    MAP = {}

    def get_command(self, ctx, cmd_name):
        """Map some aliases to their 'real' names."""
        cmd_name = self.MAP.get(cmd_name, cmd_name)
        return click.Group.get_command(self, ctx, cmd_name)