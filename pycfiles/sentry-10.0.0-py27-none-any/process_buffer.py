# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/tasks/process_buffer.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import logging
from sentry.tasks.base import instrumented_task
from sentry.utils.locking import UnableToAcquireLock
logger = logging.getLogger(__name__)

@instrumented_task(name='sentry.tasks.process_buffer.process_pending', queue='buffers.process_pending')
def process_pending(partition=None):
    """
    Process pending buffers.
    """
    from sentry import buffer
    from sentry.app import locks
    if partition is None:
        lock_key = 'buffer:process_pending'
    else:
        lock_key = 'buffer:process_pending:%d' % partition
    lock = locks.get(lock_key, duration=60)
    try:
        with lock.acquire():
            buffer.process_pending(partition=partition)
    except UnableToAcquireLock as error:
        logger.warning('process_pending.fail', extra={'error': error, 'partition': partition})

    return


@instrumented_task(name='sentry.tasks.process_buffer.process_incr')
def process_incr(**kwargs):
    """
    Processes a buffer event.
    """
    from sentry import buffer
    buffer.process(**kwargs)