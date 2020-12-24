# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paczesiowa/projects/tvu/tests/test_utils.py
# Compiled at: 2017-02-09 15:46:39
import re, sys, unittest

class AssertRaisesContext(object):

    def __init__(self, test_case, exc_class, exc_msg, regex):
        self._test_case = test_case
        self._exc_class = exc_class
        self._exc_msg = exc_msg
        self._regex = regex

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, tb):
        if exc_value is None:
            test_err_msg = self._exc_class.__name__ + ' not raised'
            raise self._test_case.failureException(test_err_msg)
        if not isinstance(exc_value, self._exc_class):
            return False
        else:
            if self._exc_msg is not None and self._regex:
                regexp = re.compile(self._exc_msg)
                if not regexp.match(str(exc_value)):
                    raise self._test_case.failureException('"%s" does not match "%s"' % (regexp.pattern,
                     str(exc_value)))
            elif self._exc_msg is not None:
                self._test_case.assertEqual(str(exc_value), self._exc_msg)
            return True


class TestCase(unittest.TestCase):

    def assertRaises(self, exc_class, exc_msg=None, callableObj=None, regex=False, *args, **kwargs):
        if exc_msg is not None and sys.version_info < (3, ):
            exc_msg = exc_msg.encode('ascii', 'replace').decode('ascii')
        if callableObj is None:
            return AssertRaisesContext(self, exc_class, exc_msg, regex)
        else:
            try:
                callableObj(*args, **kwargs)
            except exc_class as e:
                if exc_msg is not None:
                    self.assertEqual(str(e), exc_msg)
            else:
                test_err_msg = exc_class.__name__ + ' not raised'
                raise self.failureException(test_err_msg)

            return