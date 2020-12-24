# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/cli/default/formats.py
# Compiled at: 2019-05-20 06:22:43
# Size of source mod 2**32: 851 bytes
"""CLI to format drivers."""
import click
from mapchete.cli import utils
from mapchete.formats import available_input_formats, available_output_formats

@click.command(help='List available input and/or output formats.')
@utils.opt_input_formats
@utils.opt_output_formats
@utils.opt_debug
def formats(input_formats, output_formats, debug=False):
    """List input and/or output formats."""
    if input_formats == output_formats:
        show_inputs, show_outputs = (True, True)
    else:
        show_inputs, show_outputs = input_formats, output_formats
    if show_inputs:
        click.echo('input formats:')
        for driver in available_input_formats():
            click.echo('- %s' % driver)

    if show_outputs:
        click.echo('output formats:')
        for driver in available_output_formats():
            click.echo('- %s' % driver)