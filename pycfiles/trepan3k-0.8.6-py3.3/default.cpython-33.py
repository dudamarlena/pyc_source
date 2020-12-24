# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/lib/default.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 5832 bytes
""" A place for the debugger default settings """
import os, tracer
from columnize import computed_displaywidth
from trepan.lib.term_background import is_dark_background
width = computed_displaywidth()
DEBUGGER_SETTINGS = {'annotate': 0, 
 'autoeval': True, 
 'autolist': False, 
 'autoipython': False, 
 'autopython': False, 
 'basename': False, 
 'cmdtrace': False, 
 'confirm': True, 
 'debugmacro': False, 
 'dbg_trepan': False, 
 'different': True, 
 'events': tracer.ALL_EVENTS, 
 'highlight': is_dark_background(), 
 'hist_save': False, 
 'histfile': None, 
 'hist_save': True, 
 'fntrace': False, 
 'listsize': 10, 
 'maxargstrsize': 100, 
 'maxstring': 150, 
 'printset': tracer.ALL_EVENTS, 
 'nostartup': False, 
 'reload': False, 
 'skip': True, 
 'trace': False, 
 'width': width}
CLIENT_SOCKET_OPTS = {'HOST': '127.0.0.1', 
 'PORT': 1027}
SERVER_SOCKET_OPTS = {'HOST': None, 
 'PORT': 1027, 
 'reuse': 'posix' == os.name, 
 'skew': 0, 
 'search_limit': 100}
START_OPTS = {'add_hook_opts': tracer.DEFAULT_ADD_HOOK_OPTS, 
 'backlevel': 0, 
 'event_set': tracer.ALL_EVENTS, 
 'force': False, 
 'start': False}
STOP_OPTS = {'remove': False}
if __name__ == '__main__':
    import pprint
    for val in ['DEBUGGER_SETTINGS', 'START_OPTS',
     'STOP_OPTS']:
        print('%s:' % val)
        print(pprint.pformat(eval(val)))
        print('----------')