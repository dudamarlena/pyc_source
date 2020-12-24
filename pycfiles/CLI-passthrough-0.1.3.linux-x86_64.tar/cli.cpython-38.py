# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nemo/miniconda3/envs/cli/lib/python3.8/site-packages/cli_passthrough/cli.py
# Compiled at: 2019-11-05 20:39:15
# Size of source mod 2**32: 931 bytes
import sys, click, pkg_resources
from . import cli_passthrough
from .utils import write_to_log
version = pkg_resources.get_distribution('cli-passthrough').version
CONTEXT_SETTINGS = {'ignore_unknown_options':True,  'allow_extra_args':True}

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i',
  '--interactive',
  is_flag=True,
  help='Prefixes command with "/bin/bash -i -c", effectively sourcing the .bashrc file. This may use any aliases set in your current env.')
@click.version_option(prog_name='cli-passthrough', version=version)
@click.pass_context
def cli(ctx, interactive):
    """Entry point
    """
    write_to_log('\nNEW CMD = {}'.format(' '.join(sys.argv)))
    write_to_log('\nNEW CMD = {}'.format(' '.join(sys.argv)), 'stderr')
    exit_status = cli_passthrough(' '.join(ctx.args), interactive)
    sys.exit(exit_status)


main = cli