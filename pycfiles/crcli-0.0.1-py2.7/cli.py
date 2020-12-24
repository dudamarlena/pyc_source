# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/crcli/scripts/cli.py
# Compiled at: 2016-02-17 23:11:58
"""
Main click group for CLI
"""
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