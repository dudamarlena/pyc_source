# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_doctests.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 12719 bytes
import sys, textwrap
from pyflakes import messages as m
from pyflakes.checker import DoctestScope, FunctionScope, ModuleScope
from pyflakes.test.test_other import Test as TestOther
from pyflakes.test.test_imports import Test as TestImports
from pyflakes.test.test_undefined_names import Test as TestUndefinedNames
from pyflakes.test.harness import TestCase, skip
try:
    sys.pypy_version_info
    PYPY = True
except AttributeError:
    PYPY = False

class _DoctestMixin(object):
    withDoctest = True

    def doctestify(self, input):
        lines = []
        for line in textwrap.dedent(input).splitlines():
            if line.strip() == '':
                pass
            else:
                if line.startswith(' ') or line.startswith('except:') or line.startswith('except ') or line.startswith('finally:') or line.startswith('else:') or line.startswith('elif ') or lines and lines[(-1)].startswith(('>>> @',
                                                                                                                                                                                                                                '... @')):
                    line = '... %s' % line
                else:
                    line = '>>> %s' % line
                lines.append(line)

        doctestificator = textwrap.dedent('            def doctest_something():\n                """\n                   %s\n                """\n            ')
        return doctestificator % '\n       '.join(lines)

    def flakes(self, input, *args, **kw):
        return (super(_DoctestMixin, self).flakes)(self.doctestify(input), *args, **kw)


class Test(TestCase):
    withDoctest = True

    def test_scope_class(self):
        """Check that a doctest is given a DoctestScope."""
        checker = self.flakes("\n        m = None\n\n        def doctest_stuff():\n            '''\n                >>> d = doctest_stuff()\n            '''\n            f = m\n            return f\n        ")
        scopes = checker.deadScopes
        module_scopes = [scope for scope in scopes if scope.__class__ is ModuleScope]
        doctest_scopes = [scope for scope in scopes if scope.__class__ is DoctestScope]
        function_scopes = [scope for scope in scopes if scope.__class__ is FunctionScope]
        self.assertEqual(len(module_scopes), 1)
        self.assertEqual(len(doctest_scopes), 1)
        module_scope = module_scopes[0]
        doctest_scope = doctest_scopes[0]
        self.assertIsInstance(doctest_scope, DoctestScope)
        self.assertIsInstance(doctest_scope, ModuleScope)
        self.assertNotIsInstance(doctest_scope, FunctionScope)
        self.assertNotIsInstance(module_scope, DoctestScope)
        self.assertIn('m', module_scope)
        self.assertIn('doctest_stuff', module_scope)
        self.assertIn('d', doctest_scope)
        self.assertEqual(len(function_scopes), 1)
        self.assertIn('f', function_scopes[0])

    def test_nested_doctest_ignored(self):
        """Check that nested doctests are ignored."""
        checker = self.flakes('\n        m = None\n\n        def doctest_stuff():\n            \'\'\'\n                >>> def function_in_doctest():\n                ...     """\n                ...     >>> ignored_undefined_name\n                ...     """\n                ...     df = m\n                ...     return df\n                ...\n                >>> function_in_doctest()\n            \'\'\'\n            f = m\n            return f\n        ')
        scopes = checker.deadScopes
        module_scopes = [scope for scope in scopes if scope.__class__ is ModuleScope]
        doctest_scopes = [scope for scope in scopes if scope.__class__ is DoctestScope]
        function_scopes = [scope for scope in scopes if scope.__class__ is FunctionScope]
        self.assertEqual(len(module_scopes), 1)
        self.assertEqual(len(doctest_scopes), 1)
        module_scope = module_scopes[0]
        doctest_scope = doctest_scopes[0]
        self.assertIn('m', module_scope)
        self.assertIn('doctest_stuff', module_scope)
        self.assertIn('function_in_doctest', doctest_scope)
        self.assertEqual(len(function_scopes), 2)
        self.assertIn('f', function_scopes[0])
        self.assertIn('df', function_scopes[1])

    def test_global_module_scope_pollution(self):
        """Check that global in doctest does not pollute module scope."""
        checker = self.flakes("\n        def doctest_stuff():\n            '''\n                >>> def function_in_doctest():\n                ...     global m\n                ...     m = 50\n                ...     df = 10\n                ...     m = df\n                ...\n                >>> function_in_doctest()\n            '''\n            f = 10\n            return f\n\n        ")
        scopes = checker.deadScopes
        module_scopes = [scope for scope in scopes if scope.__class__ is ModuleScope]
        doctest_scopes = [scope for scope in scopes if scope.__class__ is DoctestScope]
        function_scopes = [scope for scope in scopes if scope.__class__ is FunctionScope]
        self.assertEqual(len(module_scopes), 1)
        self.assertEqual(len(doctest_scopes), 1)
        module_scope = module_scopes[0]
        doctest_scope = doctest_scopes[0]
        self.assertIn('doctest_stuff', module_scope)
        self.assertIn('function_in_doctest', doctest_scope)
        self.assertEqual(len(function_scopes), 2)
        self.assertIn('f', function_scopes[0])
        self.assertIn('df', function_scopes[1])
        self.assertIn('m', function_scopes[1])
        self.assertNotIn('m', module_scope)

    def test_global_undefined(self):
        self.flakes("\n        global m\n\n        def doctest_stuff():\n            '''\n                >>> m\n            '''\n        ", m.UndefinedName)

    def test_nested_class(self):
        """Doctest within nested class are processed."""
        self.flakes("\n        class C:\n            class D:\n                '''\n                    >>> m\n                '''\n                def doctest_stuff(self):\n                    '''\n                        >>> m\n                    '''\n                    return 1\n        ", m.UndefinedName, m.UndefinedName)

    def test_ignore_nested_function(self):
        """Doctest module does not process doctest in nested functions."""
        self.flakes("\n        def doctest_stuff():\n            def inner_function():\n                '''\n                    >>> syntax error\n                    >>> inner_function()\n                    1\n                    >>> m\n                '''\n                return 1\n            m = inner_function()\n            return m\n        ")

    def test_inaccessible_scope_class(self):
        """Doctest may not access class scope."""
        self.flakes("\n        class C:\n            def doctest_stuff(self):\n                '''\n                    >>> m\n                '''\n                return 1\n            m = 1\n        ", m.UndefinedName)

    def test_importBeforeDoctest(self):
        self.flakes("\n        import foo\n\n        def doctest_stuff():\n            '''\n                >>> foo\n            '''\n        ")

    @skip('todo')
    def test_importBeforeAndInDoctest(self):
        self.flakes('\n        import foo\n\n        def doctest_stuff():\n            """\n                >>> import foo\n                >>> foo\n            """\n\n        foo\n        ', m.RedefinedWhileUnused)

    def test_importInDoctestAndAfter(self):
        self.flakes('\n        def doctest_stuff():\n            """\n                >>> import foo\n                >>> foo\n            """\n\n        import foo\n        foo()\n        ')

    def test_offsetInDoctests(self):
        exc = self.flakes('\n\n        def doctest_stuff():\n            """\n                >>> x # line 5\n            """\n\n        ', m.UndefinedName).messages[0]
        self.assertEqual(exc.lineno, 5)
        self.assertEqual(exc.col, 12)

    def test_offsetInLambdasInDoctests(self):
        exc = self.flakes('\n\n        def doctest_stuff():\n            """\n                >>> lambda: x # line 5\n            """\n\n        ', m.UndefinedName).messages[0]
        self.assertEqual(exc.lineno, 5)
        self.assertEqual(exc.col, 20)

    def test_offsetAfterDoctests(self):
        exc = self.flakes('\n\n        def doctest_stuff():\n            """\n                >>> x = 5\n            """\n\n        x\n\n        ', m.UndefinedName).messages[0]
        self.assertEqual(exc.lineno, 8)
        self.assertEqual(exc.col, 0)

    def test_syntaxErrorInDoctest(self):
        exceptions = self.flakes('\n            def doctest_stuff():\n                """\n                    >>> from # line 4\n                    >>>     fortytwo = 42\n                    >>> except Exception:\n                """\n            ', m.DoctestSyntaxError, m.DoctestSyntaxError, m.DoctestSyntaxError).messages
        exc = exceptions[0]
        self.assertEqual(exc.lineno, 4)
        if sys.version_info >= (3, 8):
            self.assertEqual(exc.col, 18)
        else:
            self.assertEqual(exc.col, 26)
        exc = exceptions[1]
        self.assertEqual(exc.lineno, 5)
        if PYPY:
            self.assertEqual(exc.col, 13)
        else:
            self.assertEqual(exc.col, 16)
        exc = exceptions[2]
        self.assertEqual(exc.lineno, 6)
        if PYPY or sys.version_info >= (3, 8):
            self.assertEqual(exc.col, 13)
        else:
            self.assertEqual(exc.col, 18)

    def test_indentationErrorInDoctest(self):
        exc = self.flakes('\n        def doctest_stuff():\n            """\n                >>> if True:\n                ... pass\n            """\n        ', m.DoctestSyntaxError).messages[0]
        self.assertEqual(exc.lineno, 5)
        if PYPY or sys.version_info >= (3, 8):
            self.assertEqual(exc.col, 13)
        else:
            self.assertEqual(exc.col, 16)

    def test_offsetWithMultiLineArgs(self):
        exc1, exc2 = self.flakes('\n            def doctest_stuff(arg1,\n                              arg2,\n                              arg3):\n                """\n                    >>> assert\n                    >>> this\n                """\n            ', m.DoctestSyntaxError, m.UndefinedName).messages
        self.assertEqual(exc1.lineno, 6)
        self.assertEqual(exc1.col, 19)
        self.assertEqual(exc2.lineno, 7)
        self.assertEqual(exc2.col, 12)

    def test_doctestCanReferToFunction(self):
        self.flakes("\n        def foo():\n            '''\n                >>> foo\n            '''\n        ")

    def test_doctestCanReferToClass(self):
        self.flakes("\n        class Foo():\n            '''\n                >>> Foo\n            '''\n            def bar(self):\n                '''\n                    >>> Foo\n                '''\n        ")

    def test_noOffsetSyntaxErrorInDoctest(self):
        exceptions = self.flakes('\n            def buildurl(base, *args, **kwargs):\n                """\n                >>> buildurl(\'/blah.php\', (\'a\', \'&\'), (\'b\', \'=\')\n                \'/blah.php?a=%26&b=%3D\'\n                >>> buildurl(\'/blah.php\', a=\'&\', \'b\'=\'=\')\n                \'/blah.php?b=%3D&a=%26\'\n                """\n                pass\n            ', m.DoctestSyntaxError, m.DoctestSyntaxError).messages
        exc = exceptions[0]
        self.assertEqual(exc.lineno, 4)
        exc = exceptions[1]
        self.assertEqual(exc.lineno, 6)

    def test_singleUnderscoreInDoctest(self):
        self.flakes('\n        def func():\n            """A docstring\n\n            >>> func()\n            1\n            >>> _\n            1\n            """\n            return 1\n        ')


class TestOther(_DoctestMixin, TestOther):
    __doc__ = 'Run TestOther with each test wrapped in a doctest.'


class TestImports(_DoctestMixin, TestImports):
    __doc__ = 'Run TestImports with each test wrapped in a doctest.'


class TestUndefinedNames(_DoctestMixin, TestUndefinedNames):
    __doc__ = 'Run TestUndefinedNames with each test wrapped in a doctest.'