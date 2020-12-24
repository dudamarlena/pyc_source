# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/run.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2072 bytes
"""Runs the Treadmill application runner."""
import signal, logging, os, click
from .. import appmgr
from .. import utils
from .. import logcontext as lc
from ..appmgr import run as app_run
from ..appmgr import abort as app_abort
_LOGGER = logging.getLogger(__name__)

def init():
    """Top level command handler."""

    @click.command()
    @click.option('--approot', type=click.Path(exists=True), envvar='TREADMILL_APPROOT', required=True)
    @click.argument('container_dir', type=click.Path(exists=True))
    def run(approot, container_dir):
        """Runs container given a container dir."""
        with lc.LogContext(_LOGGER, os.path.basename(container_dir), lc.ContainerAdapter) as (log):
            terminated = utils.make_signal_flag(signal.SIGTERM)
            try:
                try:
                    log.logger.info('run %r %r', approot, container_dir)
                    app_env = appmgr.AppEnvironment(approot)
                    watchdog = app_run.create_watchdog(app_env, container_dir)
                    app_run.apply_cgroup_limits(app_env, container_dir)
                    if not terminated:
                        app_run.run(app_env, container_dir, watchdog, terminated)
                except Exception as exc:
                    if not terminated:
                        log.critical('Failed to start, app will be aborted.', exc_info=True)
                        app_abort.flag_aborted(app_env, container_dir, exc)
                    else:
                        log.logger.info('Exception while handling term, ignore.', exc_info=True)

            finally:
                watchdog.remove()

    return run