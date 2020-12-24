# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_type_annotations.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 7834 bytes
"""
Tests for behaviour related to type annotations.
"""
from sys import version_info
from pyflakes import messages as m
from pyflakes.test.harness import TestCase, skipIf

class TestTypeAnnotations(TestCase):

    def test_typingOverload(self):
        """Allow intentional redefinitions via @typing.overload"""
        self.flakes('\n        import typing\n        from typing import overload\n\n        @overload\n        def f(s):  # type: (None) -> None\n            pass\n\n        @overload\n        def f(s):  # type: (int) -> int\n            pass\n\n        def f(s):\n            return s\n\n        @typing.overload\n        def g(s):  # type: (None) -> None\n            pass\n\n        @typing.overload\n        def g(s):  # type: (int) -> int\n            pass\n\n        def g(s):\n            return s\n        ')

    def test_not_a_typing_overload(self):
        """regression test for @typing.overload detection bug in 2.1.0"""
        self.flakes('\n            x = lambda f: f\n\n            @x\n            def t():\n                pass\n\n            y = lambda f: f\n\n            @x\n            @y\n            def t():\n                pass\n\n            @x\n            @y\n            def t():\n                pass\n        ', m.RedefinedWhileUnused, m.RedefinedWhileUnused)

    @skipIf(version_info < (3, 6), 'new in Python 3.6')
    def test_variable_annotations(self):
        self.flakes('\n        name: str\n        age: int\n        ')
        self.flakes("\n        name: str = 'Bob'\n        age: int = 18\n        ")
        self.flakes('\n        class C:\n            name: str\n            age: int\n        ')
        self.flakes("\n        class C:\n            name: str = 'Bob'\n            age: int = 18\n        ")
        self.flakes('\n        def f():\n            name: str\n            age: int\n        ')
        self.flakes("\n        def f():\n            name: str = 'Bob'\n            age: int = 18\n            foo: not_a_real_type = None\n        ", m.UnusedVariable, m.UnusedVariable, m.UnusedVariable, m.UndefinedName)
        self.flakes('\n        def f():\n            name: str\n            print(name)\n        ', m.UndefinedName)
        self.flakes('\n        from typing import Any\n        def f():\n            a: Any\n        ')
        self.flakes('\n        foo: not_a_real_type\n        ', m.UndefinedName)
        self.flakes('\n        foo: not_a_real_type = None\n        ', m.UndefinedName)
        self.flakes('\n        class C:\n            foo: not_a_real_type\n        ', m.UndefinedName)
        self.flakes('\n        class C:\n            foo: not_a_real_type = None\n        ', m.UndefinedName)
        self.flakes('\n        def f():\n            class C:\n                foo: not_a_real_type\n        ', m.UndefinedName)
        self.flakes('\n        def f():\n            class C:\n                foo: not_a_real_type = None\n        ', m.UndefinedName)
        self.flakes('\n        from foo import Bar\n        bar: Bar\n        ')
        self.flakes("\n        from foo import Bar\n        bar: 'Bar'\n        ")
        self.flakes('\n        import foo\n        bar: foo.Bar\n        ')
        self.flakes("\n        import foo\n        bar: 'foo.Bar'\n        ")
        self.flakes('\n        from foo import Bar\n        def f(bar: Bar): pass\n        ')
        self.flakes("\n        from foo import Bar\n        def f(bar: 'Bar'): pass\n        ")
        self.flakes('\n        from foo import Bar\n        def f(bar) -> Bar: return bar\n        ')
        self.flakes("\n        from foo import Bar\n        def f(bar) -> 'Bar': return bar\n        ")
        self.flakes("\n        bar: 'Bar'\n        ", m.UndefinedName)
        self.flakes("\n        bar: 'foo.Bar'\n        ", m.UndefinedName)
        self.flakes('\n        from foo import Bar\n        bar: str\n        ', m.UnusedImport)
        self.flakes('\n        from foo import Bar\n        def f(bar: str): pass\n        ', m.UnusedImport)
        self.flakes('\n        def f(a: A) -> A: pass\n        class A: pass\n        ', m.UndefinedName, m.UndefinedName)
        self.flakes("\n        def f(a: 'A') -> 'A': return a\n        class A: pass\n        ")
        self.flakes('\n        a: A\n        class A: pass\n        ', m.UndefinedName)
        self.flakes("\n        a: 'A'\n        class A: pass\n        ")
        self.flakes("\n        a: 'A B'\n        ", m.ForwardAnnotationSyntaxError)
        self.flakes("\n        a: 'A; B'\n        ", m.ForwardAnnotationSyntaxError)
        self.flakes("\n        a: '1 + 2'\n        ")
        self.flakes('\n        a: \'a: "A"\'\n        ', m.ForwardAnnotationSyntaxError)

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_annotated_async_def(self):
        self.flakes('\n        class c: pass\n        async def func(c: c) -> None: pass\n        ')

    @skipIf(version_info < (3, 7), 'new in Python 3.7')
    def test_postponed_annotations(self):
        self.flakes('\n        from __future__ import annotations\n        def f(a: A) -> A: pass\n        class A:\n            b: B\n        class B: pass\n        ')
        self.flakes('\n        from __future__ import annotations\n        def f(a: A) -> A: pass\n        class A:\n            b: Undefined\n        class B: pass\n        ', m.UndefinedName)

    def test_typeCommentsMarkImportsAsUsed(self):
        self.flakes('\n        from mod import A, B, C, D, E, F, G\n\n\n        def f(\n            a,  # type: A\n        ):\n            # type: (...) -> B\n            for b in a:  # type: C\n                with b as c:  # type: D\n                    d = c.x  # type: E\n                    return d\n\n\n        def g(x):  # type: (F) -> G\n            return x.y\n        ')

    def test_typeCommentsFullSignature(self):
        self.flakes('\n        from mod import A, B, C, D\n        def f(a, b):\n            # type: (A, B[C]) -> D\n            return a + b\n        ')

    def test_typeCommentsStarArgs(self):
        self.flakes('\n        from mod import A, B, C, D\n        def f(a, *b, **c):\n            # type: (A, *B, **C) -> D\n            return a + b\n        ')

    def test_typeCommentsFullSignatureWithDocstring(self):
        self.flakes('\n        from mod import A, B, C, D\n        def f(a, b):\n            # type: (A, B[C]) -> D\n            """do the thing!"""\n            return a + b\n        ')

    def test_typeCommentsAdditionalComemnt(self):
        self.flakes('\n        from mod import F\n\n        x = 1 # type: F  # noqa\n        ')

    def test_typeCommentsNoWhitespaceAnnotation(self):
        self.flakes('\n        from mod import F\n\n        x = 1  #type:F\n        ')

    def test_typeCommentsInvalidDoesNotMarkAsUsed(self):
        self.flakes('\n        from mod import F\n\n        # type: F\n        ', m.UnusedImport)

    def test_typeCommentsSyntaxError(self):
        self.flakes('\n        def f(x):  # type: (F[) -> None\n            pass\n        ', m.CommentAnnotationSyntaxError)

    def test_typeCommentsSyntaxErrorCorrectLine(self):
        checker = self.flakes('        x = 1\n        # type: definitely not a PEP 484 comment\n        ', m.CommentAnnotationSyntaxError)
        self.assertEqual(checker.messages[0].lineno, 2)

    def test_typeCommentsAssignedToPreviousNode(self):
        self.flakes('\n        from mod import F\n        x = 1\n        # type: F\n        ')