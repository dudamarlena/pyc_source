# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_undefined_names.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 25291 bytes
import ast
from sys import version_info
from pyflakes import messages as m, checker
from pyflakes.test.harness import TestCase, skipIf, skip

class Test(TestCase):

    def test_undefined(self):
        self.flakes('bar', m.UndefinedName)

    def test_definedInListComp(self):
        self.flakes('[a for a in range(10) if a]')

    @skipIf(version_info < (3, ), 'in Python 2 list comprehensions execute in the same scope')
    def test_undefinedInListComp(self):
        self.flakes('\n        [a for a in range(10)]\n        a\n        ', m.UndefinedName)

    @skipIf(version_info < (3, ), 'in Python 2 exception names stay bound after the except: block')
    def test_undefinedExceptionName(self):
        """Exception names can't be used after the except: block.

        The exc variable is unused inside the exception handler."""
        self.flakes("\n        try:\n            raise ValueError('ve')\n        except ValueError as exc:\n            pass\n        exc\n        ", m.UndefinedName, m.UnusedVariable)

    def test_namesDeclaredInExceptBlocks(self):
        """Locals declared in except: blocks can be used after the block.

        This shows the example in test_undefinedExceptionName is
        different."""
        self.flakes("\n        try:\n            raise ValueError('ve')\n        except ValueError as exc:\n            e = exc\n        e\n        ")

    @skip('error reporting disabled due to false positives below')
    def test_undefinedExceptionNameObscuringLocalVariable(self):
        """Exception names obscure locals, can't be used after.

        Last line will raise UnboundLocalError on Python 3 after exiting
        the except: block. Note next two examples for false positives to
        watch out for."""
        self.flakes("\n        exc = 'Original value'\n        try:\n            raise ValueError('ve')\n        except ValueError as exc:\n            pass\n        exc\n        ", m.UndefinedName)

    @skipIf(version_info < (3, ), 'in Python 2 exception names stay bound after the except: block')
    def test_undefinedExceptionNameObscuringLocalVariable2(self):
        """Exception names are unbound after the `except:` block.

        Last line will raise UnboundLocalError on Python 3 but would print out
        've' on Python 2. The exc variable is unused inside the exception
        handler."""
        self.flakes("\n        try:\n            raise ValueError('ve')\n        except ValueError as exc:\n            pass\n        print(exc)\n        exc = 'Original value'\n        ", m.UndefinedName, m.UnusedVariable)

    def test_undefinedExceptionNameObscuringLocalVariableFalsePositive1(self):
        """Exception names obscure locals, can't be used after. Unless.

        Last line will never raise UnboundLocalError because it's only
        entered if no exception was raised."""
        expected = [] if version_info < (3, ) else [m.UnusedVariable]
        (self.flakes)(*("\n        exc = 'Original value'\n        try:\n            raise ValueError('ve')\n        except ValueError as exc:\n            print('exception logged')\n            raise\n        exc\n        ", ), *expected)

    def test_delExceptionInExcept(self):
        """The exception name can be deleted in the except: block."""
        self.flakes('\n        try:\n            pass\n        except Exception as exc:\n            del exc\n        ')

    def test_undefinedExceptionNameObscuringLocalVariableFalsePositive2(self):
        """Exception names obscure locals, can't be used after. Unless.

        Last line will never raise UnboundLocalError because `error` is
        only falsy if the `except:` block has not been entered."""
        expected = [] if version_info < (3, ) else [m.UnusedVariable]
        (self.flakes)(*("\n        exc = 'Original value'\n        error = None\n        try:\n            raise ValueError('ve')\n        except ValueError as exc:\n            error = 'exception logged'\n        if error:\n            print(error)\n        else:\n            exc\n        ", ), *expected)

    @skip('error reporting disabled due to false positives below')
    def test_undefinedExceptionNameObscuringGlobalVariable(self):
        """Exception names obscure globals, can't be used after.

        Last line will raise UnboundLocalError on both Python 2 and
        Python 3 because the existence of that exception name creates
        a local scope placeholder for it, obscuring any globals, etc."""
        self.flakes("\n        exc = 'Original value'\n        def func():\n            try:\n                pass  # nothing is raised\n            except ValueError as exc:\n                pass  # block never entered, exc stays unbound\n            exc\n        ", m.UndefinedLocal)

    @skip('error reporting disabled due to false positives below')
    def test_undefinedExceptionNameObscuringGlobalVariable2(self):
        """Exception names obscure globals, can't be used after.

        Last line will raise NameError on Python 3 because the name is
        locally unbound after the `except:` block, even if it's
        nonlocal. We should issue an error in this case because code
        only working correctly if an exception isn't raised, is invalid.
        Unless it's explicitly silenced, see false positives below."""
        self.flakes("\n        exc = 'Original value'\n        def func():\n            global exc\n            try:\n                raise ValueError('ve')\n            except ValueError as exc:\n                pass  # block never entered, exc stays unbound\n            exc\n        ", m.UndefinedLocal)

    def test_undefinedExceptionNameObscuringGlobalVariableFalsePositive1(self):
        """Exception names obscure globals, can't be used after. Unless.

        Last line will never raise NameError because it's only entered
        if no exception was raised."""
        expected = [] if version_info < (3, ) else [m.UnusedVariable]
        (self.flakes)(*("\n        exc = 'Original value'\n        def func():\n            global exc\n            try:\n                raise ValueError('ve')\n            except ValueError as exc:\n                print('exception logged')\n                raise\n            exc\n        ", ), *expected)

    def test_undefinedExceptionNameObscuringGlobalVariableFalsePositive2(self):
        """Exception names obscure globals, can't be used after. Unless.

        Last line will never raise NameError because `error` is only
        falsy if the `except:` block has not been entered."""
        expected = [] if version_info < (3, ) else [m.UnusedVariable]
        (self.flakes)(*("\n        exc = 'Original value'\n        def func():\n            global exc\n            error = None\n            try:\n                raise ValueError('ve')\n            except ValueError as exc:\n                error = 'exception logged'\n            if error:\n                print(error)\n            else:\n                exc\n        ", ), *expected)

    def test_functionsNeedGlobalScope(self):
        self.flakes('\n        class a:\n            def b():\n                fu\n        fu = 1\n        ')

    def test_builtins(self):
        self.flakes('range(10)')

    def test_builtinWindowsError(self):
        """
        C{WindowsError} is sometimes a builtin name, so no warning is emitted
        for using it.
        """
        self.flakes('WindowsError')

    @skipIf(version_info < (3, 6), 'new feature in 3.6')
    def test_moduleAnnotations(self):
        """
        Use of the C{__annotations__} in module scope should not emit
        an undefined name warning when version is greater than or equal to 3.6.
        """
        self.flakes('__annotations__')

    def test_magicGlobalsFile(self):
        """
        Use of the C{__file__} magic global should not emit an undefined name
        warning.
        """
        self.flakes('__file__')

    def test_magicGlobalsBuiltins(self):
        """
        Use of the C{__builtins__} magic global should not emit an undefined
        name warning.
        """
        self.flakes('__builtins__')

    def test_magicGlobalsName(self):
        """
        Use of the C{__name__} magic global should not emit an undefined name
        warning.
        """
        self.flakes('__name__')

    def test_magicGlobalsPath(self):
        """
        Use of the C{__path__} magic global should not emit an undefined name
        warning, if you refer to it from a file called __init__.py.
        """
        self.flakes('__path__', m.UndefinedName)
        self.flakes('__path__', filename='package/__init__.py')

    def test_magicModuleInClassScope(self):
        """
        Use of the C{__module__} magic builtin should not emit an undefined
        name warning if used in class scope.
        """
        self.flakes('__module__', m.UndefinedName)
        self.flakes('\n        class Foo:\n            __module__\n        ')
        self.flakes('\n        class Foo:\n            def bar(self):\n                __module__\n        ', m.UndefinedName)

    def test_globalImportStar(self):
        """Can't find undefined names with import *."""
        self.flakes('from fu import *; bar', m.ImportStarUsed, m.ImportStarUsage)

    @skipIf(version_info >= (3, ), 'obsolete syntax')
    def test_localImportStar(self):
        """
        A local import * still allows undefined names to be found
        in upper scopes.
        """
        self.flakes('\n        def a():\n            from fu import *\n        bar\n        ', m.ImportStarUsed, m.UndefinedName, m.UnusedImport)

    @skipIf(version_info >= (3, ), 'obsolete syntax')
    def test_unpackedParameter(self):
        """Unpacked function parameters create bindings."""
        self.flakes('\n        def a((bar, baz)):\n            bar; baz\n        ')

    def test_definedByGlobal(self):
        """
        "global" can make an otherwise undefined name in another function
        defined.
        """
        self.flakes('\n        def a(): global fu; fu = 1\n        def b(): fu\n        ')
        self.flakes('\n        def c(): bar\n        def b(): global bar; bar = 1\n        ')

    def test_definedByGlobalMultipleNames(self):
        """
        "global" can accept multiple names.
        """
        self.flakes('\n        def a(): global fu, bar; fu = 1; bar = 2\n        def b(): fu; bar\n        ')

    def test_globalInGlobalScope(self):
        """
        A global statement in the global scope is ignored.
        """
        self.flakes('\n        global x\n        def foo():\n            print(x)\n        ', m.UndefinedName)

    def test_global_reset_name_only(self):
        """A global statement does not prevent other names being undefined."""
        self.flakes('\n        def f1():\n            s\n\n        def f2():\n            global m\n        ', m.UndefinedName)

    @skip('todo')
    def test_unused_global(self):
        """An unused global statement does not define the name."""
        self.flakes('\n        def f1():\n            m\n\n        def f2():\n            global m\n        ', m.UndefinedName)

    def test_del(self):
        """Del deletes bindings."""
        self.flakes('a = 1; del a; a', m.UndefinedName)

    def test_delGlobal(self):
        """Del a global binding from a function."""
        self.flakes('\n        a = 1\n        def f():\n            global a\n            del a\n        a\n        ')

    def test_delUndefined(self):
        """Del an undefined name."""
        self.flakes('del a', m.UndefinedName)

    def test_delConditional(self):
        """
        Ignores conditional bindings deletion.
        """
        self.flakes('\n        context = None\n        test = True\n        if False:\n            del(test)\n        assert(test)\n        ')

    def test_delConditionalNested(self):
        """
        Ignored conditional bindings deletion even if they are nested in other
        blocks.
        """
        self.flakes('\n        context = None\n        test = True\n        if False:\n            with context():\n                del(test)\n        assert(test)\n        ')

    def test_delWhile(self):
        """
        Ignore bindings deletion if called inside the body of a while
        statement.
        """
        self.flakes("\n        def test():\n            foo = 'bar'\n            while False:\n                del foo\n            assert(foo)\n        ")

    def test_delWhileTestUsage(self):
        """
        Ignore bindings deletion if called inside the body of a while
        statement and name is used inside while's test part.
        """
        self.flakes('\n        def _worker():\n            o = True\n            while o is not True:\n                del o\n                o = False\n        ')

    def test_delWhileNested(self):
        """
        Ignore bindings deletions if node is part of while's test, even when
        del is in a nested block.
        """
        self.flakes('\n        context = None\n        def _worker():\n            o = True\n            while o is not True:\n                while True:\n                    with context():\n                        del o\n                o = False\n        ')

    def test_globalFromNestedScope(self):
        """Global names are available from nested scopes."""
        self.flakes('\n        a = 1\n        def b():\n            def c():\n                a\n        ')

    def test_laterRedefinedGlobalFromNestedScope(self):
        """
        Test that referencing a local name that shadows a global, before it is
        defined, generates a warning.
        """
        self.flakes('\n        a = 1\n        def fun():\n            a\n            a = 2\n            return a\n        ', m.UndefinedLocal)

    def test_laterRedefinedGlobalFromNestedScope2(self):
        """
        Test that referencing a local name in a nested scope that shadows a
        global declared in an enclosing scope, before it is defined, generates
        a warning.
        """
        self.flakes('\n            a = 1\n            def fun():\n                global a\n                def fun2():\n                    a\n                    a = 2\n                    return a\n        ', m.UndefinedLocal)

    def test_intermediateClassScopeIgnored(self):
        """
        If a name defined in an enclosing scope is shadowed by a local variable
        and the name is used locally before it is bound, an unbound local
        warning is emitted, even if there is a class scope between the enclosing
        scope and the local scope.
        """
        self.flakes('\n        def f():\n            x = 1\n            class g:\n                def h(self):\n                    a = x\n                    x = None\n                    print(x, a)\n            print(x)\n        ', m.UndefinedLocal)

    def test_doubleNestingReportsClosestName(self):
        """
        Test that referencing a local name in a nested scope that shadows a
        variable declared in two different outer scopes before it is defined
        in the innermost scope generates an UnboundLocal warning which
        refers to the nearest shadowed name.
        """
        exc = self.flakes('\n            def a():\n                x = 1\n                def b():\n                    x = 2 # line 5\n                    def c():\n                        x\n                        x = 3\n                        return x\n                    return x\n                return x\n        ', m.UndefinedLocal).messages[0]
        expected_line_num = 7 if self.withDoctest else 5
        self.assertEqual(exc.message_args, ('x', expected_line_num))

    def test_laterRedefinedGlobalFromNestedScope3(self):
        """
        Test that referencing a local name in a nested scope that shadows a
        global, before it is defined, generates a warning.
        """
        self.flakes('\n            def fun():\n                a = 1\n                def fun2():\n                    a\n                    a = 1\n                    return a\n                return a\n        ', m.UndefinedLocal)

    def test_undefinedAugmentedAssignment(self):
        self.flakes('\n            def f(seq):\n                a = 0\n                seq[a] += 1\n                seq[b] /= 2\n                c[0] *= 2\n                a -= 3\n                d += 4\n                e[any] = 5\n            ', m.UndefinedName, m.UndefinedName, m.UndefinedName, m.UnusedVariable, m.UndefinedName)

    def test_nestedClass(self):
        """Nested classes can access enclosing scope."""
        self.flakes('\n        def f(foo):\n            class C:\n                bar = foo\n                def f(self):\n                    return foo\n            return C()\n\n        f(123).f()\n        ')

    def test_badNestedClass(self):
        """Free variables in nested classes must bind at class creation."""
        self.flakes('\n        def f():\n            class C:\n                bar = foo\n            foo = 456\n            return foo\n        f()\n        ', m.UndefinedName)

    def test_definedAsStarArgs(self):
        """Star and double-star arg names are defined."""
        self.flakes('\n        def f(a, *b, **c):\n            print(a, b, c)\n        ')

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_definedAsStarUnpack(self):
        """Star names in unpack are defined."""
        self.flakes('\n        a, *b = range(10)\n        print(a, b)\n        ')
        self.flakes('\n        *a, b = range(10)\n        print(a, b)\n        ')
        self.flakes('\n        a, *b, c = range(10)\n        print(a, b, c)\n        ')

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_usedAsStarUnpack(self):
        """
        Star names in unpack are used if RHS is not a tuple/list literal.
        """
        self.flakes('\n        def f():\n            a, *b = range(10)\n        ')
        self.flakes('\n        def f():\n            (*a, b) = range(10)\n        ')
        self.flakes('\n        def f():\n            [a, *b, c] = range(10)\n        ')

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_unusedAsStarUnpack(self):
        """
        Star names in unpack are unused if RHS is a tuple/list literal.
        """
        self.flakes("\n        def f():\n            a, *b = any, all, 4, 2, 'un'\n        ", m.UnusedVariable, m.UnusedVariable)
        self.flakes('\n        def f():\n            (*a, b) = [bool, int, float, complex]\n        ', m.UnusedVariable, m.UnusedVariable)
        self.flakes('\n        def f():\n            [a, *b, c] = 9, 8, 7, 6, 5, 4\n        ', m.UnusedVariable, m.UnusedVariable, m.UnusedVariable)

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_keywordOnlyArgs(self):
        """Keyword-only arg names are defined."""
        self.flakes('\n        def f(*, a, b=None):\n            print(a, b)\n        ')
        self.flakes('\n        import default_b\n        def f(*, a, b=default_b):\n            print(a, b)\n        ')

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_keywordOnlyArgsUndefined(self):
        """Typo in kwonly name."""
        self.flakes('\n        def f(*, a, b=default_c):\n            print(a, b)\n        ', m.UndefinedName)

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_annotationUndefined(self):
        """Undefined annotations."""
        self.flakes('\n        from abc import note1, note2, note3, note4, note5\n        def func(a: note1, *args: note2,\n                 b: note3=12, **kw: note4) -> note5: pass\n        ')
        self.flakes('\n        def func():\n            d = e = 42\n            def func(a: {1, d}) -> (lambda c: e): pass\n        ')

    @skipIf(version_info < (3, ), 'new in Python 3')
    def test_metaClassUndefined(self):
        self.flakes('\n        from abc import ABCMeta\n        class A(metaclass=ABCMeta): pass\n        ')

    def test_definedInGenExp(self):
        """
        Using the loop variable of a generator expression results in no
        warnings.
        """
        self.flakes('(a for a in [1, 2, 3] if a)')
        self.flakes('(b for b in (a for a in [1, 2, 3] if a) if b)')

    def test_undefinedInGenExpNested(self):
        """
        The loop variables of generator expressions nested together are
        not defined in the other generator.
        """
        self.flakes('(b for b in (a for a in [1, 2, 3] if b) if b)', m.UndefinedName)
        self.flakes('(b for b in (a for a in [1, 2, 3] if a) if a)', m.UndefinedName)

    def test_undefinedWithErrorHandler(self):
        """
        Some compatibility code checks explicitly for NameError.
        It should not trigger warnings.
        """
        self.flakes('\n        try:\n            socket_map\n        except NameError:\n            socket_map = {}\n        ')
        self.flakes('\n        try:\n            _memoryview.contiguous\n        except (NameError, AttributeError):\n            raise RuntimeError("Python >= 3.3 is required")\n        ')
        self.flakes('\n        try:\n            socket_map\n        except:\n            socket_map = {}\n        ', m.UndefinedName)
        self.flakes('\n        try:\n            socket_map\n        except Exception:\n            socket_map = {}\n        ', m.UndefinedName)

    def test_definedInClass(self):
        """
        Defined name for generator expressions and dict/set comprehension.
        """
        self.flakes('\n        class A:\n            T = range(10)\n\n            Z = (x for x in T)\n            L = [x for x in T]\n            B = dict((i, str(i)) for i in T)\n        ')
        self.flakes('\n        class A:\n            T = range(10)\n\n            X = {x for x in T}\n            Y = {x:x for x in T}\n        ')

    def test_definedInClassNested(self):
        """Defined name for nested generator expressions in a class."""
        self.flakes('\n        class A:\n            T = range(10)\n\n            Z = (x for x in (a for a in T))\n        ')

    def test_undefinedInLoop(self):
        """
        The loop variable is defined after the expression is computed.
        """
        self.flakes('\n        for i in range(i):\n            print(i)\n        ', m.UndefinedName)
        self.flakes('\n        [42 for i in range(i)]\n        ', m.UndefinedName)
        self.flakes('\n        (42 for i in range(i))\n        ', m.UndefinedName)

    def test_definedFromLambdaInDictionaryComprehension(self):
        """
        Defined name referenced from a lambda function within a dict/set
        comprehension.
        """
        self.flakes('\n        {lambda: id(x) for x in range(10)}\n        ')

    def test_definedFromLambdaInGenerator(self):
        """
        Defined name referenced from a lambda function within a generator
        expression.
        """
        self.flakes('\n        any(lambda: id(x) for x in range(10))\n        ')

    def test_undefinedFromLambdaInDictionaryComprehension(self):
        """
        Undefined name referenced from a lambda function within a dict/set
        comprehension.
        """
        self.flakes('\n        {lambda: id(y) for x in range(10)}\n        ', m.UndefinedName)

    def test_undefinedFromLambdaInComprehension(self):
        """
        Undefined name referenced from a lambda function within a generator
        expression.
        """
        self.flakes('\n        any(lambda: id(y) for x in range(10))\n        ', m.UndefinedName)

    def test_dunderClass(self):
        """
        `__class__` is defined in class scope under Python 3, but is not
        in Python 2.
        """
        code = '\n        class Test(object):\n            def __init__(self):\n                print(__class__.__name__)\n                self.x = 1\n\n        t = Test()\n        '
        if version_info < (3, ):
            self.flakes(code, m.UndefinedName)
        else:
            self.flakes(code)


class NameTests(TestCase):
    __doc__ = '\n    Tests for some extra cases of name handling.\n    '

    def test_impossibleContext(self):
        """
        A Name node with an unrecognized context results in a RuntimeError being
        raised.
        """
        tree = ast.parse('x = 10')
        file_tokens = checker.make_tokens('x = 10')
        tree.body[0].targets[0].ctx = object()
        self.assertRaises(RuntimeError, (checker.Checker), tree, file_tokens=file_tokens)