# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\shell_starter_modules\shell_starter_data_parse_module.py
# Compiled at: 2019-01-15 04:21:05
# Size of source mod 2**32: 312 bytes
import click

@click.group()
def data_parse_commands_cli():
    pass


@data_parse_commands_cli.command()
@click.option('--file_name', required=True, type=str)
def get_data_from_file(file_name):
    click.echo('Name = ' + file_name)