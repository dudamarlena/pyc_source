# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winpwn\var.py
# Compiled at: 2020-04-14 16:26:59
import os, json
from misc import Latin1_encode
debugger = {'i386': {'windbg': '', 
            'x64dbg': '', 
            'gdb': '', 
            'windbgx': ''}, 
   'amd64': {'windbg': '', 
             'x64dbg': '', 
             'gdb': '', 
             'windbgx': ''}}
debugger_init = {'i386': {'windbg': '', 
            'x64dbg': '', 
            'gdb': '', 
            'windbgx': ''}, 
   'amd64': {'windbg': '', 
             'x64dbg': '', 
             'gdb': '', 
             'windbgx': ''}}

def init_var():
    winpwn_init = os.path.expanduser('~\\.winpwn')
    if os.path.exists(winpwn_init):
        fd = open(winpwn_init, 'r')
        js = Latin1_encode(('').join(fd.readlines()))
        x = json.loads(js)
        dbg = x['debugger']
        dbg_init = x['debugger_init']
        fd.close()
        debugger.update(dbg)
        debugger_init.update(dbg_init)