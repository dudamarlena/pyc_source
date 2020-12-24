# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/cli/stop.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 985 bytes
"""Manage Treadmill app manifest."""
import click
from .. import cli
from treadmill import restclient
from treadmill import context

def init():
    """Return top level command handler."""

    @click.command()
    @click.option('--cell', required=True, envvar='TREADMILL_CELL', callback=cli.handle_context_opt, expose_value=False)
    @click.option('--api', required=False, help='API url to use.', metavar='URL', envvar='TREADMILL_RESTAPI')
    @click.argument('instances', nargs=-1)
    @cli.ON_REST_EXCEPTIONS
    def stop(api, instances):
        """Stop (unschedule, terminate) Treadmill instance(s)."""
        if not instances:
            return
        apis = context.GLOBAL.cell_api(api)
        response = restclient.post(apis, '/instance/_bulk/delete', payload=dict(instances=list(instances)))
        return response.json()

    return stop