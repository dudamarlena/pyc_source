# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/cli/main.py
# Compiled at: 2019-11-29 07:51:51
# Size of source mod 2**32: 347 bytes
"""
Mapchete command line tool with subcommands.
"""
from pkg_resources import iter_entry_points
import click
from click_plugins import with_plugins
from mapchete import __version__

@with_plugins(iter_entry_points('mapchete.cli.commands'))
@click.version_option(version=__version__, message='%(version)s')
@click.group()
def main():
    pass