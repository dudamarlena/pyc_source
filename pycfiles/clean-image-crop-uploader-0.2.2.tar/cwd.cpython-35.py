# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/cwd.py
# Compiled at: 2018-03-24 01:59:03
# Size of source mod 2**32: 143 bytes
__doc__ = 'Cwd command.'
from pathlib import Path
import click

def show_cwd():
    """Show current directory."""
    click.echo(str(Path.cwd()))