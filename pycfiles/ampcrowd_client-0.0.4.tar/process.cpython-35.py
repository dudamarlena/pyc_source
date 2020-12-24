# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nivekuil/code/amp/python3/amp/process.py
# Compiled at: 2016-05-03 00:57:28
# Size of source mod 2**32: 828 bytes
import psutil, signal

def kill_process_tree(parent_pid):
    try:
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):
            child.kill()

        parent.kill()
    except:
        print('Cannot find the amp process to kill.  Was amp killed uncleanly?')


def toggle_process_tree(parent_pid):
    parent = psutil.Process(parent_pid)
    if parent.status() == psutil.STATUS_STOPPED:
        for child in parent.children(recursive=True):
            child.resume()

        parent.resume()
        print('Playback resumed.')
    else:
        for child in parent.children(recursive=True):
            child.suspend()

        parent.suspend()
        print("Playback paused. Type 'amp' again to resume.")