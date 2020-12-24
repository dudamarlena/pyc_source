# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/lib/thread.py
# Compiled at: 2013-03-11 05:01:47
__doc__ = 'Routines related to threading. Assumes Python 2.5 or greater'
import threading

def current_thread_name():
    return threading.currentThread().getName()


def find_debugged_frame(frame):
    """Find the first frame that is a debugged frame. We do this
    Generally we want traceback information without polluting it with
    debugger frames. We can tell these because those are frames on the
    top which don't have f_trace set. So we'll look back from the top
    to find the fist frame where f_trace is set.
    """
    f_prev = f = frame
    while f is not None and f.f_trace is None:
        f_prev = f
        f = f.f_back

    if f_prev:
        val = f_prev.f_locals.get('tracer_func_frame')
        if val == f_prev:
            if f_prev.f_back:
                f_prev = f_prev.f_back
    else:
        return frame
    return f_prev


def id2thread_name(thread_id):
    return threading.Thread.getName(threading._active[thread_id])


def map_thread_names():
    """Invert threading._active"""
    name2id = {}
    for thread_id in list(threading._active.keys()):
        thread = threading._active[thread_id]
        name = thread.getName()
        if name not in list(name2id.keys()):
            name2id[name] = thread_id

    return name2id


if __name__ == '__main__':
    import sys
    print '=' * 10

    def showit():
        print 'Current thread: %s' % current_thread_name()
        print 'All threads:'
        for (thread_id, f) in list(sys._current_frames().items()):
            print '  %s %s' % (id2thread_name(thread_id), find_debugged_frame(f))

        print '-' * 10
        print 'Thread->id map:'
        print map_thread_names()
        print '=' * 10


    showit()

    class BgThread(threading.Thread):
        __module__ = __name__

        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            showit()


    background = BgThread()
    background.start()
    background.join()