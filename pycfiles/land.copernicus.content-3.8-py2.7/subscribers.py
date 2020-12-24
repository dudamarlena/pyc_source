# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/async/subscribers.py
# Compiled at: 2017-11-01 05:34:47
""" Subscribers
"""
import os, logging
from plone.app.async.subscribers import set_quota
logger = logging.getLogger('land.copernicus.content')
NAME = 'landfiles'

def get_maximum_threads(queue):
    """ Get the maximum threads per queue
    """
    size = 0
    for dispatcher_agent in queue.dispatchers.values():
        if not dispatcher_agent.activated:
            continue
        for _agent in dispatcher_agent.values():
            size += 3

    return size or 1


def configure_queue(event):
    """ Configure zc.async queue for land files async jobs
    """
    queue = event.object
    size = get_maximum_threads(queue)
    set_quota(queue, NAME, size=size)
    logger.info('quota %s with size %r configured in queue %r.', NAME, size, queue.name)