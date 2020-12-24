# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sven/0/_sdks/python/sven-2.7/lib/python2.7/site-packages/knewt/debug.py
# Compiled at: 2018-02-10 09:15:19
debug_level = False

def set_debug(flag):
    global debug_level
    debug_level = flag


def log(line):
    if debug_level == True:
        print line


trace_level = False

def set_trace(flag):
    global trace_level
    trace_level = flag


def trace(line):
    trace_header = ''
    if trace_level == True:
        print '%s' % line