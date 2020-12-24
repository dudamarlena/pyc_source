# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ipython_doctester.py
# Compiled at: 2013-10-12 12:15:59
"""Run doctests on a single class or function, and report for IPython Notebook.

Decorate each function or class to be tested with ``ipython_doctester.test``.

If you want to turn off automatic testing but don't want to take the @test
decorators off, set ipython_doctester.run_tests = False.

Note: It's easy to cheat by simply deleting or changing the doctest.  That's
OK, cheating is learning, too.

If you want to track students' progress through a notebook in a
classroom setting, you can; see
http://ipython-docent.appspot.com/
for instructions.

Developed for the Dayton Python Workshop:
https://openhatch.org/wiki/Dayton_Python_Workshop
catherine.devlin@gmail.com

"""
import IPython, doctest, cgi, inspect, sys, os, os.path, requests
from IPython.core.displaypub import publish_display_data
try:
    from IPython.zmq import displayhook as zmq_displayhook
except ImportError:
    from IPython.kernel.zmq import displayhook as zmq_displayhook

__version__ = '0.3.0'
finder = doctest.DocTestFinder()
docent_url = 'http://ipython-docent.appspot.com'
doctest_path = './doctests'
run_tests = True
verbose = False
student_name = None
workshop_name = None

def running_from_notebook():
    return isinstance(sys.displayhook, zmq_displayhook.ZMQShellDisplayHook)


class Reporter(object):
    html = running_from_notebook()

    def __init__(self):
        self.failed = False
        self.examples = []
        self.txt = ''

    example_template = '<tr><td><code><pre>%s</pre></code></td><td><pre>%s</pre></td><td><pre style="color:%s">%s</pre></td></tr>'
    fail_template = '\n        <p><span style="color:red;">Oops!</span>  Not quite there yet...</p>\n      '
    success_template = '\n      <p style="color:green;font-size:250%;font-weight=bold">Success!</p>\n      '

    def trap_txt(self, txt):
        self.txt += txt

    def publish(self):
        if self.html:
            publish_display_data('ipython_doctester', {'text/html': self._repr_html_()})
        else:
            publish_display_data('ipython_doctester', {'text/plain': self.txt})

    def _repr_html_(self):
        result = self.fail_template if self.failed else self.success_template
        if verbose or self.failed:
            examples = ('\n        ').join(self.example_template % (cgi.escape(e.source), cgi.escape(e.want), e.color, cgi.escape(e.got)) for e in self.examples)
            result += '\n                       <table>\n                       <tr><th>Tried</th><th>Expected</th><th>Got</th></tr>' + examples + '\n                      </table>\n                      '
        return result


reporter = Reporter()

class Runner(doctest.DocTestRunner):

    def _or_nothing(self, x):
        if x in (None, ''):
            return 'Nothing'
        else:
            if hasattr(x, 'strip') and x.strip() == '':
                return '<BLANKLINE>'
            return x

    def report_failure(self, out, test, example, got):
        example.got = self._or_nothing(got)
        example.want = self._or_nothing(example.want)
        example.color = 'red'
        reporter.examples.append(example)
        reporter.failed = True
        return doctest.DocTestRunner.report_failure(self, out, test, example, got)

    def report_success(self, out, test, example, got):
        example.got = self._or_nothing(got)
        example.want = self._or_nothing(example.want)
        example.color = 'green'
        reporter.examples.append(example)
        return doctest.DocTestRunner.report_success(self, out, test, example, got)

    def report_unexpected_exception(self, out, test, example, exc_info):
        reporter.failed = True
        trim = len(reporter.txt)
        result = doctest.DocTestRunner.report_unexpected_exception(self, out, test, example, exc_info)
        example.got = reporter.txt[trim:].split('Exception raised:')[1]
        example.want = self._or_nothing(example.want)
        example.color = 'red'
        reporter.examples.append(example)
        return result


runner = Runner()
finder = doctest.DocTestFinder()

class IPythonDoctesterException(Exception):

    def _repr_html_(self):
        return '<pre>\n%s\n</pre>' % self.txt


class NoTestsException(IPythonDoctesterException):
    txt = "\n    OOPS!  We expected to find a doctest -\n    a string immediately after the function definition, looking something like\n        def do_something():\n            '''\n            >>> do_something()\n            'did something'\n            '''\n    ... but it wasn't there. Did you insert code between the function definition\n    and the doctest?\n    "


class NoStudentNameException(IPythonDoctesterException):
    txt = "\n    OOPS!  We need you to set the ipython_doctester.student_name variable;\n    please look for it (probably in the first cell in this worksheet) and\n    enter your name, like\n        ipython_doctester.student_name = 'Catherine'\n    ... then hit Shift+Enter to execute that cell, then come back here to\n    execute this one.\n    "


def testobj(func):
    tests = finder.find(func)
    if not tests or not tests[0].examples:
        doctest_filename = os.path.join(os.curdir, doctest_path, func.__name__) + '.txt'
        try:
            with open(doctest_filename) as (infile):
                func.__doc__ = (func.__doc__ or '') + '\n' + infile.read()
        except IOError:
            raise NoTestsException

        tests = finder.find(func)
        if not tests:
            raise NoTestsException
    if workshop_name and not student_name:
        raise NoStudentNameException()
    globs = {}
    reporter.__init__()
    globs[func.__name__] = func
    globs['reporter'] = reporter
    for t in tests:
        t.globs = globs.copy()
        runner.run(t, out=reporter.trap_txt)

    reporter.publish()
    if workshop_name:
        payload = dict(function_name=func.__name__, failure=reporter.failed, source=inspect.getsource(func), workshop_name=workshop_name, student_name=student_name)
        requests.post(docent_url + '/record', data=payload)
    return reporter


def test(func):
    if run_tests:
        try:
            result = testobj(func)
        except (NoStudentNameException, NoTestsException) as e:
            IPython.core.display.display(e)

    return func