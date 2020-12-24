# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/reboot_monitor.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 3074 bytes
"""Treadmill reboot monitor.

The monitor will watch a /reboots/<hostname> Zookeeper node.

If the node exists, and created after server was rebooted, node will reboot.

If the node exists but is created before server was rebooted, node will be
deleted (as server was rebooted already).

Actual reboot procedure is specified in command line. Prior to invoking
the plugin, perform graceful shutdown.
"""
import logging, os, time, click
from .. import context
from .. import exc
from .. import sysinfo
from .. import zkutils
from .. import zknamespace as z
_LOGGER = logging.getLogger(__name__)

def init():
    """Top level command handler."""

    @click.command()
    @click.argument('command', nargs=-1)
    def reboot_monitor(command):
        """Runs node reboot monitor."""
        reboot_cmd = list(command)
        _LOGGER.info('Initializing reboot monitor: %r', reboot_cmd)
        zkclient = context.GLOBAL.zk.conn
        zkclient.add_listener(zkutils.exit_on_lost)
        while not zkclient.exists(z.REBOOTS):
            _LOGGER.warn('%r node not created yet. Cell masters running?', z.REBOOTS)
            time.sleep(30)

        hostname = sysinfo.hostname()
        up_since = sysinfo.up_since()
        _LOGGER.info('Server: %s, up since: %s', hostname, up_since)
        reboot_path = z.path.reboot(hostname)

        @zkclient.DataWatch(reboot_path)
        @exc.exit_on_unhandled
        def _watch_version(_data, stat, event):
            """Watch reboot node."""
            if event is not None and event.type == 'DELETED':
                _LOGGER.info('Node deleted, ignore.')
                return True
            if not stat:
                _LOGGER.info('Node does not exist, ignore.')
                return True
            if stat.created > up_since:
                _LOGGER.info('Reboot requested at: %s, up since: %s', time.ctime(stat.created), time.ctime(up_since))
                presence_path = z.path.server_presence(hostname)
                _LOGGER.info('Deleting server presence: %s', presence_path)
                zkutils.ensure_deleted(zkclient, presence_path)
                _LOGGER.info('exec: %r', reboot_cmd)
                os.execvp(reboot_cmd[0], reboot_cmd)
            else:
                _LOGGER.info('Reboot success, requested at %s, up since: %s', stat.created, up_since)
                zkutils.ensure_deleted(zkclient, reboot_path)
                _LOGGER.info('Deleting zknode: %r', reboot_path)
            return True

        while True:
            time.sleep(100000)

        _LOGGER.info('service shutdown.')

    return reboot_monitor