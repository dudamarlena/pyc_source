# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/test/test_panic.py
# Compiled at: 2018-05-03 13:55:55
import inspect, logging, unittest, sys
from future.utils import raise_
from bd2k.util.exceptions import panic
log = logging.getLogger(__name__)
logging.basicConfig()

class TestPanic(unittest.TestCase):

    def test_panic_by_hand(self):
        try:
            self.try_and_panic_by_hand()
        except:
            self.__assert_raised_exception_is_primary()

    def test_panic(self):
        try:
            self.try_and_panic()
        except:
            self.__assert_raised_exception_is_primary()

    def test_panic_with_secondary(self):
        try:
            self.try_and_panic_with_secondary()
        except:
            self.__assert_raised_exception_is_primary()

    def test_nested_panic(self):
        try:
            self.try_and_nested_panic_with_secondary()
        except:
            self.__assert_raised_exception_is_primary()

    def try_and_panic_by_hand(self):
        try:
            self.line_of_primary_exc = inspect.currentframe().f_lineno + 1
            raise ValueError('primary')
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            try:
                raise RuntimeError('secondary')
            except Exception:
                pass

            raise_(exc_type, exc_value, exc_traceback)

    def try_and_panic(self):
        try:
            self.line_of_primary_exc = inspect.currentframe().f_lineno + 1
            raise ValueError('primary')
        except:
            with panic(log):
                pass

    def try_and_panic_with_secondary(self):
        try:
            self.line_of_primary_exc = inspect.currentframe().f_lineno + 1
            raise ValueError('primary')
        except:
            with panic(log):
                raise RuntimeError('secondary')

    def try_and_nested_panic_with_secondary(self):
        try:
            self.line_of_primary_exc = inspect.currentframe().f_lineno + 1
            raise ValueError('primary')
        except:
            with panic(log):
                with panic(log):
                    raise RuntimeError('secondary')

    def __assert_raised_exception_is_primary(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.assertEquals(exc_type, ValueError)
        self.assertEquals(str(exc_value), 'primary')
        while exc_traceback.tb_next is not None:
            exc_traceback = exc_traceback.tb_next

        self.assertEquals(exc_traceback.tb_lineno, self.line_of_primary_exc)
        return