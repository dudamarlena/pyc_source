# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/task.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 1338 bytes
"""Cleans up old tasks from Treadmill."""
import logging, time, click
from treadmill.apptrace import zk
from treadmill import sysinfo
from treadmill import context
_LOGGER = logging.getLogger(__name__)
TASK_EXPIRATION_TIME = 86400
TASK_CHECK_INTERFAL = 3600

def init():
    """Top level command handler."""

    @click.group()
    def task():
        """Manage Treadmill tasks."""
        pass

    @task.command()
    @click.option('--expiration', help='Task expiration (sec).', default=TASK_EXPIRATION_TIME)
    @click.option('--interval', help='Timeout between checks (sec).', default=TASK_CHECK_INTERFAL)
    def cleanup(expiration, interval):
        """Cleans up old tasks."""
        context.GLOBAL.zk.conn.ensure_path('/task-cleanup-election')
        me = '%s' % sysinfo.hostname()
        lock = context.GLOBAL.zk.conn.Lock('/task-cleanup-election', me)
        _LOGGER.info('Waiting for leader lock.')
        with lock:
            while True:
                zk.cleanup(context.GLOBAL.zk.conn, expiration)
                _LOGGER.info('Finished cleanup, sleep %s sec', interval)
                time.sleep(interval)

    del cleanup
    return task