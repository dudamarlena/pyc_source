# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/development/dev.py
# Compiled at: 2019-02-14 01:20:22
import click, russell
from russell.log import configure_logger
from russell.main import check_cli_version, add_commands, print_version_callback
from russell.cli.project import clone2
from russell.cli.data import *
from russell.cli.data import _upload
from russell.log import configure_logger
from russell.manager.auth_config import AuthConfigManager
from russell.manager.data_config import DataConfigManager
from russell.manager.experiment_config import ExperimentConfigManager

@click.group()
@click.option('--version', is_flag=True, callback=print_version_callback, expose_value=False, is_eager=True, help='Show version info')
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
def cli(verbose):
    """
    Russell CLI interacts with Russell server and executes your commands.
    More help is available under each command listed below.
    """
    russell.russell_host = 'https://top.xiaoxiangxueyuan.com'
    russell.russell_web_host = 'https://lianxi.xiaoxiangxueyuan.com'
    russell.russell_fs_host = 'fs.xiaoxiangxueyuan.com'
    russell.russell_fs_port = 443
    AuthConfigManager.CONFIG_FILE_PATH += '-dev'
    DataConfigManager.CONFIG_FILE_PATH += '-dev'
    ExperimentConfigManager.CONFIG_FILE_PATH += '-dev'
    configure_logger(verbose)
    check_cli_version()


add_commands(cli)
data.add_command(_upload)
cli.add_command(clone2)
cli.add_command(data)