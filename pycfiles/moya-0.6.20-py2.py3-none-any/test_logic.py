# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_logic.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
import os.path, unittest
from fs.opener import open_fs
from moya.context import Context
from moya.archive import Archive
from moya.console import Console
from moya.tags import context, config
BF_HELLO = b'\n++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.\n'

class TestLogic(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(os.path.dirname(__file__))
        self.fs = open_fs(path)
        self.context = Context()
        self.context[b'console'] = Console()
        self.archive = Archive()
        import_fs = self.fs.opendir(b'archivetest')
        self.archive.load_library(import_fs)
        self.archive.finalize()

    def test_setcontext(self):
        """Test setting values in the context"""
        c = self.context
        setcontext = self.archive.get_callable(b'moya.tests#setcontext')
        setcontext(c)
        self.assertEqual(c[b'foo'], 1)
        self.assertEqual(c[b'bar.baz'], b'Hello')
        self.assertEqual(c[b'half'], 0.5)
        self.assertEqual(c[b'bool'], True)
        self.assertEqual(c[b't'], True)
        self.assertEqual(c[b'f'], False)
        self.assertEqual(c[b'n'], None)
        self.assertEqual(c[b'l'], [])
        self.assertEqual(c[b'j'], {b'list': [1, 2, 3], b'map': dict(foo=10, bar=20)})
        self.assertEqual(c[b'fruit'], [b'apples', b'oranges', b'pears'])
        return

    def test_setcontext_by_value(self):
        """Test setting values from the 'value' attribute"""
        c = self.context
        self.archive(b'moya.tests#setcontextbyvalue', c, None)
        self.assertEqual(c[b'foo'], 10)
        self.assertEqual(c[b'bar'], 15)
        self.assertEqual(c[b'zero'], 0)
        self.assertEqual(c[b'empty'], b'')
        self.assertEqual(c[b'fruit'], b'apple')
        self.assertEqual(c[b'grapes'], b'grapegrapegrape')
        self.assertEqual(c[b'nograpes'], b"'grape'*3")
        self.assertEqual(c[b'pi'], 3.14)
        self.assertEqual(c[b'check'], True)
        self.assertEqual(c[b'check2'], False)
        self.assertEqual(c[b's'], 27)
        return

    def test_macro(self):
        """Test macro calling"""
        self.assertEqual(self.archive(b'moya.tests#macrotest1', self.context, None), 4)
        self.assertEqual(self.archive(b'moya.tests#macroreturnlist', self.context, None), [1, 2, 3])
        self.assertEqual(self.archive(b'moya.tests#testscope1', self.context, None)[b'b'], 2)
        self.assertEqual(self.archive(b'moya.tests#nested', self.context, None, 5), 10)
        self.assertEqual(self.archive(b'moya.tests#quadruple', self.context, None, 3), 12)
        return

    def test_ifelse(self):
        """Test if / elif /else"""
        tests = [
         (1, 'apple'),
         (2, 'orange'),
         (3, 'pear'),
         (4, 'not a fruit'),
         (5, 'not a fruit')]
        for n, correct in tests:
            result = self.archive(b'moya.tests#ifelse', self.context, None, n=n)
            self.assertEqual(result, correct)

        return

    def test_bf(self):
        """Test BF macro"""
        context = self.context
        call = self.archive.call
        result = call(b'moya.tests#bf', context, None, program=BF_HELLO)
        self.assertEqual(result, b'Hello World!\n')
        return