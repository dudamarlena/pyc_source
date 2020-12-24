# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/version_monitor.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 3576 bytes
"""Treadmill version monitor.

The monitor will watch a /version/<hostname> Zookeeper node.

If the node is deleted, it will run an "upgrade/reset" script, and recreated
the node.

The content of the node contain real path of the Treadmill code and timestamp
when the reset happened.
"""
import logging, os, subprocess, time, click
from .. import appmgr
from .. import context
from .. import exc
from .. import subproc
from .. import sysinfo
from .. import utils
from .. import versionmgr
from .. import watchdog
from .. import zkutils
from .. import zknamespace as z
_LOGGER = logging.getLogger(__name__)

def init():
    """Top level command handler."""

    @click.command()
    @click.option('--approot', type=click.Path(exists=True), envvar='TREADMILL_APPROOT', required=True)
    @click.argument('command', nargs=-1)
    def version_monitor(approot, command):
        """Runs node version monitor."""
        cli_cmd = list(command)
        _LOGGER.info('Initializing code monitor: %r', cli_cmd)
        watchdogs = watchdog.Watchdog(os.path.join(approot, appmgr.AppEnvironment.WATCHDOG_DIR))
        context.GLOBAL.zk.conn.add_listener(zkutils.exit_on_lost)
        while not context.GLOBAL.zk.conn.exists(z.VERSION):
            _LOGGER.warn('%r node not created yet. Cell masters running?', z.VERSION)
            time.sleep(30)

        hostname = sysinfo.hostname()
        version_path = z.path.version(hostname)
        codepath = os.path.realpath(utils.rootdir())
        digest = versionmgr.checksum_dir(codepath).hexdigest()
        _LOGGER.info('codepath: %s, digest: %s', codepath, digest)
        info = {'codepath': codepath, 
         'since': int(time.time()), 
         'digest': digest}
        zkutils.put(context.GLOBAL.zk.conn, version_path, info)

        @context.GLOBAL.zk.conn.DataWatch(version_path)
        @exc.exit_on_unhandled
        def _watch_version(_data, _stat, event):
            """Force exit if server node is deleted."""
            if event is not None:
                if event.type == 'DELETED':
                    _LOGGER.info('Upgrade requested, running: %s', cli_cmd)
                    if cli_cmd:
                        try:
                            subproc.check_call(cli_cmd)
                        except subprocess.CalledProcessError:
                            _LOGGER.exception('Upgrade failed.')
                            watchdogs.create(name='version_monitor', timeout='0s', content='Upgrade to {code!r}({digest}) failed'.format(code=codepath, digest=digest)).heartbeat()
                            del info['digest']

                    _LOGGER.info('Upgrade complete.')
                    utils.sys_exit(0)
            return True

        while True:
            time.sleep(100000)

        _LOGGER.info('service shutdown.')

    return version_monitor