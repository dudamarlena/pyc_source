# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/debug.py
# Compiled at: 2015-09-06 21:42:15
__author__ = 'perkins'
DEBUG = False
debug_settings = {'pushStack': False, 
   'popStack': False, 
   'discardedFrames': False, 
   'repl': False, 
   'syntax': False, 
   'symbols': False, 
   'patternMatcher': False, 
   'tracebck': False, 
   'jit-crash-on-error': False, 
   'jit': True, 
   'jit-one-opcode-per-line': False}

def getDebug(key):
    if key in debug_settings:
        return debug_settings[key]
    return False


def setDebug(k, v):
    if k == 'all':
        for k in debug_settings:
            debug_settings[k] = v

    else:
        debug_settings[k] = v


def LOG(SECTION, *args):
    if not getDebug(SECTION):
        return
    print SECTION,
    for arg in args:
        print arg,

    print


def setAll(b):
    for i in debug_settings:
        debug_settings[i] = b