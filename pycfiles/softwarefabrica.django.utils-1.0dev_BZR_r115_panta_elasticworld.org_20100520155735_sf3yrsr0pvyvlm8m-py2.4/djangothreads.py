# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/djangothreads.py
# Compiled at: 2009-05-16 09:30:52
"""
Threading support routines for django applications

Using these functions external applications can join threads before exiting.
This for example is useful when threads are spawn for long-running activities.
"""
try:
    import thread
except ImportError:
    import dummy_thread as thread

try:
    import threading
except ImportError:
    import dummy_threading as threading

import logging
_all_django_threads = {}

def add_thread(thread):
    """Add the given ``thread`` to the set of threads to wait for at the end."""
    global _all_django_threads
    assert isinstance(thread, threading.Thread)
    _all_django_threads[thread] = True
    assert thread in _all_django_threads.keys()


def remove_thread(thread):
    """Remove the given ``thread`` from the set of threads to wait for at the end."""
    assert isinstance(thread, threading.Thread)
    if thread in _all_django_threads.keys():
        _all_django_threads[thread] = False
        del _all_django_threads[thread]


def wait_thread(thread):
    """Wait for the given ``thread`` and then remove it from the set of threads to wait for."""
    assert isinstance(thread, threading.Thread)
    if thread in _all_django_threads.keys():
        if _all_django_threads[thread]:
            thread.join()
            _all_django_threads[thread] = False
        del _all_django_threads[thread]


def wait_all_threads():
    """Wait for all the known threads and remove them from the set of threads to wait for."""
    logging.info('waiting for django threads...')
    for thread in _all_django_threads.keys():
        assert isinstance(thread, threading.Thread)
        if _all_django_threads[thread]:
            thread_name = '%s' % thread
            logging.info('waiting for thread %s...' % thread_name)
            thread.join()
            logging.info('thread %s exited' % thread_name)
            _all_django_threads[thread] = False
        del _all_django_threads[thread]