# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: flaskdeploy/__main__.py
# Compiled at: 2018-12-17 07:59:25
# Size of source mod 2**32: 325 bytes
import click
from .scripts import deploy, generation

@click.group()
def cli():
    """A quick deploy script for productive flask app."""
    pass


cli.add_command(deploy.cli, 'deploy')
cli.add_command(generation.cli, 'gen')
if __name__ == '__main__':
    cli()