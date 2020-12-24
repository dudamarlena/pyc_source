# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\shell_starter_modules\shell_starter_module.py
# Compiled at: 2019-01-15 04:22:34
# Size of source mod 2**32: 501 bytes
from models.settings import config
import click, modules.shell_starter_modules.shell_starter_net_state_module as ns_module, modules.shell_starter_modules.shell_starter_general_module as general_module, modules.shell_starter_modules.shell_starter_data_parse_module as parse_module
cli = click.CommandCollection(sources=[
 general_module.general_commands_cli,
 ns_module.net_stats_commands_cli,
 parse_module.data_parse_commands_cli])