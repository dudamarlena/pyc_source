# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/lib/thred.py
# Compiled at: 2015-04-04 21:14:05
"""Routines related to threading. Assumes Python 2.5 or greater"""
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
            continue

    return name2id


if __name__ == '__main__':
    import sys
    print('==========')

    def showit():
        print('Current thread: %s' % current_thread_name())
        print('All threads:')
        for thread_id, f in list(sys._current_frames().items()):
            print('  %s %s' % (id2thread_name(thread_id),
             find_debugged_frame(f)))

        print('----------')
        print('Thread->id map:')
        print(map_thread_names())
        print('==========')


    showit()

    class BgThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            showit()


    background = BgThread()
    background.start()
    background.join()