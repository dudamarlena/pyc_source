# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/__main__.py
# Compiled at: 2019-11-20 10:29:37
""" __main__.py
~~~~~~~~~~~~~~~~~~~~
Called when multiqc namespace is used, primarily by the cli:

$ multiqc .
$ python -m multiqc .
"""
from __future__ import print_function
import click, pkg_resources
from . import multiqc
from .utils import config

def modify_usage_error(main_command):
    """ Function to modify the default click error handling.
    Used here to tell the user about how to find additional help.
    With thanks to this Stack Overflow answer: http://stackoverflow.com/a/43922088/713980
    :param main_command: top-level group or command object constructed by click wrapper
    :return: None
    """

    def show(self, file=None):
        if file is None:
            file = click._compat.get_text_stderr()
        color = None
        if self.ctx is not None:
            color = self.ctx.color
            click.utils.echo(self.ctx.get_usage() + '\n', file=file, color=color)
        click.utils.echo(("Error: %s\n\nThis is MultiQC v{}\n\nFor more help, run 'multiqc --help' or visit http://multiqc.info\n").format(config.version) % self.format_message(), file=file, color=color)
        return

    click.exceptions.UsageError.show = show
    return


if __name__ == '__main__' or __name__ == 'multiqc.__main__':
    for entry_point in pkg_resources.iter_entry_points('multiqc.cli_options.v1'):
        opt_func = entry_point.load()
        multiqc.run_cli = opt_func(multiqc.run_cli)

    modify_usage_error(multiqc.run_cli)
    multiqc.run_cli(prog_name='multiqc')