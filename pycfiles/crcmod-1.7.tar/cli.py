# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/crcli/scripts/cli.py
# Compiled at: 2016-02-17 23:11:58
__doc__ = '\nMain click group for CLI\n'
import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points
import crcli

@with_plugins(ep for ep in list(iter_entry_points('crcli.crcli_commands')))
@click.group()
@click.pass_context
def main_group(ctx):
    """This is the command line interface to the collective-reaction database.
    """
    ctx.obj = {}