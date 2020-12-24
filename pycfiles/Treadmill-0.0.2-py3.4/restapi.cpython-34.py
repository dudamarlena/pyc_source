# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/restapi.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 1119 bytes
"""Implementation of treadmill API server plugin."""
import click
from .. import rest
from .. import context
from .. import zkutils
from treadmill import cli
from treadmill.rest import api
from treadmill.rest import error_handlers

def init():
    """Return top level command handler."""

    @click.command()
    @click.option('-p', '--port', required=True)
    @click.option('-a', '--auth', type=click.Choice(['spnego']))
    @click.option('-t', '--title', help='API Doc Title', default='Treadmill REST API')
    @click.option('-m', '--modules', help='API modules to load.', required=True, type=cli.LIST)
    @click.option('-c', '--cors-origin', help='CORS origin REGEX', required=True)
    def top(port, auth, title, modules, cors_origin):
        """Run Treadmill API server."""
        context.GLOBAL.zk.conn.add_listener(zkutils.exit_on_lost)
        api_paths = api.init(modules, title.replace('_', ' '), cors_origin)
        rest_server = rest.RestServer(port)
        rest_server.run(auth_type=auth, protect=api_paths)

    return top