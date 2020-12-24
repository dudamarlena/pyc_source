# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/lib/default.py
# Compiled at: 2013-03-18 19:28:12
""" A place for the debugger default settings """
from os import environ as ENV
import os, tracer
from tracer import *
width = 80
if 'COLUMNS' in ENV:
    try:
        width = int(ENV['COLUMNS'])
    except:
        pass

DEBUGGER_SETTINGS = {'annotate': 0, 'autoeval': True, 'autolist': False, 'autoipython': False, 'autopython': False, 'basename': False, 'cmdtrace': False, 'confirm': True, 'debugmacro': False, 'dbg_pydbgr': False, 'different': True, 'events': tracer.ALL_EVENTS, 'highlight': 'light', 'hist_save': False, 'histfile': None, 'fntrace': False, 'listsize': 10, 'maxargstrsize': 100, 'maxstring': 150, 'printset': tracer.ALL_EVENTS, 'nostartup': False, 'reload': False, 'skip': True, 'trace': False, 'width': width}
CLIENT_SOCKET_OPTS = {'HOST': '127.0.0.1', 'PORT': 1027}
SERVER_SOCKET_OPTS = {'HOST': None, 'PORT': 1027, 'reuse': 'posix' == os.name}
START_OPTS = {'event_set': tracer.ALL_EVENTS, 'add_hook_opts': tracer.DEFAULT_ADD_HOOK_OPTS, 'start': False, 'force': False, 'backlevel': 0}
STOP_OPTS = {'remove': False}
if __name__ == '__main__':
    import pprint
    for val in ['DEBUGGER_SETTINGS', 'START_OPTS', 'STOP_OPTS']:
        print '%s:\n' % val, pprint.pformat(eval(val))
        print