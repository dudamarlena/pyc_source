# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\pycake\src\pycake\cli.py
# Compiled at: 2018-11-08 02:23:02
# Size of source mod 2**32: 1096 bytes
from __future__ import absolute_import
import click, crayons
from .meta import __version__
from .options import CONTEXT_SETTINGS, PyCakeGroup
from .cli_utils import format_help

@click.group(cls=PyCakeGroup, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name=crayons.yellow('pycake', bold=True), version=__version__)
@click.pass_context
def cli(ctx, **kwargs):
    if ctx.invoked_subcommand is None:
        click.echo(format_help(ctx.get_help()))


@cli.command(short_help='Prepare all the stuff to start new Python project.', context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
def prepare(ctx, **kwargs):
    from .commands import prepare
    project_dir = prepare()
    click.echo('\n\nThe target project is: {}\n'.format(project_dir))
    click.echo('You should run follow command first: {}\n'.format(crayons.yellow('make init', bold=True)))


if __name__ == '__main__':
    cli()