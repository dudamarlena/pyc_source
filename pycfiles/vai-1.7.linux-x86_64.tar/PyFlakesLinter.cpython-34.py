# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/linting/PyFlakesLinter.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1452 bytes
from .LinterResult import LinterResult
import pyflakes.api

class PyFlakesLinter:
    __doc__ = 'Fast, less accurate linter.'

    def __init__(self, document):
        self._document = document

    def runOnce(self):
        reporter = Reporter()
        pyflakes.api.check(self._document.documentText(), self._document.documentMetaInfo('Filename').data(), reporter=reporter)
        return reporter.errors()


class Reporter:
    __doc__ = 'Wrap class to get events delivered for our consumption'

    def __init__(self):
        self._errors = []

    def unexpectedError(self, *args):
        pass

    def syntaxError(self, filename, msg, lineno, offset, text):
        self._errors.append(LinterResult(filename=filename, line=lineno, column=offset, level='error', message=msg))

    def flake(self, msg):
        self._errors.append(LinterResult(filename=msg.filename, line=msg.lineno, column=msg.col, level='warning', message=str(msg)))

    def errors(self):
        return self._errors