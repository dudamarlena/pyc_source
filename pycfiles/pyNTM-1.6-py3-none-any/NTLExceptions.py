# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLExceptions.py
# Compiled at: 2018-04-23 08:51:10
import sys, traceback
from .NTLUtilities import jsrange, ispy3
__all__ = [
 'BaseError',
 'DigitError', 'IntError', 'RealError', 'ComplexError',
 'BoolError', 'DictError', 'ListError', 'TupleError', 'StringError', 'PolyError',
 'PNError', 'OEError', 'PCError', 'ZeroError',
 'DefinitionError', 'ArgumentError', 'KeywordError',
 'ExponentError', 'ResidueError', 'SolutionError']

class BaseError(Exception):
    """Cautions:

    * Turn off system-default traceback function by set `sys.tracebacklimit` to 0.
    * But bugs appear in Python 3.6, so we have to set `sys.tracebacklimit` to None.
    * In Python 2.7, `trace.print_stack(limit=None)` dose not support negative limit.

    """

    def __init__(self, message):
        (self.traceback_3 if ispy3 else self.traceback_2)()
        super().__init__(message)

    def tb_preparation(self):
        tb = traceback.extract_stack()
        for tbitem in tb:
            if '/jspcap/' in tbitem[0]:
                index = tb.index(tbitem)
                break
        else:
            index = len(tb)

        return index

    def traceback_2(self):
        index = self.tb_preparation()
        print 'Traceback (most recent call last):'
        print ('').join(traceback.format_stack()[:index])[:-1]
        sys.tracebacklimit = 0

    def traceback_3(self):
        index = self.tb_preparation()
        print 'Traceback (most recent call last):'
        traceback.print_stack(limit=-index)
        sys.tracebacklimit = 0


class DigitError(BaseError, TypeError):
    pass


class IntError(BaseError, TypeError):
    pass


class DictError(BaseError, TypeError):
    pass


class ListError(BaseError, TypeError):
    pass


class TupleError(BaseError, TypeError):
    pass


class PolyError(BaseError, TypeError):
    pass


class ArgumentError(BaseError, TypeError):
    pass


class RealError(BaseError, TypeError):
    pass


class ComplexError(BaseError, TypeError):
    pass


class PNError(BaseError, ValueError):
    pass


class OEError(BaseError, ValueError):
    pass


class PCError(BaseError, ValueError):
    pass


class ZeroError(BaseError, ValueError):
    pass


class BoolError(BaseError, ValueError):
    pass


class StringError(BaseError, ValueError):
    pass


class DefinitionError(BaseError, ValueError):
    pass


class SolutionError(BaseError, RuntimeError):
    pass


class ExponentError(BaseError, KeyError):
    pass


class ResidueError(BaseError, ZeroDivisionError):
    pass


class KeywordError(BaseError, AttributeError):
    pass