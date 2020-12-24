# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winpwn\context.py
# Compiled at: 2020-04-17 05:00:57


class context:
    terminal = []
    arch = 'i386'
    endian = 'little'
    log_level = ''
    timeout = 512
    tick = 0.0625
    length = None
    newline = '\r\n'
    pie = None
    noout = None
    nocolor = None
    dbginit = ''
    gdb = None
    windbg = None
    windbgx = None
    x64dbg = None
    devdebug = False