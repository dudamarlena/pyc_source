# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/cli/monitor.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2459 bytes
"""Treadmill Application monitor CLI

Create, delete and manage app monitors.
"""
import logging, click
from treadmill import cli
from treadmill import context
from treadmill import restclient
_LOGGER = logging.getLogger(__name__)
_EXCEPTIONS = []
_EXCEPTIONS.extend(cli.REST_EXCEPTIONS)
_ON_EXCEPTIONS = cli.handle_exceptions(_EXCEPTIONS)
_REST_PATH = '/app-monitor/'

def init():
    """Configures application monitor"""
    formatter = cli.make_formatter(cli.AppMonitorPrettyFormatter)
    ctx = {}

    @click.group()
    @click.option('--cell', required=True, envvar='TREADMILL_CELL', callback=cli.handle_context_opt, expose_value=False)
    @click.option('--api', help='API url to use.', metavar='URL', envvar='TREADMILL_RESTAPI')
    def monitor_group(api):
        """Manage Treadmill app monitor configuration"""
        ctx['api'] = api

    @monitor_group.command()
    @click.option('-n', '--count', type=int, help='Instance count')
    @click.argument('name')
    @_ON_EXCEPTIONS
    def configure(count, name):
        """Configure application monitor"""
        restapi = context.GLOBAL.cell_api(ctx['api'])
        url = _REST_PATH + name
        if count is not None:
            data = {'count': count}
            try:
                _LOGGER.debug('Creating app monitor: %s', name)
                restclient.post(restapi, url, payload=data)
            except restclient.AlreadyExistsError:
                _LOGGER.debug('Updating app monitor: %s', name)
                restclient.put(restapi, url, payload=data)

        _LOGGER.debug('Retrieving app monitor: %s', name)
        monitor_entry = restclient.get(restapi, url)
        cli.out(formatter(monitor_entry.json()))

    @monitor_group.command(name='list')
    @_ON_EXCEPTIONS
    def _list():
        """List configured app monitors"""
        restapi = context.GLOBAL.cell_api(ctx['api'])
        response = restclient.get(restapi, _REST_PATH)
        cli.out(formatter(response.json()))

    @monitor_group.command()
    @click.argument('name', nargs=1, required=True)
    @_ON_EXCEPTIONS
    def delete(name):
        """Delete app monitor"""
        restapi = context.GLOBAL.cell_api(ctx['api'])
        url = _REST_PATH + name
        restclient.delete(restapi, url)

    del delete
    del _list
    del configure
    return monitor_group