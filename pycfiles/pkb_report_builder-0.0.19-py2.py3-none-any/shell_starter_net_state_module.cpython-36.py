# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\Github\MobileHR\MobileHR.Mario.Engine\MobileHR.Mario.Engine\modules\shell_starter_modules\shell_starter_net_state_module.py
# Compiled at: 2018-12-10 13:04:31
# Size of source mod 2**32: 316 bytes
import click, modules.net_state_modules.net_state_module as ns_module

@click.group()
def net_stats_commands_cli():
    pass


@net_stats_commands_cli.command()
def get_net_state():
    try:
        click.echo(ns_module.get_net_state_info())
    except Exception as e:
        pass