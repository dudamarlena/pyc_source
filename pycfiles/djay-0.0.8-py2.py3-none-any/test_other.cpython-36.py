# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_other.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 48418 bytes
"""
Tests for various Pyflakes behavior.
"""
from sys import version_info
from pyflakes import messages as m
from pyflakes.test.harness import TestCase, skip, skipIf

class Test(TestCase):

    def test_duplicateArgs(self):
        self.flakes('def fu(bar, bar): pass', m.DuplicateArgument)

    def test_localReferencedBeforeAssignment(self):
        self.flakes('\n        a = 1\n        def f():\n            a; a=1\n        f()\n        ', m.UndefinedLocal, m.UnusedVariable)

    @skipIf(version_info >= (3, ), 'in Python 3 list comprehensions execute in a separate scope')
    def test_redefinedInListComp(self):
        """
        Test that shadowing a variable in a list comprehension raises
        a warning.
        """
        self.flakes('\n        a = 1\n        [1 for a, b in [(1, 2)]]\n        ', m.RedefinedInListComp)
        self.flakes('\n        class A:\n            a = 1\n            [1 for a, b in [(1, 2)]]\n        ', m.RedefinedInListComp)
        self.flakes('\n        def f():\n            a = 1\n            [1 for a, b in [(1, 2)]]\n        ', m.RedefinedInListComp)
        self.flakes('\n        [1 for a, b in [(1, 2)]]\n        [1 for a, b in [(1, 2)]]\n        ')
        self.flakes('\n        for a, b in [(1, 2)]:\n            pass\n        [1 for a, b in [(1, 2)]]\n        ')

    def test_redefinedInGenerator(self):
        """
        Test that reusing a variable in a generator does not raise
        a warning.
        """
        self.flakes('\n        a = 1\n        (1 for a, b in [(1, 2)])\n        ')
        self.flakes('\n        class A:\n            a = 1\n            list(1 for a, b in [(1, 2)])\n        ')
        self.flakes('\n        def f():\n            a = 1\n            (1 for a, b in [(1, 2)])\n        ', m.UnusedVariable)
        self.flakes('\n        (1 for a, b in [(1, 2)])\n        (1 for a, b in [(1, 2)])\n        ')
        self.flakes('\n        for a, b in [(1, 2)]:\n            pass\n        (1 for a, b in [(1, 2)])\n        ')

    def test_redefinedInSetComprehension(self):
        """
        Test that reusing a variable in a set comprehension does not raise
        a warning.
        """
        self.flakes('\n        a = 1\n        {1 for a, b in [(1, 2)]}\n        ')
        self.flakes('\n        class A:\n            a = 1\n            {1 for a, b in [(1, 2)]}\n        ')
        self.flakes('\n        def f():\n            a = 1\n            {1 for a, b in [(1, 2)]}\n        ', m.UnusedVariable)
        self.flakes('\n        {1 for a, b in [(1, 2)]}\n        {1 for a, b in [(1, 2)]}\n        ')
        self.flakes('\n        for a, b in [(1, 2)]:\n            pass\n        {1 for a, b in [(1, 2)]}\n        ')

    def test_redefinedInDictComprehension(self):
        """
        Test that reusing a variable in a dict comprehension does not raise
        a warning.
        """
        self.flakes('\n        a = 1\n        {1: 42 for a, b in [(1, 2)]}\n        ')
        self.flakes('\n        class A:\n            a = 1\n            {1: 42 for a, b in [(1, 2)]}\n        ')
        self.flakes('\n        def f():\n            a = 1\n            {1: 42 for a, b in [(1, 2)]}\n        ', m.UnusedVariable)
        self.flakes('\n        {1: 42 for a, b in [(1, 2)]}\n        {1: 42 for a, b in [(1, 2)]}\n        ')
        self.flakes('\n        for a, b in [(1, 2)]:\n            pass\n        {1: 42 for a, b in [(1, 2)]}\n        ')

    def test_redefinedFunction(self):
        """
        Test that shadowing a function definition with another one raises a
        warning.
        """
        self.flakes('\n        def a(): pass\n        def a(): pass\n        ', m.RedefinedWhileUnused)

    def test_redefinedUnderscoreFunction(self):
        """
        Test that shadowing a function definition named with underscore doesn't
        raise anything.
        """
        self.flakes('\n        def _(): pass\n        def _(): pass\n        ')

    def test_redefinedUnderscoreImportation(self):
        """
        Test that shadowing an underscore importation raises a warning.
        """
        self.flakes('\n        from .i18n import _\n        def _(): pass\n        ', m.RedefinedWhileUnused)

    def test_redefinedClassFunction(self):
        """
        Test that shadowing a function definition in a class suite with another
        one raises a warning.
        """
        self.flakes('\n        class A:\n            def a(): pass\n            def a(): pass\n        ', m.RedefinedWhileUnused)

    def test_redefinedIfElseFunction(self):
        """
        Test that shadowing a function definition twice in an if
        and else block does not raise a warning.
        """
        self.flakes('\n        if True:\n            def a(): pass\n        else:\n            def a(): pass\n        ')

    def test_redefinedIfFunction(self):
        """
        Test that shadowing a function definition within an if block
        raises a warning.
        """
        self.flakes('\n        if True:\n            def a(): pass\n            def a(): pass\n        ', m.RedefinedWhileUnused)

    def test_redefinedTryExceptFunction(self):
        """
        Test that shadowing a function definition twice in try
        and except block does not raise a warning.
        """
        self.flakes('\n        try:\n            def a(): pass\n        except:\n            def a(): pass\n        ')

    def test_redefinedTryFunction(self):
        """
        Test that shadowing a function definition within a try block
        raises a warning.
        """
        self.flakes('\n        try:\n            def a(): pass\n            def a(): pass\n        except:\n            pass\n        ', m.RedefinedWhileUnused)

    def test_redefinedIfElseInListComp(self):
        """
        Test that shadowing a variable in a list comprehension in
        an if and else block does not raise a warning.
        """
        self.flakes("\n        if False:\n            a = 1\n        else:\n            [a for a in '12']\n        ")

    @skipIf(version_info >= (3, ), 'in Python 3 list comprehensions execute in a separate scope')
    def test_redefinedElseInListComp(self):
        """
        Test that shadowing a variable in a list comprehension in
        an else (or if) block raises a warning.
        """
        self.flakes("\n        if False:\n            pass\n        else:\n            a = 1\n            [a for a in '12']\n        ", m.RedefinedInListComp)

    def test_functionDecorator(self):
        """
        Test that shadowing a function definition with a decorated version of
        that function does not raise a warning.
        """
        self.flakes('\n        from somewhere import somedecorator\n\n        def a(): pass\n        a = somedecorator(a)\n        ')

    def test_classFunctionDecorator(self):
        """
        Test that shadowing a function definition in a class suite with a
        decorated version of that function does not raise a warning.
        """
        self.flakes('\n        class A:\n            def a(): pass\n            a = classmethod(a)\n        ')

    def test_modernProperty(self):
        self.flakes('\n        class A:\n            @property\n            def t(self):\n                pass\n            @t.setter\n            def t(self, value):\n                pass\n            @t.deleter\n            def t(self):\n                pass\n        ')

    def test_unaryPlus(self):
        """Don't die on unary +."""
        self.flakes('+1')

    def test_undefinedBaseClass(self):
        """
        If a name in the base list of a class definition is undefined, a
        warning is emitted.
        """
        self.flakes('\n        class foo(foo):\n            pass\n        ', m.UndefinedName)

    def test_classNameUndefinedInClassBody(self):
        """
        If a class name is used in the body of that class's definition and
        the name is not already defined, a warning is emitted.
        """
        self.flakes('\n        class foo:\n            foo\n        ', m.UndefinedName)

    def test_classNameDefinedPreviously(self):
        """
        If a class name is used in the body of that class's definition and
        the name was previously defined in some other way, no warning is
        emitted.
        """
        self.flakes('\n        foo = None\n        class foo:\n            foo\n        ')

    def test_classRedefinition(self):
        """
        If a class is defined twice in the same module, a warning is emitted.
        """
        self.flakes('\n        class Foo:\n            pass\n        class Foo:\n            pass\n        ', m.RedefinedWhileUnused)

    def test_functionRedefinedAsClass(self):
        """
        If a function is redefined as a class, a warning is emitted.
        """
        self.flakes('\n        def Foo():\n            pass\n        class Foo:\n            pass\n        ', m.RedefinedWhileUnused)

    def test_classRedefinedAsFunction(self):
        """
        If a class is redefined as a function, a warning is emitted.
        """
        self.flakes('\n        class Foo:\n            pass\n        def Foo():\n            pass\n        ', m.RedefinedWhileUnused)

    def test_classWithReturn(self):
        """
        If a return is used inside a class, a warning is emitted.
        """
        self.flakes('\n        class Foo(object):\n            return\n        ', m.ReturnOutsideFunction)

    def test_moduleWithReturn(self):
        """
        If a return is used at the module level, a warning is emitted.
        """
        self.flakes('\n        return\n        ', m.ReturnOutsideFunction)

    def test_classWithYield(self):
        """
        If a yield is used inside a class, a warning is emitted.
        """
        self.flakes('\n        class Foo(object):\n            yield\n        ', m.YieldOutsideFunction)

    def test_moduleWithYield(self):
        """
        If a yield is used at the module level, a warning is emitted.
        """
        self.flakes('\n        yield\n        ', m.YieldOutsideFunction)

    @skipIf(version_info < (3, 3), 'Python >= 3.3 only')
    def test_classWithYieldFrom(self):
        """
        If a yield from is used inside a class, a warning is emitted.
        """
        self.flakes('\n        class Foo(object):\n            yield from range(10)\n        ', m.YieldOutsideFunction)

    @skipIf(version_info < (3, 3), 'Python >= 3.3 only')
    def test_moduleWithYieldFrom(self):
        """
        If a yield from is used at the module level, a warning is emitted.
        """
        self.flakes('\n        yield from range(10)\n        ', m.YieldOutsideFunction)

    def test_continueOutsideLoop(self):
        self.flakes('\n        continue\n        ', m.ContinueOutsideLoop)
        self.flakes('\n        def f():\n            continue\n        ', m.ContinueOutsideLoop)
        self.flakes('\n        while True:\n            pass\n        else:\n            continue\n        ', m.ContinueOutsideLoop)
        self.flakes('\n        while True:\n            pass\n        else:\n            if 1:\n                if 2:\n                    continue\n        ', m.ContinueOutsideLoop)
        self.flakes('\n        while True:\n            def f():\n                continue\n        ', m.ContinueOutsideLoop)
        self.flakes('\n        while True:\n            class A:\n                continue\n        ', m.ContinueOutsideLoop)

    def test_continueInsideLoop(self):
        self.flakes('\n        while True:\n            continue\n        ')
        self.flakes('\n        for i in range(10):\n            continue\n        ')
        self.flakes('\n        while True:\n            if 1:\n                continue\n        ')
        self.flakes('\n        for i in range(10):\n            if 1:\n                continue\n        ')
        self.flakes('\n        while True:\n            while True:\n                pass\n            else:\n                continue\n        else:\n            pass\n        ')
        self.flakes('\n        while True:\n            try:\n                pass\n            finally:\n                while True:\n                    continue\n        ')

    def test_continueInFinally(self):
        self.flakes('\n        while True:\n            try:\n                pass\n            finally:\n                continue\n        ', m.ContinueInFinally)
        self.flakes('\n        while True:\n            try:\n                pass\n            finally:\n                if 1:\n                    if 2:\n                        continue\n        ', m.ContinueInFinally)
        self.flakes('\n        try:\n            pass\n        finally:\n            continue\n        ', m.ContinueInFinally)

    def test_breakOutsideLoop(self):
        self.flakes('\n        break\n        ', m.BreakOutsideLoop)
        self.flakes('\n        def f():\n            break\n        ', m.BreakOutsideLoop)
        self.flakes('\n        while True:\n            pass\n        else:\n            break\n        ', m.BreakOutsideLoop)
        self.flakes('\n        while True:\n            pass\n        else:\n            if 1:\n                if 2:\n                    break\n        ', m.BreakOutsideLoop)
        self.flakes('\n        while True:\n            def f():\n                break\n        ', m.BreakOutsideLoop)
        self.flakes('\n        while True:\n            class A:\n                break\n        ', m.BreakOutsideLoop)
        self.flakes('\n        try:\n            pass\n        finally:\n            break\n        ', m.BreakOutsideLoop)

    def test_breakInsideLoop(self):
        self.flakes('\n        while True:\n            break\n        ')
        self.flakes('\n        for i in range(10):\n            break\n        ')
        self.flakes('\n        while True:\n            if 1:\n                break\n        ')
        self.flakes('\n        for i in range(10):\n            if 1:\n                break\n        ')
        self.flakes('\n        while True:\n            while True:\n                pass\n            else:\n                break\n        else:\n            pass\n        ')
        self.flakes('\n        while True:\n            try:\n                pass\n            finally:\n                while True:\n                    break\n        ')
        self.flakes('\n        while True:\n            try:\n                pass\n            finally:\n                break\n        ')
        self.flakes('\n        while True:\n            try:\n                pass\n            finally:\n                if 1:\n                    if 2:\n                        break\n        ')

    def test_defaultExceptLast(self):
        """
        A default except block should be last.

        YES:

        try:
            ...
        except Exception:
            ...
        except:
            ...

        NO:

        try:
            ...
        except:
            ...
        except Exception:
            ...
        """
        self.flakes('\n        try:\n            pass\n        except ValueError:\n            pass\n        ')
        self.flakes('\n        try:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        ')
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        ')
        self.flakes('\n        try:\n            pass\n        except ValueError:\n            pass\n        else:\n            pass\n        ')
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        else:\n            pass\n        ')
        self.flakes('\n        try:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        else:\n            pass\n        ')

    def test_defaultExceptNotLast(self):
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        ', m.DefaultExceptNotLast, m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        else:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except:\n            pass\n        else:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        else:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        else:\n            pass\n        ', m.DefaultExceptNotLast, m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast, m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        else:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except:\n            pass\n        else:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        else:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast)
        self.flakes('\n        try:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        except:\n            pass\n        except ValueError:\n            pass\n        else:\n            pass\n        finally:\n            pass\n        ', m.DefaultExceptNotLast, m.DefaultExceptNotLast)

    @skipIf(version_info < (3, ), 'Python 3 only')
    def test_starredAssignmentNoError(self):
        """
        Python 3 extended iterable unpacking
        """
        self.flakes('\n        a, *b = range(10)\n        ')
        self.flakes('\n        *a, b = range(10)\n        ')
        self.flakes('\n        a, *b, c = range(10)\n        ')
        self.flakes('\n        (a, *b) = range(10)\n        ')
        self.flakes('\n        (*a, b) = range(10)\n        ')
        self.flakes('\n        (a, *b, c) = range(10)\n        ')
        self.flakes('\n        [a, *b] = range(10)\n        ')
        self.flakes('\n        [*a, b] = range(10)\n        ')
        self.flakes('\n        [a, *b, c] = range(10)\n        ')
        s = ', '.join('a%d' % i for i in range(128)) + ', *rest = range(1<<8)'
        self.flakes(s)
        s = '(' + ', '.join('a%d' % i for i in range(128)) + ', *rest) = range(1<<8)'
        self.flakes(s)
        s = '[' + ', '.join('a%d' % i for i in range(128)) + ', *rest] = range(1<<8)'
        self.flakes(s)

    @skipIf(version_info < (3, ), 'Python 3 only')
    def test_starredAssignmentErrors(self):
        """
        SyntaxErrors (not encoded in the ast) surrounding Python 3 extended
        iterable unpacking
        """
        s = ', '.join('a%d' % i for i in range(256)) + ', *rest = range(1<<8 + 1)'
        self.flakes(s, m.TooManyExpressionsInStarredAssignment)
        s = '(' + ', '.join('a%d' % i for i in range(256)) + ', *rest) = range(1<<8 + 1)'
        self.flakes(s, m.TooManyExpressionsInStarredAssignment)
        s = '[' + ', '.join('a%d' % i for i in range(256)) + ', *rest] = range(1<<8 + 1)'
        self.flakes(s, m.TooManyExpressionsInStarredAssignment)
        s = ', '.join('a%d' % i for i in range(512)) + ', *rest = range(1<<8 + 2)'
        self.flakes(s, m.TooManyExpressionsInStarredAssignment)
        s = '(' + ', '.join('a%d' % i for i in range(512)) + ', *rest) = range(1<<8 + 2)'
        self.flakes(s, m.TooManyExpressionsInStarredAssignment)
        s = '[' + ', '.join('a%d' % i for i in range(512)) + ', *rest] = range(1<<8 + 2)'
        self.flakes(s, m.TooManyExpressionsInStarredAssignment)
        self.flakes('\n        a, *b, *c = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        a, *b, c, *d = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        *a, *b, *c = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        (a, *b, *c) = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        (a, *b, c, *d) = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        (*a, *b, *c) = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        [a, *b, *c] = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        [a, *b, c, *d] = range(10)\n        ', m.TwoStarredExpressions)
        self.flakes('\n        [*a, *b, *c] = range(10)\n        ', m.TwoStarredExpressions)

    @skip('todo: Too hard to make this warn but other cases stay silent')
    def test_doubleAssignment(self):
        """
        If a variable is re-assigned to without being used, no warning is
        emitted.
        """
        self.flakes('\n        x = 10\n        x = 20\n        ', m.RedefinedWhileUnused)

    def test_doubleAssignmentConditionally(self):
        """
        If a variable is re-assigned within a conditional, no warning is
        emitted.
        """
        self.flakes('\n        x = 10\n        if True:\n            x = 20\n        ')

    def test_doubleAssignmentWithUse(self):
        """
        If a variable is re-assigned to after being used, no warning is
        emitted.
        """
        self.flakes('\n        x = 10\n        y = x * 2\n        x = 20\n        ')

    def test_comparison(self):
        """
        If a defined name is used on either side of any of the six comparison
        operators, no warning is emitted.
        """
        self.flakes('\n        x = 10\n        y = 20\n        x < y\n        x <= y\n        x == y\n        x != y\n        x >= y\n        x > y\n        ')

    def test_identity(self):
        """
        If a defined name is used on either side of an identity test, no
        warning is emitted.
        """
        self.flakes('\n        x = 10\n        y = 20\n        x is y\n        x is not y\n        ')

    def test_containment(self):
        """
        If a defined name is used on either side of a containment test, no
        warning is emitted.
        """
        self.flakes('\n        x = 10\n        y = 20\n        x in y\n        x not in y\n        ')

    def test_loopControl(self):
        """
        break and continue statements are supported.
        """
        self.flakes('\n        for x in [1, 2]:\n            break\n        ')
        self.flakes('\n        for x in [1, 2]:\n            continue\n        ')

    def test_ellipsis(self):
        """
        Ellipsis in a slice is supported.
        """
        self.flakes('\n        [1, 2][...]\n        ')

    def test_extendedSlice(self):
        """
        Extended slices are supported.
        """
        self.flakes('\n        x = 3\n        [1, 2][x,:]\n        ')

    def test_varAugmentedAssignment(self):
        """
        Augmented assignment of a variable is supported.
        We don't care about var refs.
        """
        self.flakes('\n        foo = 0\n        foo += 1\n        ')

    def test_attrAugmentedAssignment(self):
        """
        Augmented assignment of attributes is supported.
        We don't care about attr refs.
        """
        self.flakes('\n        foo = None\n        foo.bar += foo.baz\n        ')

    def test_globalDeclaredInDifferentScope(self):
        """
        A 'global' can be declared in one scope and reused in another.
        """
        self.flakes("\n        def f(): global foo\n        def g(): foo = 'anything'; foo.is_used()\n        ")

    def test_function_arguments(self):
        """
        Test to traverse ARG and ARGUMENT handler
        """
        self.flakes('\n        def foo(a, b):\n            pass\n        ')
        self.flakes('\n        def foo(a, b, c=0):\n            pass\n        ')
        self.flakes('\n        def foo(a, b, c=0, *args):\n            pass\n        ')
        self.flakes('\n        def foo(a, b, c=0, *args, **kwargs):\n            pass\n        ')

    @skipIf(version_info < (3, 3), 'Python >= 3.3 only')
    def test_function_arguments_python3(self):
        self.flakes('\n        def foo(a, b, c=0, *args, d=0, **kwargs):\n            pass\n        ')


class TestUnusedAssignment(TestCase):
    __doc__ = '\n    Tests for warning about unused assignments.\n    '

    def test_unusedVariable(self):
        """
        Warn when a variable in a function is assigned a value that's never
        used.
        """
        self.flakes('\n        def a():\n            b = 1\n        ', m.UnusedVariable)

    def test_unusedUnderscoreVariable(self):
        """
        Don't warn when the magic "_" (underscore) variable is unused.
        See issue #202.
        """
        self.flakes('\n        def a(unused_param):\n            _ = unused_param\n        ')

    def test_unusedVariableAsLocals(self):
        """
        Using locals() it is perfectly valid to have unused variables
        """
        self.flakes('\n        def a():\n            b = 1\n            return locals()\n        ')

    def test_unusedVariableNoLocals(self):
        """
        Using locals() in wrong scope should not matter
        """
        self.flakes('\n        def a():\n            locals()\n            def a():\n                b = 1\n                return\n        ', m.UnusedVariable)

    @skip("todo: Difficult because it doesn't apply in the context of a loop")
    def test_unusedReassignedVariable(self):
        """
        Shadowing a used variable can still raise an UnusedVariable warning.
        """
        self.flakes('\n        def a():\n            b = 1\n            b.foo()\n            b = 2\n        ', m.UnusedVariable)

    def test_variableUsedInLoop(self):
        """
        Shadowing a used variable cannot raise an UnusedVariable warning in the
        context of a loop.
        """
        self.flakes('\n        def a():\n            b = True\n            while b:\n                b = False\n        ')

    def test_assignToGlobal(self):
        """
        Assigning to a global and then not using that global is perfectly
        acceptable. Do not mistake it for an unused local variable.
        """
        self.flakes('\n        b = 0\n        def a():\n            global b\n            b = 1\n        ')

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_assignToNonlocal(self):
        """
        Assigning to a nonlocal and then not using that binding is perfectly
        acceptable. Do not mistake it for an unused local variable.
        """
        self.flakes("\n        b = b'0'\n        def a():\n            nonlocal b\n            b = b'1'\n        ")

    def test_assignToMember(self):
        """
        Assigning to a member of another object and then not using that member
        variable is perfectly acceptable. Do not mistake it for an unused
        local variable.
        """
        self.flakes('\n        class b:\n            pass\n        def a():\n            b.foo = 1\n        ')

    def test_assignInForLoop(self):
        """
        Don't warn when a variable in a for loop is assigned to but not used.
        """
        self.flakes('\n        def f():\n            for i in range(10):\n                pass\n        ')

    def test_assignInListComprehension(self):
        """
        Don't warn when a variable in a list comprehension is
        assigned to but not used.
        """
        self.flakes('\n        def f():\n            [None for i in range(10)]\n        ')

    def test_generatorExpression(self):
        """
        Don't warn when a variable in a generator expression is
        assigned to but not used.
        """
        self.flakes('\n        def f():\n            (None for i in range(10))\n        ')

    def test_assignmentInsideLoop(self):
        """
        Don't warn when a variable assignment occurs lexically after its use.
        """
        self.flakes('\n        def f():\n            x = None\n            for i in range(10):\n                if i > 2:\n                    return x\n                x = i * 2\n        ')

    def test_tupleUnpacking(self):
        """
        Don't warn when a variable included in tuple unpacking is unused. It's
        very common for variables in a tuple unpacking assignment to be unused
        in good Python code, so warning will only create false positives.
        """
        self.flakes('\n        def f(tup):\n            (x, y) = tup\n        ')
        self.flakes('\n        def f():\n            (x, y) = 1, 2\n        ', m.UnusedVariable, m.UnusedVariable)
        self.flakes('\n        def f():\n            (x, y) = coords = 1, 2\n            if x > 1:\n                print(coords)\n        ')
        self.flakes('\n        def f():\n            (x, y) = coords = 1, 2\n        ', m.UnusedVariable)
        self.flakes('\n        def f():\n            coords = (x, y) = 1, 2\n        ', m.UnusedVariable)

    def test_listUnpacking(self):
        """
        Don't warn when a variable included in list unpacking is unused.
        """
        self.flakes('\n        def f(tup):\n            [x, y] = tup\n        ')
        self.flakes('\n        def f():\n            [x, y] = [1, 2]\n        ', m.UnusedVariable, m.UnusedVariable)

    def test_closedOver(self):
        """
        Don't warn when the assignment is used in an inner function.
        """
        self.flakes('\n        def barMaker():\n            foo = 5\n            def bar():\n                return foo\n            return bar\n        ')

    def test_doubleClosedOver(self):
        """
        Don't warn when the assignment is used in an inner function, even if
        that inner function itself is in an inner function.
        """
        self.flakes('\n        def barMaker():\n            foo = 5\n            def bar():\n                def baz():\n                    return foo\n            return bar\n        ')

    def test_tracebackhideSpecialVariable(self):
        """
        Do not warn about unused local variable __tracebackhide__, which is
        a special variable for py.test.
        """
        self.flakes('\n            def helper():\n                __tracebackhide__ = True\n        ')

    def test_ifexp(self):
        """
        Test C{foo if bar else baz} statements.
        """
        self.flakes("a = 'moo' if True else 'oink'")
        self.flakes("a = foo if True else 'oink'", m.UndefinedName)
        self.flakes("a = 'moo' if True else bar", m.UndefinedName)

    def test_withStatementNoNames(self):
        """
        No warnings are emitted for using inside or after a nameless C{with}
        statement a name defined beforehand.
        """
        self.flakes('\n        from __future__ import with_statement\n        bar = None\n        with open("foo"):\n            bar\n        bar\n        ')

    def test_withStatementSingleName(self):
        """
        No warnings are emitted for using a name defined by a C{with} statement
        within the suite or afterwards.
        """
        self.flakes("\n        from __future__ import with_statement\n        with open('foo') as bar:\n            bar\n        bar\n        ")

    def test_withStatementAttributeName(self):
        """
        No warnings are emitted for using an attribute as the target of a
        C{with} statement.
        """
        self.flakes("\n        from __future__ import with_statement\n        import foo\n        with open('foo') as foo.bar:\n            pass\n        ")

    def test_withStatementSubscript(self):
        """
        No warnings are emitted for using a subscript as the target of a
        C{with} statement.
        """
        self.flakes("\n        from __future__ import with_statement\n        import foo\n        with open('foo') as foo[0]:\n            pass\n        ")

    def test_withStatementSubscriptUndefined(self):
        """
        An undefined name warning is emitted if the subscript used as the
        target of a C{with} statement is not defined.
        """
        self.flakes("\n        from __future__ import with_statement\n        import foo\n        with open('foo') as foo[bar]:\n            pass\n        ", m.UndefinedName)

    def test_withStatementTupleNames(self):
        """
        No warnings are emitted for using any of the tuple of names defined by
        a C{with} statement within the suite or afterwards.
        """
        self.flakes("\n        from __future__ import with_statement\n        with open('foo') as (bar, baz):\n            bar, baz\n        bar, baz\n        ")

    def test_withStatementListNames(self):
        """
        No warnings are emitted for using any of the list of names defined by a
        C{with} statement within the suite or afterwards.
        """
        self.flakes("\n        from __future__ import with_statement\n        with open('foo') as [bar, baz]:\n            bar, baz\n        bar, baz\n        ")

    def test_withStatementComplicatedTarget(self):
        """
        If the target of a C{with} statement uses any or all of the valid forms
        for that part of the grammar (See
        U{http://docs.python.org/reference/compound_stmts.html#the-with-statement}),
        the names involved are checked both for definedness and any bindings
        created are respected in the suite of the statement and afterwards.
        """
        self.flakes("\n        from __future__ import with_statement\n        c = d = e = g = h = i = None\n        with open('foo') as [(a, b), c[d], e.f, g[h:i]]:\n            a, b, c, d, e, g, h, i\n        a, b, c, d, e, g, h, i\n        ")

    def test_withStatementSingleNameUndefined(self):
        """
        An undefined name warning is emitted if the name first defined by a
        C{with} statement is used before the C{with} statement.
        """
        self.flakes("\n        from __future__ import with_statement\n        bar\n        with open('foo') as bar:\n            pass\n        ", m.UndefinedName)

    def test_withStatementTupleNamesUndefined(self):
        """
        An undefined name warning is emitted if a name first defined by the
        tuple-unpacking form of the C{with} statement is used before the
        C{with} statement.
        """
        self.flakes("\n        from __future__ import with_statement\n        baz\n        with open('foo') as (bar, baz):\n            pass\n        ", m.UndefinedName)

    def test_withStatementSingleNameRedefined(self):
        """
        A redefined name warning is emitted if a name bound by an import is
        rebound by the name defined by a C{with} statement.
        """
        self.flakes("\n        from __future__ import with_statement\n        import bar\n        with open('foo') as bar:\n            pass\n        ", m.RedefinedWhileUnused)

    def test_withStatementTupleNamesRedefined(self):
        """
        A redefined name warning is emitted if a name bound by an import is
        rebound by one of the names defined by the tuple-unpacking form of a
        C{with} statement.
        """
        self.flakes("\n        from __future__ import with_statement\n        import bar\n        with open('foo') as (bar, baz):\n            pass\n        ", m.RedefinedWhileUnused)

    def test_withStatementUndefinedInside(self):
        """
        An undefined name warning is emitted if a name is used inside the
        body of a C{with} statement without first being bound.
        """
        self.flakes("\n        from __future__ import with_statement\n        with open('foo') as bar:\n            baz\n        ", m.UndefinedName)

    def test_withStatementNameDefinedInBody(self):
        """
        A name defined in the body of a C{with} statement can be used after
        the body ends without warning.
        """
        self.flakes("\n        from __future__ import with_statement\n        with open('foo') as bar:\n            baz = 10\n        baz\n        ")

    def test_withStatementUndefinedInExpression(self):
        """
        An undefined name warning is emitted if a name in the I{test}
        expression of a C{with} statement is undefined.
        """
        self.flakes('\n        from __future__ import with_statement\n        with bar as baz:\n            pass\n        ', m.UndefinedName)
        self.flakes('\n        from __future__ import with_statement\n        with bar as bar:\n            pass\n        ', m.UndefinedName)

    def test_dictComprehension(self):
        """
        Dict comprehensions are properly handled.
        """
        self.flakes('\n        a = {1: x for x in range(10)}\n        ')

    def test_setComprehensionAndLiteral(self):
        """
        Set comprehensions are properly handled.
        """
        self.flakes('\n        a = {1, 2, 3}\n        b = {x for x in range(10)}\n        ')

    def test_exceptionUsedInExcept(self):
        self.flakes('\n        try: pass\n        except Exception as e: e\n        ')
        self.flakes('\n        def download_review():\n            try: pass\n            except Exception as e: e\n        ')

    @skipIf(version_info < (3, ), 'In Python 2 exception names stay bound after the exception handler')
    def test_exceptionUnusedInExcept(self):
        self.flakes('\n        try: pass\n        except Exception as e: pass\n        ', m.UnusedVariable)

    def test_exceptionUnusedInExceptInFunction(self):
        self.flakes('\n        def download_review():\n            try: pass\n            except Exception as e: pass\n        ', m.UnusedVariable)

    def test_exceptWithoutNameInFunction(self):
        """
        Don't issue false warning when an unnamed exception is used.
        Previously, there would be a false warning, but only when the
        try..except was in a function
        """
        self.flakes('\n        import tokenize\n        def foo():\n            try: pass\n            except tokenize.TokenError: pass\n        ')

    def test_exceptWithoutNameInFunctionTuple(self):
        """
        Don't issue false warning when an unnamed exception is used.
        This example catches a tuple of exception types.
        """
        self.flakes('\n        import tokenize\n        def foo():\n            try: pass\n            except (tokenize.TokenError, IndentationError): pass\n        ')

    def test_augmentedAssignmentImportedFunctionCall(self):
        """
        Consider a function that is called on the right part of an
        augassign operation to be used.
        """
        self.flakes('\n        from foo import bar\n        baz = 0\n        baz += bar()\n        ')

    def test_assert_without_message(self):
        """An assert without a message is not an error."""
        self.flakes('\n        a = 1\n        assert a\n        ')

    def test_assert_with_message(self):
        """An assert with a message is not an error."""
        self.flakes("\n        a = 1\n        assert a, 'x'\n        ")

    def test_assert_tuple(self):
        """An assert of a non-empty tuple is always True."""
        self.flakes("\n        assert (False, 'x')\n        assert (False, )\n        ", m.AssertTuple, m.AssertTuple)

    def test_assert_tuple_empty(self):
        """An assert of an empty tuple is always False."""
        self.flakes('\n        assert ()\n        ')

    def test_assert_static(self):
        """An assert of a static value is not an error."""
        self.flakes('\n        assert True\n        assert 1\n        ')

    @skipIf(version_info < (3, 3), 'new in Python 3.3')
    def test_yieldFromUndefined(self):
        """
        Test C{yield from} statement
        """
        self.flakes('\n        def bar():\n            yield from foo()\n        ', m.UndefinedName)

    @skipIf(version_info < (3, 6), 'new in Python 3.6')
    def test_f_string(self):
        """Test PEP 498 f-strings are treated as a usage."""
        self.flakes("\n        baz = 0\n        print(f'{4*baz}')\n        ")


class TestAsyncStatements(TestCase):

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_asyncDef(self):
        self.flakes('\n        async def bar():\n            return 42\n        ')

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_asyncDefAwait(self):
        self.flakes("\n        async def read_data(db):\n            await db.fetch('SELECT ...')\n        ")

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_asyncDefUndefined(self):
        self.flakes('\n        async def bar():\n            return foo()\n        ', m.UndefinedName)

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_asyncFor(self):
        self.flakes('\n        async def read_data(db):\n            output = []\n            async for row in db.cursor():\n                output.append(row)\n            return output\n        ')

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_asyncForUnderscoreLoopVar(self):
        self.flakes('\n        async def coro(it):\n            async for _ in it:\n                pass\n        ')

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_loopControlInAsyncFor(self):
        self.flakes("\n        async def read_data(db):\n            output = []\n            async for row in db.cursor():\n                if row[0] == 'skip':\n                    continue\n                output.append(row)\n            return output\n        ")
        self.flakes("\n        async def read_data(db):\n            output = []\n            async for row in db.cursor():\n                if row[0] == 'stop':\n                    break\n                output.append(row)\n            return output\n        ")

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_loopControlInAsyncForElse(self):
        self.flakes('\n        async def read_data(db):\n            output = []\n            async for row in db.cursor():\n                output.append(row)\n            else:\n                continue\n            return output\n        ', m.ContinueOutsideLoop)
        self.flakes('\n        async def read_data(db):\n            output = []\n            async for row in db.cursor():\n                output.append(row)\n            else:\n                break\n            return output\n        ', m.BreakOutsideLoop)

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_continueInAsyncForFinally(self):
        self.flakes('\n        async def read_data(db):\n            output = []\n            async for row in db.cursor():\n                try:\n                    output.append(row)\n                finally:\n                    continue\n            return output\n        ', m.ContinueInFinally)

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_asyncWith(self):
        self.flakes('\n        async def commit(session, data):\n            async with session.transaction():\n                await session.update(data)\n        ')

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_asyncWithItem(self):
        self.flakes('\n        async def commit(session, data):\n            async with session.transaction() as trans:\n                await trans.begin()\n                ...\n                await trans.end()\n        ')

    @skipIf(version_info < (3, 5), 'new in Python 3.5')
    def test_matmul(self):
        self.flakes('\n        def foo(a, b):\n            return a @ b\n        ')

    @skipIf(version_info < (3, 6), 'new in Python 3.6')
    def test_formatstring(self):
        self.flakes("\n        hi = 'hi'\n        mom = 'mom'\n        f'{hi} {mom}'\n        ")

    def test_raise_notimplemented(self):
        self.flakes('\n        raise NotImplementedError("This is fine")\n        ')
        self.flakes('\n        raise NotImplementedError\n        ')
        self.flakes('\n        raise NotImplemented("This isn\'t gonna work")\n        ', m.RaiseNotImplemented)
        self.flakes('\n        raise NotImplemented\n        ', m.RaiseNotImplemented)


class TestIncompatiblePrintOperator(TestCase):
    __doc__ = '\n    Tests for warning about invalid use of print function.\n    '

    def test_valid_print(self):
        self.flakes('\n        print("Hello")\n        ')

    def test_invalid_print_when_imported_from_future(self):
        exc = self.flakes('\n        from __future__ import print_function\n        import sys\n        print >>sys.stderr, "Hello"\n        ', m.InvalidPrintSyntax).messages[0]
        self.assertEqual(exc.lineno, 4)
        self.assertEqual(exc.col, 0)

    def test_print_function_assignment(self):
        """
        A valid assignment, tested for catching false positives.
        """
        self.flakes('\n        from __future__ import print_function\n        log = print\n        log("Hello")\n        ')

    def test_print_in_lambda(self):
        self.flakes('\n        from __future__ import print_function\n        a = lambda: print\n        ')

    def test_print_returned_in_function(self):
        self.flakes('\n        from __future__ import print_function\n        def a():\n            return print\n        ')

    def test_print_as_condition_test(self):
        self.flakes('\n        from __future__ import print_function\n        if print: pass\n        ')