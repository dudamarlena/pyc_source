# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/tb.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains a set of useful traceback elements based on python's
:mod:`traceback` system."""
from builtins import str
import sys, traceback, threading

def _get_thread(ident=None):
    if ident is None:
        return threading.current_thread()
    else:
        for th in threading.enumerate():
            if th.ident == ident:
                return th

        return


def _get_frames():
    return sys._current_frames()


def format_frame_stacks(frames=None, limit=None):
    if frames is None:
        frames = _get_frames()
    frame_stacks = extract_frame_stacks(frames=frames, limit=limit)
    ret = []
    for ident, (frame, frame_stack) in list(frame_stacks.items()):
        curr_th, th = _get_thread(), _get_thread(ident)
        if th is None:
            th_name = '<Unknown>'
            curr = ''
        else:
            th_name = th.name
            if curr_th.ident == th.ident:
                th_str = '(Current) '
            else:
                curr = ''
            ret.append('  Thread ' + curr + th_name + ' (' + str(ident) + ') in\n')
            format_stack = traceback.format_list(frame_stack)
            for i, line in enumerate(format_stack):
                line = '  ' + line.replace('\n  ', '\n    ')
                ret.append(line)

    return ret


def extract_frame_stacks(frames=None, limit=None):
    if frames is None:
        frames = _get_frames()
    ret = {}
    for ident, frame in list(frames.items()):
        frame_stack = traceback.extract_stack(frame, limit=limit)
        ret[ident] = (frame, frame_stack)

    return ret