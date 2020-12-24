# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/nodeinfo.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2315 bytes
"""Node info sproc module."""
import logging, os, socket, click
from treadmill import cli
from treadmill import context
from treadmill import sysinfo
from treadmill import utils
from treadmill import zkutils
from treadmill import zknamespace as z
from treadmill import rest
from treadmill.rest import api
from treadmill.rest import error_handlers
_LOGGER = logging.getLogger(__name__)
_SERVERS_ACL = zkutils.make_role_acl('servers', 'rwcd')

def init():
    """Top level command handler."""

    @click.command()
    @click.option('-r', '--register', required=False, default=False, is_flag=True, help='Register as /nodeinfo in Zookeeper.')
    @click.option('-p', '--port', required=False, default=0)
    @click.option('-a', '--auth', type=click.Choice(['spnego']))
    @click.option('-m', '--modules', help='API modules to load.', required=False, type=cli.LIST)
    @click.option('-t', '--title', help='API Doc Title', default='Treadmill Nodeinfo REST API')
    @click.option('-c', '--cors-origin', help='CORS origin REGEX')
    def server(register, port, auth, modules, title, cors_origin):
        """Runs nodeinfo server."""
        if port == 0:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', 0))
            port = sock.getsockname()[1]
            sock.close()
        hostname = sysinfo.hostname()
        hostport = '%s:%s' % (hostname, port)
        if register:
            zkclient = context.GLOBAL.zk.conn
            zkclient.add_listener(zkutils.exit_on_lost)
            appname = 'root.%s#%010d' % (hostname, os.getpid())
            path = z.path.endpoint(appname, 'tcp', 'nodeinfo')
            _LOGGER.info('register endpoint: %s %s', path, hostport)
            zkutils.create(zkclient, path, hostport, acl=[
             _SERVERS_ACL], ephemeral=True)
        _LOGGER.info('Starting nodeinfo server on port: %s', port)
        utils.drop_privileges()
        api_paths = []
        if modules:
            api_paths = api.init(modules, title.replace('_', ' '), cors_origin)
        rest_server = rest.RestServer(port)
        rest_server.run(auth_type=auth, protect=api_paths)

    return server