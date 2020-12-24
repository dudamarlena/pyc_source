# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/utils/testutils.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 10596 bytes
"""Utilities for writing tests.

- :class:`ParametricTestCase` provides a :meth:`TestCase.subTest` replacement
  for Python < 3.4
- :class:`TestLogging` with context or the :func:`test_logging` decorator
  enables testing the number of logging messages of different levels.
"""
__authors__ = [
 'T. Vincent']
__license__ = 'MIT'
__date__ = '26/01/2018'
import contextlib, functools, logging, sys, unittest
_logger = logging.getLogger(__name__)
if sys.hexversion >= 50594032:

    class ParametricTestCase(unittest.TestCase):
        pass


else:

    class ParametricTestCase(unittest.TestCase):
        __doc__ = 'TestCase with subTest support for Python < 3.4.\n\n        Add subTest method to support parametric tests.\n        API is the same, but behavior differs:\n        If a subTest fails, the following ones are not run.\n        '
        _subtest_msg = None

        @contextlib.contextmanager
        def subTest(self, msg=None, **params):
            """Use as unittest.TestCase.subTest method in Python >= 3.4."""
            param_str = ', '.join(['%s=%s' % (k, v) for k, v in params.items()])
            self._subtest_msg = '[%s] (%s)' % (msg or '', param_str)
            yield
            self._subtest_msg = None

        def shortDescription(self):
            short_desc = super(ParametricTestCase, self).shortDescription()
            if self._subtest_msg is not None:
                short_desc = ' '.join([msg for msg in (short_desc, self._subtest_msg) if msg])
            if short_desc:
                return short_desc


def parameterize(test_case_class, *args, **kwargs):
    """Create a suite containing all tests taken from the given
    subclass, passing them the parameters.

    .. code-block:: python

        class TestParameterizedCase(unittest.TestCase):
            def __init__(self, methodName='runTest', foo=None):
                unittest.TestCase.__init__(self, methodName)
                self.foo = foo

        def suite():
            testSuite = unittest.TestSuite()
            testSuite.addTest(parameterize(TestParameterizedCase, foo=10))
            testSuite.addTest(parameterize(TestParameterizedCase, foo=50))
            return testSuite
    """
    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(test_case_class)
    suite = unittest.TestSuite()
    for name in test_names:
        suite.addTest(test_case_class(name, *args, **kwargs))

    return suite


class TestLogging(logging.Handler):
    __doc__ = 'Context checking the number of logging messages from a specified Logger.\n\n    It disables propagation of logging message while running.\n\n    This is meant to be used as a with statement, for example:\n\n    >>> with TestLogging(logger, error=2, warning=0):\n    >>>     pass  # Run tests here expecting 2 ERROR and no WARNING from logger\n    ...\n\n    :param logger: Name or instance of the logger to test.\n                   (Default: root logger)\n    :type logger: str or :class:`logging.Logger`\n    :param int critical: Expected number of CRITICAL messages.\n                         Default: Do not check.\n    :param int error: Expected number of ERROR messages.\n                      Default: Do not check.\n    :param int warning: Expected number of WARNING messages.\n                        Default: Do not check.\n    :param int info: Expected number of INFO messages.\n                     Default: Do not check.\n    :param int debug: Expected number of DEBUG messages.\n                      Default: Do not check.\n    :param int notset: Expected number of NOTSET messages.\n                       Default: Do not check.\n    :raises RuntimeError: If the message counts are the expected ones.\n    '

    def __init__(self, logger=None, critical=None, error=None, warning=None, info=None, debug=None, notset=None):
        if logger is None:
            logger = logging.getLogger()
        elif not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)
        self.logger = logger
        self.records = []
        self.count_by_level = {logging.CRITICAL: critical, 
         logging.ERROR: error, 
         logging.WARNING: warning, 
         logging.INFO: info, 
         logging.DEBUG: debug, 
         logging.NOTSET: notset}
        super(TestLogging, self).__init__()

    def __enter__(self):
        """Context (i.e., with) support"""
        self.records = []
        self.logger.addHandler(self)
        self.logger.propagate = False
        self.entry_level = self.logger.level * 1
        self.logger.setLevel(logging.DEBUG)

    def __exit__(self, exc_type, exc_value, traceback):
        """Context (i.e., with) support"""
        self.logger.removeHandler(self)
        self.logger.propagate = True
        self.logger.setLevel(self.entry_level)
        for level, expected_count in self.count_by_level.items():
            if expected_count is None:
                pass
            else:
                count = len([r for r in self.records if r.levelno == level])
                if count != expected_count:
                    for record in self.records:
                        self.logger.handle(record)

                    raise RuntimeError('Expected %d %s logging messages, got %d' % (
                     expected_count, logging.getLevelName(level), count))

    def emit(self, record):
        """Override :meth:`logging.Handler.emit`"""
        self.records.append(record)


def test_logging(logger=None, critical=None, error=None, warning=None, info=None, debug=None, notset=None):
    """Decorator checking number of logging messages.

    Propagation of logging messages is disabled by this decorator.

    In case the expected number of logging messages is not found, it raises
    a RuntimeError.

    >>> class Test(unittest.TestCase):
    ...     @test_logging('module_logger_name', error=2, warning=0)
    ...     def test(self):
    ...         pass  # Test expecting 2 ERROR and 0 WARNING messages

    :param logger: Name or instance of the logger to test.
                   (Default: root logger)
    :type logger: str or :class:`logging.Logger`
    :param int critical: Expected number of CRITICAL messages.
                         Default: Do not check.
    :param int error: Expected number of ERROR messages.
                      Default: Do not check.
    :param int warning: Expected number of WARNING messages.
                        Default: Do not check.
    :param int info: Expected number of INFO messages.
                     Default: Do not check.
    :param int debug: Expected number of DEBUG messages.
                      Default: Do not check.
    :param int notset: Expected number of NOTSET messages.
                       Default: Do not check.
    """

    def decorator(func):
        test_context = TestLogging(logger, critical, error, warning, info, debug, notset)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with test_context:
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


class EnsureImportError(object):
    __doc__ = 'This context manager allows to simulate the unavailability\n    of a library, even if it is actually available. It ensures that\n    an ImportError is raised if the code inside the context tries to\n    import the module.\n\n    It can be used to test that a correct fallback library is used,\n    or that the expected error code is returned.\n\n    Trivial example::\n\n        from silx.utils.testutils import EnsureImportError\n\n        with EnsureImportError("h5py"):\n            try:\n                import h5py\n            except ImportError:\n                print("Good")\n\n    .. note::\n\n        This context manager does not remove the library from the namespace,\n        if it is already imported. It only ensures that any attempt to import\n        it again will cause an ImportError to be raised.\n    '

    def __init__(self, name):
        """

        :param str name: Name of module to be hidden (e.g. "h5py")
        """
        self.module_name = name

    def __enter__(self):
        """Simulate failed import by setting sys.modules[name]=None"""
        if self.module_name not in sys.modules:
            self._delete_on_exit = True
            self._backup = None
        else:
            self._delete_on_exit = False
            self._backup = sys.modules[self.module_name]
        sys.modules[self.module_name] = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore previous state"""
        if self._delete_on_exit:
            del sys.modules[self.module_name]
        else:
            sys.modules[self.module_name] = self._backup