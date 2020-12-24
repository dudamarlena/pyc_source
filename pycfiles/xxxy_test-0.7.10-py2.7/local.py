# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/development/local.py
# Compiled at: 2019-02-14 01:20:52
import click, russell
from russell.log import configure_logger
from russell.main import check_cli_version, add_commands

@click.group()
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
def cli(verbose):
    """
    Russell CLI interacts with Russell server and executes your commands.
    More help is available under each command listed below.
    """
    russell.russell_host = 'http://localhost:5000'
    russell.russell_web_host = 'https://lianxi.xiaoxiangxueyuan.com'
    configure_logger(verbose)
    check_cli_version()


add_commands(cli)