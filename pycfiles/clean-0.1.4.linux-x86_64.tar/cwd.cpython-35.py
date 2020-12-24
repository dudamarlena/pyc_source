# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/cwd.py
# Compiled at: 2018-03-24 01:59:03
# Size of source mod 2**32: 143 bytes
"""Cwd command."""
from pathlib import Path
import click

def show_cwd():
    """Show current directory."""
    click.echo(str(Path.cwd()))