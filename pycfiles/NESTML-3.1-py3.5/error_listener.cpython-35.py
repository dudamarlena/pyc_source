# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/error_listener.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1348 bytes
"""
This class contains several method used to parse handed over models and returns them as one or more AST trees.
"""
from antlr4.error.ErrorListener import ConsoleErrorListener, ErrorListener

class NestMLErrorListener(ErrorListener):
    __doc__ = 'helper class to listen for parser errors and record whether an error has occurred'

    def __init__(self):
        super(NestMLErrorListener, self).__init__()
        self._error_occurred = False

    @property
    def error_occurred(self):
        return self._error_occurred

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self._error_occurred = True