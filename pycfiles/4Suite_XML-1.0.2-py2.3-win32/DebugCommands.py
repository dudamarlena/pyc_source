# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\Debugger\DebugCommands.py
# Compiled at: 2001-09-15 16:28:41
RUN = 1
QUIT = 2
PRINT = 3
TEMPLATE = 4
LIST_SHEET = 5
BACK_TRACE = 6
STEP = 7
NEXT = 8
TEST = 9
EVAL = 10
MATCH = 11
AVT = 12
LIST_TEMPLATE = 13
SET_BREAK = 14
LIST_BREAK = 15
DELETE_BREAK = 16
HELP = 100
g_runCommands = [
 RUN, TEMPLATE, STEP, NEXT]

class ExitException:
    __module__ = __name__