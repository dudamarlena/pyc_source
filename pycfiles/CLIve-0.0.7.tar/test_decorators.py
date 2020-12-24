# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/cliutils/tests/test_decorators.py
# Compiled at: 2008-10-04 00:19:08
import unittest, os, sys, tempfile
from StringIO import StringIO
from cliutils.decorators import cliargs, redirect, decorator, indir, logged

class TestDecorators(unittest.TestCase):
    __module__ = __name__

    def test_metadecorator(self):

        def adecorator(callable):

            def inner(*args, **kwargs):
                """Inner docstring"""
                return callable(*args, **kwargs)

            return inner

        decorated_adecorator = decorator(adecorator)

        @adecorator
        def badfunc(*args, **kwargs):
            """Docstring"""
            pass

        @decorated_adecorator
        def goodfunc(*args, **kwargs):
            """Docstring"""
            pass

        self.assertNotEqual(badfunc.__name__, 'badfunc')
        self.assertNotEqual(badfunc.__doc__, 'Docstring')
        self.assertEqual(goodfunc.__name__, 'goodfunc')
        self.assertEqual(goodfunc.__doc__, 'Docstring')

    def test_cliargs(self):

        @cliargs
        def func(*args, **kwargs):
            """Docstring"""
            return (
             args, kwargs)

        sys.argv[:] = ['executable.py', 'a', 'b', '-b', '--cde', 'fgh', 'c']
        (args, kwargs) = func()
        self.assertEqual(args, ('a', 'b', 'c'))
        self.assertEqual(kwargs, {'cde': 'fgh', 'b': True})

    def test_usage_failover(self):

        @cliargs
        def func(a, b, c, d=None):
            """Usage information"""
            pass

        sys.argv[:] = [
         'executable', 'a', 'b', 'c', '--e', 'f']
        sys.stdout = StringIO()
        func()
        sys.stdout.seek(0)
        result = sys.stdout.read()
        self.assertEqual(result.strip(), 'Usage information')
        return

    def test_redirect(self):
        s = StringIO()
        token = 'ABCDEFG'

        @redirect(s)
        def func():
            print token

        func()
        s.seek(0)
        result = s.read()
        self.assertEqual(result.strip(), token)

    def test_indir(self):
        d = os.path.realpath(tempfile.mkdtemp())
        curdir = os.path.realpath(os.curdir)
        self.assert_(d != curdir)

        @indir(d)
        def whereami():
            return os.path.realpath(os.curdir)

        newdir = whereami()
        self.assertEqual(newdir, d)
        self.assertEqual(os.path.realpath(os.curdir), curdir)


if __name__ == '__main__':
    unittest.main()