# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/error.py
# Compiled at: 2018-12-29 12:21:47


class PySmiError(Exception):
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)
        self.msg = args and args[0] or ''
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, (', ').join([ '%s=%r' % (k, getattr(self, k)) for k in dir(self) if k[0] != '_' if k != 'args' ]))

    def __str__(self):
        return self.msg


class PySmiLexerError(PySmiError):
    __module__ = __name__
    lineno = '?'

    def __str__(self):
        return self.msg + ', line %s' % self.lineno


class PySmiParserError(PySmiLexerError):
    __module__ = __name__


class PySmiSyntaxError(PySmiParserError):
    __module__ = __name__


class PySmiSearcherError(PySmiError):
    __module__ = __name__


class PySmiFileNotModifiedError(PySmiSearcherError):
    __module__ = __name__


class PySmiFileNotFoundError(PySmiSearcherError):
    __module__ = __name__


class PySmiReaderError(PySmiError):
    __module__ = __name__


class PySmiReaderFileNotModifiedError(PySmiReaderError):
    __module__ = __name__


class PySmiReaderFileNotFoundError(PySmiReaderError):
    __module__ = __name__


class PySmiCodegenError(PySmiError):
    __module__ = __name__


class PySmiSemanticError(PySmiCodegenError):
    __module__ = __name__


class PySmiWriterError(PySmiError):
    __module__ = __name__