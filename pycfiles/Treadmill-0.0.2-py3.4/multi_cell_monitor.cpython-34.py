# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/cli/supervise/multi_cell_monitor.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 3659 bytes
"""Implementation of treadmill admin master CLI plugin"""
import logging, time, urllib.request, urllib.parse, urllib.error, click
from treadmill import cli
from treadmill import context
from treadmill import restclient
from treadmill import utils
_LOGGER = logging.getLogger(__name__)
_DEFAULT_INTERVAL = '1m'

def _count(cell, appname):
    """Get number of instances scheduled/running on the cell."""
    try:
        ctx = context.Context()
        ctx.cell = cell
        ctx.dns_domain = context.GLOBAL.dns_domain
        stateapi = ctx.state_api()
        url = '/state/?' + urllib.parse.urlencode([('match', appname)])
        response = restclient.get(stateapi, url)
        state = response.json()
        for instance in state:
            _LOGGER.info('cell: %s - %s %s %s', cell, instance['name'], instance['state'], instance['host'])

        return len([instance for instance in state if instance['state'] == 'running'])
    except Exception:
        _LOGGER.exception('Unable to get instance count for cell %s, app: %s', cell, appname)
        return 0


def _configure_monitor(name, count):
    """Configure target count for the current cell."""
    _LOGGER.info('configuring monitor: %s, count: %s', name, count)
    url = '/app-monitor/%s' % name
    restapi = context.GLOBAL.cell_api()
    data = {'count': count}
    try:
        _LOGGER.debug('Creating app monitor: %s', name)
        restclient.post(restapi, url, payload=data)
    except restclient.AlreadyExistsError:
        _LOGGER.debug('Updating app monitor: %s', name)
        restclient.put(restapi, url, payload=data)


def init():
    """Return top level command handler"""

    @click.command()
    @click.option('--cell', required=True, envvar='TREADMILL_CELL', callback=cli.handle_context_opt, expose_value=False)
    @click.option('--monitor', nargs=2, type=click.Tuple([str, int]), multiple=True, required=True)
    @click.option('--once', help='Run once.', is_flag=True, default=False)
    @click.option('--interval', help='Wait interval between checks.', default=_DEFAULT_INTERVAL)
    @click.argument('name')
    def controller(monitor, once, interval, name):
        """Control app monitors across cells"""
        monitors = list(monitor)
        while True:
            intended_total = 0
            actual_total = 0
            intended = 0
            for cellname, count in monitors:
                if cellname == context.GLOBAL.cell:
                    intended = count
                else:
                    actual = _count(cellname, name)
                    _LOGGER.info('state for cell %s, actual: %s, intended: %s', cellname, actual, count)
                    intended_total += count
                    actual_total += actual

            missing = intended_total - actual_total
            my_count = intended + max(0, missing)
            _LOGGER.info('intended: %s, actual: %s, missing: %s, my count: %s', intended_total, actual_total, missing, my_count)
            _configure_monitor(name, my_count)
            if once:
                break
            time.sleep(utils.to_seconds(interval))

    return controller