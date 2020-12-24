# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/fifo.py
# Compiled at: 2013-01-26 13:25:47
"""Queues are using to enqueue some actions which will be performed after
a task execution."""
from Queue import Queue

def put(action, parameters=()):
    """Enqueue one action with action parameters in environment"""
    if 'mico_queue' in env:
        env['mico_queue'].put((action, parameters))
    else:
        env['mico_queue'] = Queue()
        env['mico_queue'].put((action, parameters))


def run():
    """Run enqueued actions"""
    if 'mico_queue' in env:
        ret = []
        q = env['mico_queue']
        while not q.empty():
            action, parameters = q.get()
            ret.append(action(*parameters))

        return ret
    return []


def get():
    """Get an element of the queue"""
    if 'mico_queue' in env:
        q = env['mico_queue']
        return q.get()