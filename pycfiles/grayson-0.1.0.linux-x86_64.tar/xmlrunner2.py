# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/xmlrunner2.py
# Compiled at: 2012-03-02 14:59:52
"""
XML Test Runner for PyUnit
"""
from __future__ import with_statement
__version__ = '0.1'
import os.path, re, sys, time, traceback, unittest
from xml.sax.saxutils import escape
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class _TestInfo(object):
    """Information about a particular test.
    
    Used by _XMLTestResult.
    
    """

    def __init__(self, test, time):
        self._class, self._method = test.id().rsplit('.', 1)
        self._time = time
        self._error = None
        self._failure = None
        return

    @staticmethod
    def create_success(test, time):
        """Create a _TestInfo instance for a successful test."""
        return _TestInfo(test, time)

    @staticmethod
    def create_failure(test, time, failure):
        """Create a _TestInfo instance for a failed test."""
        info = _TestInfo(test, time)
        info._failure = failure
        return info

    @staticmethod
    def create_error(test, time, error):
        """Create a _TestInfo instance for an erroneous test."""
        info = _TestInfo(test, time)
        info._error = error
        return info

    def print_report(self, stream):
        """Print information about this test case in XML format to the
        supplied stream.

        """
        stream.write('  <testcase classname="%(class)s" name="%(method)s" time="%(time).4f">' % {'class': self._class, 
           'method': self._method, 
           'time': self._time})
        if self._failure is not None:
            self._print_error(stream, 'failure', self._failure)
        if self._error is not None:
            self._print_error(stream, 'error', self._error)
        stream.write('</testcase>\n')
        return

    def _print_error(self, stream, tagname, error):
        """Print information from a failure or error to the supplied stream."""
        text = escape(str(error[1]))
        stream.write('\n')
        stream.write('    <%s type="%s">%s\n' % (
         tagname, _clsname(error[0]), text))
        tb_stream = StringIO()
        traceback.print_tb(error[2], None, tb_stream)
        stream.write(escape(tb_stream.getvalue()))
        stream.write('    </%s>\n' % tagname)
        stream.write('  ')
        return


def _clsname(cls):
    return cls.__module__ + '.' + cls.__name__


class _XMLTestResult(unittest.TestResult):
    """A test result class that stores result as XML.

    Used by XMLTestRunner.

    """

    def __init__(self, classname):
        unittest.TestResult.__init__(self)
        self._test_name = classname
        self._start_time = None
        self._tests = []
        self._error = None
        self._failure = None
        return

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self._error = None
        self._failure = None
        self._start_time = time.time()
        return

    def stopTest(self, test):
        time_taken = time.time() - self._start_time
        unittest.TestResult.stopTest(self, test)
        if self._error:
            info = _TestInfo.create_error(test, time_taken, self._error)
        elif self._failure:
            info = _TestInfo.create_failure(test, time_taken, self._failure)
        else:
            info = _TestInfo.create_success(test, time_taken)
        self._tests.append(info)

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self._error = err

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self._failure = err

    def print_report(self, stream, time_taken, out, err):
        """Prints the XML report to the supplied stream.
        
        The time the tests took to perform as well as the captured standard
        output and standard error streams must be passed in.a

        """
        stream.write('<testsuite errors="%(e)d" failures="%(f)d" ' % {'e': len(self.errors), 'f': len(self.failures)})
        stream.write('name="%(n)s" tests="%(t)d" time="%(time).3f">\n' % {'n': self._test_name, 
           't': self.testsRun, 
           'time': time_taken})
        for info in self._tests:
            info.print_report(stream)

        stream.write('  <system-out><![CDATA[%s]]></system-out>\n' % out)
        stream.write('  <system-err><![CDATA[%s]]></system-err>\n' % err)
        stream.write('</testsuite>\n')


class XMLTestRunner(object):
    """A test runner that stores results in XML format compatible with JUnit.

    XMLTestRunner(stream=None) -> XML test runner

    The XML file is written to the supplied stream. If stream is None, the
    results are stored in a file called TEST-<module>.<class>.xml in the
    current working directory (if not overridden with the path property),
    where <module> and <class> are the module and class name of the test class.

    """

    def __init__(self, stream=None):
        self._stream = stream
        self._path = '.'

    def run(self, test):
        """Run the given test case or test suite."""
        class_ = test.__class__
        classname = class_.__module__ + '.' + class_.__name__
        if self._stream == None:
            filename = 'TEST-%s.xml' % classname
            stream = file(os.path.join(self._path, filename), 'w')
            stream.write('<?xml version="1.0" encoding="utf-8"?>\n')
        else:
            stream = self._stream
        result = _XMLTestResult(classname)
        start_time = time.time()
        with _fake_std_streams():
            test(result)
            try:
                out_s = sys.stdout.getvalue()
            except AttributeError:
                out_s = ''

            try:
                err_s = sys.stderr.getvalue()
            except AttributeError:
                err_s = ''

        time_taken = time.time() - start_time
        result.print_report(stream, time_taken, out_s, err_s)
        if self._stream is None:
            stream.close()
        return result

    def _set_path(self, path):
        self._path = path

    path = property(lambda self: self._path, _set_path, None, 'The path where the XML files are stored.\n            \n            This property is ignored when the XML file is written to a file\n            stream.')


class _fake_std_streams(object):

    def __enter__(self):
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr


class XMLTestRunnerTest(unittest.TestCase):

    def setUp(self):
        self._stream = StringIO()

    def _try_test_run(self, test_class, expected):
        """Run the test suite against the supplied test class and compare the
        XML result against the expected XML string. Fail if the expected
        string doesn't match the actual string. All time attributes in the
        expected string should have the value "0.000". All error and failure
        messages are reduced to "Foobar".

        """
        runner = XMLTestRunner(self._stream)
        runner.run(unittest.makeSuite(test_class))
        got = self._stream.getvalue()
        got = re.sub('time="\\d+\\.\\d+"', 'time="0.000"', got)
        got = re.sub('(?s)<failure (.*?)>.*?</failure>', '<failure \\1>Foobar</failure>', got)
        got = re.sub('(?s)<error (.*?)>.*?</error>', '<error \\1>Foobar</error>', got)
        got = got.replace('type="builtins.', 'type="exceptions.')
        self.assertEqual(expected, got)

    def test_no_tests(self):
        """Regression test: Check whether a test run without any tests
        matches a previous run.
        
        """

        class TestTest(unittest.TestCase):
            pass

        self._try_test_run(TestTest, '<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="0" time="0.000">\n  <system-out><![CDATA[]]></system-out>\n  <system-err><![CDATA[]]></system-err>\n</testsuite>\n')

    def test_success(self):
        """Regression test: Check whether a test run with a successful test
        matches a previous run.
        
        """

        class TestTest(unittest.TestCase):

            def test_foo(self):
                pass

        self._try_test_run(TestTest, '<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="1" time="0.000">\n  <testcase classname="__main__.TestTest" name="test_foo" time="0.000"></testcase>\n  <system-out><![CDATA[]]></system-out>\n  <system-err><![CDATA[]]></system-err>\n</testsuite>\n')

    def test_failure(self):
        """Regression test: Check whether a test run with a failing test
        matches a previous run.
        
        """

        class TestTest(unittest.TestCase):

            def test_foo(self):
                self.assert_(False)

        self._try_test_run(TestTest, '<testsuite errors="0" failures="1" name="unittest.TestSuite" tests="1" time="0.000">\n  <testcase classname="__main__.TestTest" name="test_foo" time="0.000">\n    <failure type="exceptions.AssertionError">Foobar</failure>\n  </testcase>\n  <system-out><![CDATA[]]></system-out>\n  <system-err><![CDATA[]]></system-err>\n</testsuite>\n')

    def test_error(self):
        """Regression test: Check whether a test run with a erroneous test
        matches a previous run.
        
        """

        class TestTest(unittest.TestCase):

            def test_foo(self):
                raise IndexError()

        self._try_test_run(TestTest, '<testsuite errors="1" failures="0" name="unittest.TestSuite" tests="1" time="0.000">\n  <testcase classname="__main__.TestTest" name="test_foo" time="0.000">\n    <error type="exceptions.IndexError">Foobar</error>\n  </testcase>\n  <system-out><![CDATA[]]></system-out>\n  <system-err><![CDATA[]]></system-err>\n</testsuite>\n')

    def test_stdout_capture(self):
        """Regression test: Check whether a test run with output to stdout
        matches a previous run.
        
        """

        class TestTest(unittest.TestCase):

            def test_foo(self):
                sys.stdout.write('Test\n')

        self._try_test_run(TestTest, '<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="1" time="0.000">\n  <testcase classname="__main__.TestTest" name="test_foo" time="0.000"></testcase>\n  <system-out><![CDATA[Test\n]]></system-out>\n  <system-err><![CDATA[]]></system-err>\n</testsuite>\n')

    def test_stderr_capture(self):
        """Regression test: Check whether a test run with output to stderr
        matches a previous run.
        
        """

        class TestTest(unittest.TestCase):

            def test_foo(self):
                sys.stderr.write('Test\n')

        self._try_test_run(TestTest, '<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="1" time="0.000">\n  <testcase classname="__main__.TestTest" name="test_foo" time="0.000"></testcase>\n  <system-out><![CDATA[]]></system-out>\n  <system-err><![CDATA[Test\n]]></system-err>\n</testsuite>\n')

    class NullStream(object):
        """A file-like object that discards everything written to it."""

        def write(self, buffer):
            pass

    def test_unittests_changing_stdout(self):
        """Check whether the XMLTestRunner recovers gracefully from unit tests
        that change stdout, but don't change it back properly.

        """

        class TestTest(unittest.TestCase):

            def test_foo(self):
                sys.stdout = XMLTestRunnerTest.NullStream()

        runner = XMLTestRunner(self._stream)
        runner.run(unittest.makeSuite(TestTest))

    def test_unittests_changing_stderr(self):
        """Check whether the XMLTestRunner recovers gracefully from unit tests
        that change stderr, but don't change it back properly.

        """

        class TestTest(unittest.TestCase):

            def test_foo(self):
                sys.stderr = XMLTestRunnerTest.NullStream()

        runner = XMLTestRunner(self._stream)
        runner.run(unittest.makeSuite(TestTest))


if __name__ == '__main__':
    unittest.main()