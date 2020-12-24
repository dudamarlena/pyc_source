# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/init.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 7090 bytes
"""Treadmill initialization and server presence daemon.

This service register the node into the Treadmill cell and, as such, is
responsible for publishing the node's capacity to the scheduler.

This service is also responsible for shutting down the node, when necessary or
requested, by disabling all traffic from and to the containers.
"""
import logging, os, threading, time, click, kazoo
from .. import appmgr
from .. import context
from .. import exc
from .. import sysinfo
from .. import utils
from .. import zknamespace as z
from .. import zkutils
from ..appmgr import initialize as app_initialize
if os.name == 'posix':
    from .. import netdev
    from .. import subproc
_LOGGER = logging.getLogger(__name__)
_WATCHDOG_CHECK_INTERVAL = 30

def init():
    """Top level command handler."""

    @click.command()
    @click.option('--exit-on-fail', is_flag=True, default=False)
    @click.option('--zkid', help='Zookeeper session ID file.')
    @click.option('--approot', type=click.Path(exists=True), envvar='TREADMILL_APPROOT', required=True)
    def top(exit_on_fail, zkid, approot):
        """Run treadmill init process."""
        _LOGGER.info('Initializing Treadmill: %s', approot)
        app_env = appmgr.AppEnvironment(approot)
        zkclient = zkutils.connect(context.GLOBAL.zk.url, idpath=zkid, listener=zkutils.exit_on_lost)
        utils.report_ready()
        while not zkclient.exists(z.SERVER_PRESENCE):
            _LOGGER.warn('namespace not ready.')
            time.sleep(30)

        hostname = sysinfo.hostname()
        new_node_info = sysinfo.node_info(app_env)
        zk_blackout_path = z.path.blackedout_server(hostname)
        zk_presence_path = z.path.server_presence(hostname)
        zk_server_path = z.path.server(hostname)
        while not zkclient.exists(zk_server_path):
            _LOGGER.warn('server not defined in the cell.')
            time.sleep(30)

        _LOGGER.info('Checking blackout list.')
        blacklisted = bool(zkclient.exists(zk_blackout_path))
        if not blacklisted:
            old_session_ok = False
            try:
                _data, metadata = zkclient.get(zk_presence_path)
                if metadata.owner_session_id == zkclient.client_id[0]:
                    _LOGGER.info('Reconnecting with previous session: %s', metadata.owner_session_id)
                    old_session_ok = True
                else:
                    _LOGGER.info('Session id does not match, new session.')
                    zkclient.delete(zk_presence_path)
            except kazoo.client.NoNodeError:
                _LOGGER.info('%s does not exist.', zk_presence_path)

            if not old_session_ok:
                app_initialize.initialize(app_env)
                node_info = zkutils.get(zkclient, zk_server_path)
                node_info.update(new_node_info)
                _LOGGER.info('Registering node: %s: %s, %s', zk_server_path, hostname, node_info)
                zkutils.update(zkclient, zk_server_path, node_info)
                host_acl = zkutils.make_host_acl(hostname, 'rwcda')
                _LOGGER.debug('host_acl: %r', host_acl)
                zkutils.put(zkclient, zk_presence_path, {'seen': False}, acl=[
                 host_acl], ephemeral=True)
            app_env.watchdogs.initialize()
            _init_network()
            _LOGGER.info('Ready.')
            node_deleted_event = threading.Event()

            @zkclient.DataWatch(zk_presence_path)
            @exc.exit_on_unhandled
            def _exit_on_delete(data, _stat, event):
                """Force exit if server node is deleted."""
                if data is None or event is not None and event.type == 'DELETED':
                    node_deleted_event.set()
                    return False
                else:
                    return True

            down_reason = 'service node deleted.'
            while not node_deleted_event.wait(_WATCHDOG_CHECK_INTERVAL):
                result = app_env.watchdogs.check()
                if result:
                    down_reason = 'watchdogs %r failed.' % result
                    break

        else:
            down_reason = 'node blacklisted.'
        _LOGGER.warning('Shutting down: %s', down_reason)
        zkutils.ensure_exists(zkclient, zk_blackout_path, acl=[
         zkutils.make_host_acl(hostname, 'rwcda')], data=down_reason)
        zkutils.ensure_deleted(zkclient, zk_presence_path)
        zkclient.remove_listener(zkutils.exit_on_lost)
        zkclient.stop()
        zkclient.close()
        _cleanup_network()
        _blackout_terminate(app_env)
        if exit_on_fail:
            utils.sys_exit(-1)
        else:
            while True:
                time.sleep(1000000)

    return top


def _blackout_terminate(app_env):
    """Blackout by terminating all containers in running dir.
    """
    if os.name == 'posix':
        supervisor_dir = os.path.join(app_env.init_dir, 'supervisor')
        cleanupd_dir = os.path.join(app_env.init_dir, 'cleanup')
        _LOGGER.info('try to shutdown cleanup service')
        subproc.check_call(['s6-svc', '-d', cleanupd_dir])
        subproc.check_call(['s6-svwait', '-d', cleanupd_dir])
        _LOGGER.info('try to shutdown supervisor')
        subproc.check_call(['s6-svc', '-d', supervisor_dir])


def _init_network():
    """Initialize network.
    """
    if os.name == 'nt':
        return
    netdev.dev_conf_forwarding_set('tm0', True)


def _cleanup_network():
    """Cleanup network.
    """
    if os.name == 'nt':
        return
    netdev.dev_conf_forwarding_set('tm0', False)