# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/cleanup.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 3630 bytes
"""Runs the Treadmill container cleanup job."""
import glob, logging, os, subprocess, click
from .. import appmgr
from .. import idirwatch
from .. import logcontext as lc
from .. import subproc
import treadmill
_LOGGER = lc.ContainerAdapter(logging.getLogger(__name__))
_WATCHDOG_HEARTBEAT_SEC = 300
_MAX_REQUEST_PER_CYCLE = 1
_SERVICE_NAME = 'Cleanup'

def init():
    """Top level command handler."""

    @click.command()
    @click.option('--approot', type=click.Path(exists=True), envvar='TREADMILL_APPROOT', required=True)
    def top(approot):
        """Start cleanup process."""
        app_env = appmgr.AppEnvironment(root=approot)
        watchdog_lease = app_env.watchdogs.create(name='svc-{svc_name}'.format(svc_name=_SERVICE_NAME), timeout='{hb:d}s'.format(hb=_WATCHDOG_HEARTBEAT_SEC), content='Service {svc_name!r} failed'.format(svc_name=_SERVICE_NAME))

        def _on_created(path):
            """Callback invoked with new cleanup file appears."""
            fullpath = os.path.join(app_env.cleanup_dir, path)
            with lc.LogContext(_LOGGER, os.path.basename(path), lc.ContainerAdapter) as (log):
                if not os.path.islink(fullpath):
                    log.logger.info('Ignore - not a link: %s', fullpath)
                    return
                container_dir = os.readlink(fullpath)
                log.logger.info('Cleanup: %s => %s', path, container_dir)
                if os.path.exists(container_dir):
                    try:
                        log.logger.info('invoking treadmill.TREADMILL_BIN script: %r', treadmill.TREADMILL_BIN)
                        subproc.check_call([
                         treadmill.TREADMILL_BIN,
                         'sproc',
                         'finish',
                         container_dir])
                    except subprocess.CalledProcessError:
                        log.exception('Fatal error running %r.', treadmill.TREADMILL_BIN)
                        raise

                else:
                    log.logger.info('Container dir does not exist: %r', container_dir)
                os.unlink(fullpath)

        watcher = idirwatch.DirWatcher(app_env.cleanup_dir)
        watcher.on_created = _on_created
        leftover = glob.glob(os.path.join(app_env.cleanup_dir, '*'))
        for pending_cleanup in leftover:
            _on_created(pending_cleanup)

        loop_timeout = _WATCHDOG_HEARTBEAT_SEC / 2
        while True:
            if watcher.wait_for_events(timeout=loop_timeout):
                watcher.process_events(max_events=_MAX_REQUEST_PER_CYCLE)
            watchdog_lease.heartbeat()

        _LOGGER.info('Cleanup service shutdown.')
        watchdog_lease.remove()

    return top