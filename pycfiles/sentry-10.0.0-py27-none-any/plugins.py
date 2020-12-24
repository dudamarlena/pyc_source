# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/commands/plugins.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import click

@click.group()
def plugins():
    """Manage Sentry plugins."""
    pass


@plugins.command()
def list():
    """List all installed plugins"""
    from pkg_resources import iter_entry_points
    for ep in iter_entry_points('sentry.plugins'):
        click.echo('%s: %s %s (%s)' % (ep.name, ep.dist.project_name, ep.dist.version, ep.dist.location))