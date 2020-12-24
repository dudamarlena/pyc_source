# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/ccnmtl/django-smoketest/smoketest/__init__.py
# Compiled at: 2017-06-18 04:08:30


def _dummy_method(*args, **kwargs):
    """ Just a dummy method that does nothing. """
    pass


class SmokeTest(object):
    _FAILED_TEST_FULL_MSG = '%(method_full_name)s %(result)s: %(msg)s'

    def __init__(self, logging_method=_dummy_method):
        """Construct instance of the SmokeTest class.

        @param logging_method: Python method that should receive a
            string as a parameter, and logs it for further review (or
            it can do whatever is needs to do for that
            matter). Optional, with dummy method which does nothing.

        """
        self._status = 'PASS'
        self._msg = ''
        self._logging_method = logging_method

    def failed(self):
        return self._status == 'FAIL'

    def passed(self):
        return self._status == 'PASS'

    def reset(self):
        self._status = 'PASS'

    def run(self):
        run, failed, passed, errored = (0, 0, 0, 0)
        failed_tests = []
        errored_tests = []
        for d in dir(self):
            if d.startswith('test_'):
                run += 1
                method_full_name = '%s.%s.%s' % (
                 self.__class__.__module__, self.__class__.__name__, d)
                try:
                    if hasattr(self, 'setUp'):
                        self.setUp()
                    getattr(self, d)()
                    if self.failed():
                        failed += 1
                        msg = self._FAILED_TEST_FULL_MSG % {'method_full_name': method_full_name, 
                           'result': 'failed', 
                           'msg': self._msg}
                        failed_tests.append(msg)
                        self._logging_method(msg)
                        self.reset()
                    else:
                        passed += 1
                    if hasattr(self, 'tearDown'):
                        self.tearDown()
                except Exception as e:
                    errored += 1
                    msg = self._FAILED_TEST_FULL_MSG % {'method_full_name': method_full_name, 
                       'result': 'errored', 
                       'msg': str(e)}
                    errored_tests.append(msg)
                    self._logging_method(msg)

        return (
         run, passed, failed, errored, failed_tests, errored_tests)

    def assertEqual(self, a, b, msg=None):
        if a != b:
            self._status = 'FAIL'
            self._msg = msg or '%s != %s' % (a, b)

    def assertNotEqual(self, a, b, msg=None):
        if a == b:
            self._status = 'FAIL'
            self._msg = msg or '%s == %s' % (a, b)

    def assertTrue(self, t, msg=None):
        if not t:
            self._status = 'FAIL'
            self._msg = msg or '%s is not true' % t

    def assertFalse(self, x, msg=None):
        if x:
            self._status = 'FAIL'
            self._msg = msg or '%s is not false' % x

    def assertIs(self, a, b, msg=None):
        if a is not b:
            self._status = 'FAIL'
            self._msg = msg or '%s is not %s' % (a, b)

    def assertIsNot(self, a, b, msg=None):
        if a is b:
            self._status = 'FAIL'
            self._msg = msg or '%s is %s' % (a, b)

    def assertIsNone(self, x, msg=None):
        if x is not None:
            self._status = 'FAIL'
            self._msg = msg or '%s is not None' % x
        return

    def assertIsNotNone(self, x, msg=None):
        if x is None:
            self._status = 'FAIL'
            self._msg = msg or '%s is None' % x
        return

    def assertIn(self, a, b, msg=None):
        if a not in b:
            self._status = 'FAIL'
            self._msg = msg or '%s is not in %s' % (a, b)

    def assertNotIn(self, a, b, msg=None):
        if a in b:
            self._status = 'FAIL'
            self._msg = msg or '%a is in %b' % (a, b)

    def assertIsInstance(self, a, b, msg=None):
        if not isinstance(a, b):
            self._status = 'FAIL'
            self._msg = msg or '%a is not an instance of %s' % (a, b)

    def assertNotIsInstance(self, a, b, msg=None):
        if isinstance(a, b):
            self._status = 'FAIL'
            self._msg = msg or '%s is an instance of %s' % (a, b)

    def assertRaises(self, exc_class, callable_obj, *args, **kwargs):
        try:
            callable_obj(*args, **kwargs)
            self._status = 'FAIL'
            if hasattr(exc_class, '__name__'):
                exc_name = exc_class.__name__
            else:
                exc_name = str(exc_class)
            self._msg = '%s not raised' % exc_name
        except exc_class:
            return

    def assertAlmostEqual(self, a, b, places=7, msg=None):
        if round(b - a, places) != 0.0:
            self._status = 'FAIL'
            self._msg = msg or '%f is not almost equal to %f' % (a, b)

    def assertNotAlmostEqual(self, a, b, places=7, msg=None):
        if round(b - a, places) == 0.0:
            self._status = 'FAIL'
            self._msg = msg or '%f is almost equal to %f' % (a, b)

    def assertGreater(self, a, b, msg=None):
        if not a > b:
            self._status = 'FAIL'
            self._msg = msg or '%f is not greater than %f' % (a, b)

    def assertGreaterEqual(self, a, b, msg=None):
        if not a >= b:
            self._status = 'FAIL'
            self._msg = msg or '%f is not greater than or equal to %f' % (a, b)

    def assertLess(self, a, b, msg=None):
        if not a < b:
            self._status = 'FAIL'
            self._msg = msg or '%f is not less than %f' % (a, b)

    def assertLessEqual(self, a, b, msg=None):
        if not a <= b:
            self._status = 'FAIL'
            self._msg = msg or '%f is not less than or equal to %f' % (a, b)


class ApplicationTestResultSet(object):
    """ keeps track of:
    - number of test classes
    - number of tests run
    - number of tests passed
    - number of tests that errored out
    - number of tests that failed
    - failed tests
    - errored tests
    """

    def __init__(self, num_test_classes=0, num_tests_run=0, num_tests_passed=0, num_tests_errored=0, num_tests_failed=0, failed=None, errored=None):
        self.num_test_classes = num_test_classes
        self.num_tests_run = num_tests_run
        self.num_tests_passed = num_tests_passed
        self.num_tests_errored = num_tests_errored
        self.num_tests_failed = num_tests_failed
        if failed is None:
            self.failed = []
        else:
            self.failed = failed
        if errored is None:
            self.errored = []
        else:
            self.errored = errored
        return

    def passed(self):
        return self.num_tests_passed == self.num_tests_run and self.num_tests_failed == 0 and self.num_tests_errored == 0