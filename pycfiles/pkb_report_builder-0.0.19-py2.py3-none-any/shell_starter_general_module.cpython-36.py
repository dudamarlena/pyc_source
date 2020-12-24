# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\MobileHR\MobileHR.Mario.Engine\MobileHR.Mario.Engine\modules\shell_starter_modules\shell_starter_general_module.py
# Compiled at: 2018-12-11 09:04:26
# Size of source mod 2**32: 959 bytes
import click, models.settings.config as config

@click.group()
def general_commands_cli():
    pass


@general_commands_cli.command()
def version():
    click.echo(config.version_code)


@general_commands_cli.command()
def build_version():
    click.echo(config.build_version_code)


@general_commands_cli.command()
def info():
    config.show_system_info()


@general_commands_cli.command()
def version_name():
    try:
        click.echo(config.get_version_name())
    except Exception as e:
        click.echo(str(e))


@general_commands_cli.command()
@click.option('--name', required=True, type=str)
@click.option('--age', required=False, type=int)
def input_params(name, age):
    click.echo('Name = ' + name + '; age = ' + str(age))