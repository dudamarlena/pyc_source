# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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