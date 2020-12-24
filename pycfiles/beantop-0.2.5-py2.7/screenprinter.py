# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beantop/screenprinter.py
# Compiled at: 2013-05-21 04:02:16


class ScreenPrinter:

    def __init__(self, operative_system, sys):
        self._operative_system = operative_system
        self._sys = sys

    def print_lines(self, lines):
        for line in lines:
            self._sys.stdout.write(line + '\n')

    def clear(self):
        self._operative_system.system('clear')