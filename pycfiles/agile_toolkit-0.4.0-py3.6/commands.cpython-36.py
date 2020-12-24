# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/commands.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 1116 bytes
import os, json
from dotenv import load_dotenv
load_dotenv()
import click
from . import __version__
from .github import git
from .kong import kong
AGILE_CONFIG = os.environ.get('AGILE_CONFIG', 'agile.json')

@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug',
  is_flag=True,
  default=False,
  help='Run in debug mode')
@click.option('--version',
  is_flag=True,
  default=False,
  help='Display version and exit')
@click.option('--config',
  default=AGILE_CONFIG, type=(click.Path()),
  help=f"Agile configuration json file location ({AGILE_CONFIG})")
@click.pass_context
def start(ctx, debug, version, config):
    """Commands for devops operations"""
    ctx.obj = {}
    ctx.DEBUG = debug
    if os.path.isfile(config):
        with open(config) as (fp):
            agile = json.load(fp)
    else:
        agile = {}
    ctx.obj['agile'] = agile
    if version:
        click.echo(__version__)
        ctx.exit(0)
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())


start.add_command(git)
start.add_command(kong)