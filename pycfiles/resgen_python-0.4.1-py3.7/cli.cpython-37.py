# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/resgen/cli.py
# Compiled at: 2020-03-22 19:12:26
# Size of source mod 2**32: 130 bytes
import click
from .sync import commands as sync_commands

@click.group()
def cli():
    pass


cli.add_command(sync_commands.sync)