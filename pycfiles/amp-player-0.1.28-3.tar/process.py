# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nivekuil/code/amp/amp/process.py
# Compiled at: 2015-08-11 04:00:43
import psutil, signal

def kill_process_tree(parent_pid):
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):
        child.kill()

    parent.kill()


def toggle_process_tree(parent_pid):
    parent = psutil.Process(parent_pid)
    if parent.status() == psutil.STATUS_STOPPED:
        for child in parent.children(recursive=True):
            child.resume()

        parent.resume()
        print 'Playback resumed.'
    else:
        for child in parent.children(recursive=True):
            child.suspend()

        parent.suspend()
        print "Playback paused. Type 'amp' again to resume."