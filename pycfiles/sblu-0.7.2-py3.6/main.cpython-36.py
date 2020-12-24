# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/cli/main.py
# Compiled at: 2019-10-14 18:28:00
# Size of source mod 2**32: 603 bytes
import click
from . import make_cli_class, setup_for_command_line
from ..version import version
from .util import config

def make_subcommand(package):

    @click.command(package, cls=(make_cli_class(package)))
    def cli():
        pass

    return cli


@click.group('sblu')
@click.option('-v', '--verbose', count=True)
@click.version_option(version=version)
def cli(verbose):
    setup_for_command_line(verbose)


for subcommand in ('pdb', 'docking', 'measure', 'cluspro', 'ftmap', 'atlas', 'xyztraj'):
    sub_cli = make_subcommand(subcommand)
    cli.add_command(sub_cli)

cli.add_command(config)