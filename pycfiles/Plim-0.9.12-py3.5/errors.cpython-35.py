# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plim/errors.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 748 bytes
from .util import u

class PlimError(Exception):

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class PlimSyntaxError(PlimError):

    def __init__(self, msg, line):
        super(PlimSyntaxError, self).__init__()
        self.msg = msg
        self.line = line

    def __unicode__(self):
        return u('{msg} | at line(pos) "{line}"').format(msg=self.msg, line=self.line)


class ParserNotFound(PlimError):

    def __init__(self, lineno, line):
        super(ParserNotFound, self).__init__()
        self.lineno = lineno
        self.line = line

    def __unicode__(self):
        return u('Invalid syntax at line {lineno}: {line}').format(lineno=self.lineno, line=self.line)