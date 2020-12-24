# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/cli/default/processes.py
# Compiled at: 2020-03-05 08:05:20
# Size of source mod 2**32: 984 bytes
"""CLI to list processes."""
import click, logging
from mapchete.cli import utils
from mapchete.processes import process_names_docstrings
logger = logging.getLogger(__name__)

@click.command(help='List available processes.')
@click.option('--process_name', '-n', type=click.STRING, help='Print docstring of process.')
@utils.opt_debug
def processes(process_name=None, docstrings=False, debug=False):
    """List available processes."""
    processes = process_names_docstrings(process_name=process_name)
    click.echo('%s processes found' % len(processes))
    for process_info in processes:
        _print_process_info(process_info, print_docstring=process_name is not None)


def _print_process_info(process_info, print_docstring=False):
    name, docstring = process_info
    click.echo(click.style(name, bold=print_docstring, underline=print_docstring))
    if print_docstring:
        click.echo(docstring)