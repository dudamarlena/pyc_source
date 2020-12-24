# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/main.py
# Compiled at: 2019-02-22 11:42:46
import click
from distutils.version import LooseVersion
import pkg_resources, russell
from russell.cli.auth import login, logout
from russell.cli.data import data
from russell.cli.experiment import delete, info, logs, output, status, stop
from russell.cli.run import run
from russell.cli.project import init, clone
from russell.client.version import VersionClient
from russell.client.service import ServiceClient
from russell.exceptions import RussellException
from russell.log import configure_logger
from russell.log import logger as russell_logger
from russell.cli.version import version, upgrade, check_cli_version

def print_version_callback(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    server_version = VersionClient().get_cli_version()
    current_version = pkg_resources.require('xxxy-test')[0].version
    click.echo(('Version: {}').format(current_version))
    click.echo(('Remote latest version: {}').format(server_version.latest_version))
    if LooseVersion(current_version) < LooseVersion(server_version.min_version):
        raise RussellException(('\n    Your version of CLI ({}) is no longer compatible with server. Run:\n        pip install -U xxxy-test\n    to upgrade to the latest version ({})\n                ').format(current_version, server_version.latest_version))
    if LooseVersion(current_version) < LooseVersion(server_version.latest_version):
        click.echo(('\n    New version of CLI ({}) is now available. To upgrade run:\n        pip install -U xxxy-test\n                ').format(server_version.latest_version))
    ctx.exit()


@click.group()
@click.option('-h', '--host', default=russell.russell_host, help='Russell server endpoint')
@click.option('-v', '--verbose', count=True, help='Turn on debug logging')
@click.option('--version', is_flag=True, callback=print_version_callback, expose_value=False, is_eager=True, help='Show version info')
def cli(host, verbose):
    """
    Russell CLI interacts with Russell server and executes your commands.
    More help is available under each command listed below.
    """
    russell.russell_host = host
    configure_logger(verbose)
    check_cli_version()
    check_server_status()


def check_server_status():
    """
    Check if russell cloud service status now
    """
    service = ServiceClient().get_service_status()
    if service.service_status <= 0:
        raise RussellException('\n            System is being maintained. Please wait until the end. \n        ')


def add_commands(cli):
    cli.add_command(data)
    cli.add_command(delete)
    cli.add_command(info)
    cli.add_command(init)
    cli.add_command(login)
    cli.add_command(logout)
    cli.add_command(logs)
    cli.add_command(output)
    cli.add_command(status)
    cli.add_command(stop)
    cli.add_command(run)
    cli.add_command(clone)
    cli.add_command(version)
    cli.add_command(upgrade)


add_commands(cli)