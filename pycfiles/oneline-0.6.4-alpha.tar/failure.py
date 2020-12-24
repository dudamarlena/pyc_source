# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/lz4/nose-1.3.4-py2.7.egg/nose/failure.py
# Compiled at: 2014-09-06 21:58:19
import logging, unittest
from traceback import format_tb
from nose.pyversion import is_base_exception
log = logging.getLogger(__name__)
__all__ = [
 'Failure']

class Failure(unittest.TestCase):
    """Unloadable or unexecutable test.

    A Failure case is placed in a test suite to indicate the presence of a
    test that could not be loaded or executed. A common example is a test
    module that fails to import.
    
    """
    __test__ = False

    def __init__(self, exc_class, exc_val, tb=None, address=None):
        log.debug('A failure! %s %s %s', exc_class, exc_val, format_tb(tb))
        self.exc_class = exc_class
        self.exc_val = exc_val
        self.tb = tb
        self._address = address
        unittest.TestCase.__init__(self)

    def __str__(self):
        return 'Failure: %s (%s)' % (
         getattr(self.exc_class, '__name__', self.exc_class), self.exc_val)

    def address(self):
        return self._address

    def runTest(self):
        if self.tb is not None:
            if is_base_exception(self.exc_val):
                raise self.exc_val, None, self.tb
            raise self.exc_class, self.exc_val, self.tb
        else:
            raise self.exc_class(self.exc_val)
        return