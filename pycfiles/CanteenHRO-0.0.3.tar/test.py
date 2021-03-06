# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/test.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  tests\n  ~~~~~\n\n  utilities for providing unittest functionality.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
from __future__ import print_function
import os, sys, unittest, itertools
from .core import meta
from .core import Library
from .util import config
from .util import ObjectProxy
from .dispatch import spawn
from .logic.http import semantics
combine = lambda *t: tuple(itertools.chain(*t))
_get_app = lambda s, k: k.get('app', s.dispatch_endpoint())
_dispatch = lambda m, s, a, k: s.dispatch(*combine((_get_app(s, k), m), a), **k)

class BaseTest(unittest.TestCase):
    """ Provides base code testing functionality, both for framework testing
        and testing of applications written with Canteen. """
    __appconfig__ = None
    __orig_testing__ = None

    @classmethod
    def setUpClass(cls):
        """ Test class setup hook, in this case used for forcing the env var
          ``CANTEEN_TESTING`` to exist.

          :returns: ``None``. """
        if 'CANTEEN_TESTING' not in os.environ:
            cls.__orig_testing__ = False
            os.environ['CANTEEN_TESTING'] = 'on'
        super(BaseTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """ Test class teardown hook, in this case used to remove the env var
          ``CANTEEN_TESTING`` if it was forced into existence.

          :returns: ``None``. """
        if not cls.__orig_testing__:
            del os.environ['CANTEEN_TESTING']

    @classmethod
    def set_config(cls, target):
        """ Set app configuration to a testing-compatible active set.

          :param target: :py:class:`canteen.util.config.Config` instance that
            contains app/framework configuration to be used during testing.

          :returns: ``cls``, for chainability. """
        return setattr(cls, '__appconfig__', target) or cls

    with Library('werkzeug', strict=True) as (library, werkzeug):
        __werkzeug__ = ObjectProxy({'test': library.load('test'), 
           'testapp': library.load('testapp'), 
           'wrappers': library.load('wrappers')})

        def dispatch_endpoint(self):
            """ Internal function to spawn a throwaway app instance for issuing a
            one-shot dispatch.

            :returns: Instance of :py:class:`canteen.core.Runtime`, for
              whichever runtime is active for the target app. """
            return spawn(None, config=config.Config(**self.__appconfig__))

        def _spawn_client(self, wsgi_target=None):
            """ Internal function to spawn a throwaway :py:mod:`werkzeug`-based HTTP
            :py:class:`werkzeug.test.Client` instance, for the purpose of
            executing WSGI dispatch during testing.

            :param wsgi_target: Target WSGI application to dispatch against.
              Defaults to ``None``, indicating that a reference WSGI app (known
              to be good) should be used in its place.

            :returns: Prepared :py:class:`werkzeug.test.Client` instance, with
              the target ``wsgi_target`` wrapped and ready to dispatch. """
            return self.__werkzeug__.test.Client(*(
             wsgi_target or self.__werkzeug__.testapp.test_app,
             semantics.HTTPSemantics.HTTPResponse))

        def dispatch(self, app, method, *args, **kwargs):
            """ Perform a WSGI dispatch against ``app``, with HTTP ``method`` and
            pass position ``args`` and keyword ``kwargs``.

            :param app: WSGI application to dispatch against.

            :param method: HTTP method to dispatch in target ``app``.

            :param *args: Positional arguments to pass to the Werkzeug test
              client dispatch method.

            :param **kwargs: Keyword arguments to pass to the Werkzeug test
              client dispatch method.

            :returns: Result of dispatching ``method`` against ``app`` via
              WSGI. """
            return getattr(self._spawn_client(app), method.lower())(*args, **kwargs)

        GET = lambda self, *a, **k: _dispatch('GET', self, a, k)
        PUT = lambda self, *a, **k: _dispatch('PUT', self, a, k)
        POST = lambda self, *a, **k: _dispatch('POST', self, a, k)
        HEAD = lambda self, *a, **k: _dispatch('HEAD', self, a, k)
        TRACE = lambda self, *a, **k: _dispatch('TRACE', self, a, k)
        PATCH = lambda self, *a, **k: _dispatch('PATCH', self, a, k)
        PURGE = lambda self, *a, **k: _dispatch('PURGE', self, a, k)
        DELETE = lambda self, *a, **k: _dispatch('DELETE', self, a, k)
        OPTIONS = lambda self, *a, **k: _dispatch('OPTIONS', self, a, k)
        CONNECT = lambda self, *a, **k: _dispatch('CONNECT', self, a, k)


class AppTest(BaseTest):
    """ Provides an extension point for application developers to write tests
        against applications written for ``Canteen``. """
    __root__, __owner__, __metaclass__ = True, 'AppTest', meta.Proxy.Registry


class FrameworkTest(BaseTest):
    """ Provides an extension point for Canteen developers (on the framework
        itself) to create tests for builtin functionality. """
    __root__, __owner__, __metaclass__ = True, 'FrameworkTest', meta.Proxy.Registry


def run(output=None, suites=None, scope=(
 AppTest, FrameworkTest), _format='text', verbosity=1, **kwargs):
    """ Run a suite of test cases with an optional output plan, and optionally
        scoping to only framework or application tests.

         :param output:
         :param suites:
         :param scope:
         :param _format:
         :param verbosity:
         :param kwargs:

         :returns: """
    master_suite, loader = [], unittest.TestLoader()
    for bucket in scope:
        suite = unittest.TestSuite()
        for child in bucket.iter_children():
            suite.addTests(loader.loadTestsFromTestCase(child))

        master_suite.append(suite)

    if suites:
        for _suite in suites:
            master_suite.append(_suite)

    def filter_suite(_s):
        """ Filter whole testsuites from being run by this tool if they don't
          contain any substantive tests.

          :param _s: Testsuite to filter.

          :returns: ``True`` if the testsuite should be run, ``False``
            otherwise. """
        if not _s.countTestCases():
            return False
        return True

    _seen_tests = set()

    def merge_suite(left, right):
        """ Merge two testsuites' containing tests, into one testsuite.

          :param left: The first testsuite to merge from.
          :param right: The other testsuite to merge from.

          :returns: :py:class:`unittest.TestSuite` instance merged of all tests
            contained in ``left`` and ``right``. """
        _master = []
        for case in [ test for test in left ] + [ test for test in right ]:
            if isinstance(case, unittest.TestSuite):
                for _case in case:
                    _master.append(_case)
                    _seen_tests.add(_case)

                continue
            if case not in _seen_tests:
                _master.append(case)
                _seen_tests.add(case)
            else:
                continue

        return set(unittest.TestSuite(_master))

    master_suite = unittest.TestSuite(reduce(merge_suite, filter(filter_suite, master_suite)))
    if _format == 'xml':
        if output is None:
            output = '.develop/tests'
        try:
            import xmlrunner
            return xmlrunner.XMLTestRunner(output=output).run(master_suite)
        except ImportError:
            xmlrunner = False
            raise RuntimeError('Cannot generate XML output without `xmlrunner`.')

    runner = unittest.TextTestRunner(stream=(output or sys.stdout), verbosity=verbosity, **kwargs)
    return runner.run(master_suite)


def clirunner(arguments, root=None):
    """ Discover and run known testsuites. Optionally scope to a certain
        ``root`` directory, or provide alternate output options.

        :param arguments: Command-line arguments.
        :param root: Root directory to run tests from.

        :returns: Nothing, as ``sys.exit`` is called from this tool. """
    output, _format = (None, 'text')
    if not __debug__:
        raise RuntimeError('Cannot run tests with -O or -OO.')
    if not root:
        root = os.getcwd()
    if arguments:
        if len(arguments) > 2:
            print('Can only call with a maximum of 2 arguments: FORMAT and OUTPUT, or just FORMAT.')
            sys.exit(1)
        if len(arguments) == 2:
            _format, output = tuple(arguments)
        else:
            _format = arguments[0]
    discovered = None
    if root:
        loader = unittest.TestLoader()
        discovered = loader.discover(root)
    try:
        run(**{'output': output or (sys.stdout if _format is 'text' else None), 
           'suites': discovered, 
           'format': _format, 
           'verbosity': 5 if 'TEST_VERBOSE' in os.environ else 0 if 'TEST_QUIET' in os.environ else 1})
    except Exception as e:
        print(e)
        sys.exit(1)
    else:
        sys.exit(0)

    return