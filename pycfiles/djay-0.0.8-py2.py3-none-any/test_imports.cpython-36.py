# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_imports.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 34273 bytes
from sys import version_info
from pyflakes import messages as m
from pyflakes.checker import FutureImportation, Importation, ImportationFrom, StarImportation, SubmoduleImportation
from pyflakes.test.harness import TestCase, skip, skipIf

class TestImportationObject(TestCase):

    def test_import_basic(self):
        binding = Importation('a', None, 'a')
        if not binding.source_statement == 'import a':
            raise AssertionError
        elif not str(binding) == 'a':
            raise AssertionError

    def test_import_as(self):
        binding = Importation('c', None, 'a')
        if not binding.source_statement == 'import a as c':
            raise AssertionError
        elif not str(binding) == 'a as c':
            raise AssertionError

    def test_import_submodule(self):
        binding = SubmoduleImportation('a.b', None)
        if not binding.source_statement == 'import a.b':
            raise AssertionError
        elif not str(binding) == 'a.b':
            raise AssertionError

    def test_import_submodule_as(self):
        binding = Importation('c', None, 'a.b')
        if not binding.source_statement == 'import a.b as c':
            raise AssertionError
        elif not str(binding) == 'a.b as c':
            raise AssertionError

    def test_import_submodule_as_source_name(self):
        binding = Importation('a', None, 'a.b')
        if not binding.source_statement == 'import a.b as a':
            raise AssertionError
        elif not str(binding) == 'a.b as a':
            raise AssertionError

    def test_importfrom_relative(self):
        binding = ImportationFrom('a', None, '.', 'a')
        if not binding.source_statement == 'from . import a':
            raise AssertionError
        elif not str(binding) == '.a':
            raise AssertionError

    def test_importfrom_relative_parent(self):
        binding = ImportationFrom('a', None, '..', 'a')
        if not binding.source_statement == 'from .. import a':
            raise AssertionError
        elif not str(binding) == '..a':
            raise AssertionError

    def test_importfrom_relative_with_module(self):
        binding = ImportationFrom('b', None, '..a', 'b')
        if not binding.source_statement == 'from ..a import b':
            raise AssertionError
        elif not str(binding) == '..a.b':
            raise AssertionError

    def test_importfrom_relative_with_module_as(self):
        binding = ImportationFrom('c', None, '..a', 'b')
        if not binding.source_statement == 'from ..a import b as c':
            raise AssertionError
        elif not str(binding) == '..a.b as c':
            raise AssertionError

    def test_importfrom_member(self):
        binding = ImportationFrom('b', None, 'a', 'b')
        if not binding.source_statement == 'from a import b':
            raise AssertionError
        elif not str(binding) == 'a.b':
            raise AssertionError

    def test_importfrom_submodule_member(self):
        binding = ImportationFrom('c', None, 'a.b', 'c')
        if not binding.source_statement == 'from a.b import c':
            raise AssertionError
        elif not str(binding) == 'a.b.c':
            raise AssertionError

    def test_importfrom_member_as(self):
        binding = ImportationFrom('c', None, 'a', 'b')
        if not binding.source_statement == 'from a import b as c':
            raise AssertionError
        elif not str(binding) == 'a.b as c':
            raise AssertionError

    def test_importfrom_submodule_member_as(self):
        binding = ImportationFrom('d', None, 'a.b', 'c')
        if not binding.source_statement == 'from a.b import c as d':
            raise AssertionError
        elif not str(binding) == 'a.b.c as d':
            raise AssertionError

    def test_importfrom_star(self):
        binding = StarImportation('a.b', None)
        if not binding.source_statement == 'from a.b import *':
            raise AssertionError
        elif not str(binding) == 'a.b.*':
            raise AssertionError

    def test_importfrom_star_relative(self):
        binding = StarImportation('.b', None)
        if not binding.source_statement == 'from .b import *':
            raise AssertionError
        elif not str(binding) == '.b.*':
            raise AssertionError

    def test_importfrom_future(self):
        binding = FutureImportation('print_function', None, None)
        if not binding.source_statement == 'from __future__ import print_function':
            raise AssertionError
        elif not str(binding) == '__future__.print_function':
            raise AssertionError

    def test_unusedImport_underscore(self):
        """
        The magic underscore var should be reported as unused when used as an
        import alias.
        """
        self.flakes('import fu as _', m.UnusedImport)


class Test(TestCase):

    def test_unusedImport(self):
        self.flakes('import fu, bar', m.UnusedImport, m.UnusedImport)
        self.flakes('from baz import fu, bar', m.UnusedImport, m.UnusedImport)

    def test_unusedImport_relative(self):
        self.flakes('from . import fu', m.UnusedImport)
        self.flakes('from . import fu as baz', m.UnusedImport)
        self.flakes('from .. import fu', m.UnusedImport)
        self.flakes('from ... import fu', m.UnusedImport)
        self.flakes('from .. import fu as baz', m.UnusedImport)
        self.flakes('from .bar import fu', m.UnusedImport)
        self.flakes('from ..bar import fu', m.UnusedImport)
        self.flakes('from ...bar import fu', m.UnusedImport)
        self.flakes('from ...bar import fu as baz', m.UnusedImport)
        checker = self.flakes('from . import fu', m.UnusedImport)
        error = checker.messages[0]
        if not error.message == '%r imported but unused':
            raise AssertionError
        else:
            if not error.message_args == ('.fu', ):
                raise AssertionError
            else:
                checker = self.flakes('from . import fu as baz', m.UnusedImport)
                error = checker.messages[0]
                assert error.message == '%r imported but unused'
            assert error.message_args == ('.fu as baz', )

    def test_aliasedImport(self):
        self.flakes('import fu as FU, bar as FU', m.RedefinedWhileUnused, m.UnusedImport)
        self.flakes('from moo import fu as FU, bar as FU', m.RedefinedWhileUnused, m.UnusedImport)

    def test_aliasedImportShadowModule(self):
        """Imported aliases can shadow the source of the import."""
        self.flakes('from moo import fu as moo; moo')
        self.flakes('import fu as fu; fu')
        self.flakes('import fu.bar as fu; fu')

    def test_usedImport(self):
        self.flakes('import fu; print(fu)')
        self.flakes('from baz import fu; print(fu)')
        self.flakes('import fu; del fu')

    def test_usedImport_relative(self):
        self.flakes('from . import fu; assert fu')
        self.flakes('from .bar import fu; assert fu')
        self.flakes('from .. import fu; assert fu')
        self.flakes('from ..bar import fu as baz; assert baz')

    def test_redefinedWhileUnused(self):
        self.flakes('import fu; fu = 3', m.RedefinedWhileUnused)
        self.flakes('import fu; fu, bar = 3', m.RedefinedWhileUnused)
        self.flakes('import fu; [fu, bar] = 3', m.RedefinedWhileUnused)

    def test_redefinedIf(self):
        """
        Test that importing a module twice within an if
        block does raise a warning.
        """
        self.flakes('\n        i = 2\n        if i==1:\n            import os\n            import os\n        os.path', m.RedefinedWhileUnused)

    def test_redefinedIfElse(self):
        """
        Test that importing a module twice in if
        and else blocks does not raise a warning.
        """
        self.flakes('\n        i = 2\n        if i==1:\n            import os\n        else:\n            import os\n        os.path')

    def test_redefinedTry(self):
        """
        Test that importing a module twice in a try block
        does raise a warning.
        """
        self.flakes('\n        try:\n            import os\n            import os\n        except:\n            pass\n        os.path', m.RedefinedWhileUnused)

    def test_redefinedTryExcept(self):
        """
        Test that importing a module twice in a try
        and except block does not raise a warning.
        """
        self.flakes('\n        try:\n            import os\n        except:\n            import os\n        os.path')

    def test_redefinedTryNested(self):
        """
        Test that importing a module twice using a nested
        try/except and if blocks does not issue a warning.
        """
        self.flakes('\n        try:\n            if True:\n                if True:\n                    import os\n        except:\n            import os\n        os.path')

    def test_redefinedTryExceptMulti(self):
        self.flakes('\n        try:\n            from aa import mixer\n        except AttributeError:\n            from bb import mixer\n        except RuntimeError:\n            from cc import mixer\n        except:\n            from dd import mixer\n        mixer(123)\n        ')

    def test_redefinedTryElse(self):
        self.flakes('\n        try:\n            from aa import mixer\n        except ImportError:\n            pass\n        else:\n            from bb import mixer\n        mixer(123)\n        ', m.RedefinedWhileUnused)

    def test_redefinedTryExceptElse(self):
        self.flakes('\n        try:\n            import funca\n        except ImportError:\n            from bb import funca\n            from bb import funcb\n        else:\n            from bbb import funcb\n        print(funca, funcb)\n        ')

    def test_redefinedTryExceptFinally(self):
        self.flakes('\n        try:\n            from aa import a\n        except ImportError:\n            from bb import a\n        finally:\n            a = 42\n        print(a)\n        ')

    def test_redefinedTryExceptElseFinally(self):
        self.flakes('\n        try:\n            import b\n        except ImportError:\n            b = Ellipsis\n            from bb import a\n        else:\n            from aa import a\n        finally:\n            a = 42\n        print(a, b)\n        ')

    def test_redefinedByFunction(self):
        self.flakes('\n        import fu\n        def fu():\n            pass\n        ', m.RedefinedWhileUnused)

    def test_redefinedInNestedFunction(self):
        """
        Test that shadowing a global name with a nested function definition
        generates a warning.
        """
        self.flakes('\n        import fu\n        def bar():\n            def baz():\n                def fu():\n                    pass\n        ', m.RedefinedWhileUnused, m.UnusedImport)

    def test_redefinedInNestedFunctionTwice(self):
        """
        Test that shadowing a global name with a nested function definition
        generates a warning.
        """
        self.flakes('\n        import fu\n        def bar():\n            import fu\n            def baz():\n                def fu():\n                    pass\n        ', m.RedefinedWhileUnused, m.RedefinedWhileUnused, m.UnusedImport, m.UnusedImport)

    def test_redefinedButUsedLater(self):
        """
        Test that a global import which is redefined locally,
        but used later in another scope does not generate a warning.
        """
        self.flakes("\n        import unittest, transport\n\n        class GetTransportTestCase(unittest.TestCase):\n            def test_get_transport(self):\n                transport = 'transport'\n                self.assertIsNotNone(transport)\n\n        class TestTransportMethodArgs(unittest.TestCase):\n            def test_send_defaults(self):\n                transport.Transport()\n        ")

    def test_redefinedByClass(self):
        self.flakes('\n        import fu\n        class fu:\n            pass\n        ', m.RedefinedWhileUnused)

    def test_redefinedBySubclass(self):
        """
        If an imported name is redefined by a class statement which also uses
        that name in the bases list, no warning is emitted.
        """
        self.flakes('\n        from fu import bar\n        class bar(bar):\n            pass\n        ')

    def test_redefinedInClass(self):
        """
        Test that shadowing a global with a class attribute does not produce a
        warning.
        """
        self.flakes('\n        import fu\n        class bar:\n            fu = 1\n        print(fu)\n        ')

    def test_importInClass(self):
        """
        Test that import within class is a locally scoped attribute.
        """
        self.flakes('\n        class bar:\n            import fu\n        ')
        self.flakes('\n        class bar:\n            import fu\n\n        fu\n        ', m.UndefinedName)

    def test_usedInFunction(self):
        self.flakes('\n        import fu\n        def fun():\n            print(fu)\n        ')

    def test_shadowedByParameter(self):
        self.flakes('\n        import fu\n        def fun(fu):\n            print(fu)\n        ', m.UnusedImport, m.RedefinedWhileUnused)
        self.flakes('\n        import fu\n        def fun(fu):\n            print(fu)\n        print(fu)\n        ')

    def test_newAssignment(self):
        self.flakes('fu = None')

    def test_usedInGetattr(self):
        self.flakes('import fu; fu.bar.baz')
        self.flakes('import fu; "bar".fu.baz', m.UnusedImport)

    def test_usedInSlice(self):
        self.flakes('import fu; print(fu.bar[1:])')

    def test_usedInIfBody(self):
        self.flakes('\n        import fu\n        if True: print(fu)\n        ')

    def test_usedInIfConditional(self):
        self.flakes('\n        import fu\n        if fu: pass\n        ')

    def test_usedInElifConditional(self):
        self.flakes('\n        import fu\n        if False: pass\n        elif fu: pass\n        ')

    def test_usedInElse(self):
        self.flakes('\n        import fu\n        if False: pass\n        else: print(fu)\n        ')

    def test_usedInCall(self):
        self.flakes('import fu; fu.bar()')

    def test_usedInClass(self):
        self.flakes('\n        import fu\n        class bar:\n            bar = fu\n        ')

    def test_usedInClassBase(self):
        self.flakes('\n        import fu\n        class bar(object, fu.baz):\n            pass\n        ')

    def test_notUsedInNestedScope(self):
        self.flakes('\n        import fu\n        def bleh():\n            pass\n        print(fu)\n        ')

    def test_usedInFor(self):
        self.flakes('\n        import fu\n        for bar in range(9):\n            print(fu)\n        ')

    def test_usedInForElse(self):
        self.flakes('\n        import fu\n        for bar in range(10):\n            pass\n        else:\n            print(fu)\n        ')

    def test_redefinedByFor(self):
        self.flakes('\n        import fu\n        for fu in range(2):\n            pass\n        ', m.ImportShadowedByLoopVar)

    def test_shadowedByFor(self):
        """
        Test that shadowing a global name with a for loop variable generates a
        warning.
        """
        self.flakes('\n        import fu\n        fu.bar()\n        for fu in ():\n            pass\n        ', m.ImportShadowedByLoopVar)

    def test_shadowedByForDeep(self):
        """
        Test that shadowing a global name with a for loop variable nested in a
        tuple unpack generates a warning.
        """
        self.flakes('\n        import fu\n        fu.bar()\n        for (x, y, z, (a, b, c, (fu,))) in ():\n            pass\n        ', m.ImportShadowedByLoopVar)
        self.flakes('\n        import fu\n        fu.bar()\n        for [x, y, z, (a, b, c, (fu,))] in ():\n            pass\n        ', m.ImportShadowedByLoopVar)

    def test_usedInReturn(self):
        self.flakes('\n        import fu\n        def fun():\n            return fu\n        ')

    def test_usedInOperators(self):
        self.flakes('import fu; 3 + fu.bar')
        self.flakes('import fu; 3 % fu.bar')
        self.flakes('import fu; 3 - fu.bar')
        self.flakes('import fu; 3 * fu.bar')
        self.flakes('import fu; 3 ** fu.bar')
        self.flakes('import fu; 3 / fu.bar')
        self.flakes('import fu; 3 // fu.bar')
        self.flakes('import fu; -fu.bar')
        self.flakes('import fu; ~fu.bar')
        self.flakes('import fu; 1 == fu.bar')
        self.flakes('import fu; 1 | fu.bar')
        self.flakes('import fu; 1 & fu.bar')
        self.flakes('import fu; 1 ^ fu.bar')
        self.flakes('import fu; 1 >> fu.bar')
        self.flakes('import fu; 1 << fu.bar')

    def test_usedInAssert(self):
        self.flakes('import fu; assert fu.bar')

    def test_usedInSubscript(self):
        self.flakes('import fu; fu.bar[1]')

    def test_usedInLogic(self):
        self.flakes('import fu; fu and False')
        self.flakes('import fu; fu or False')
        self.flakes('import fu; not fu.bar')

    def test_usedInList(self):
        self.flakes('import fu; [fu]')

    def test_usedInTuple(self):
        self.flakes('import fu; (fu,)')

    def test_usedInTry(self):
        self.flakes('\n        import fu\n        try: fu\n        except: pass\n        ')

    def test_usedInExcept(self):
        self.flakes('\n        import fu\n        try: fu\n        except: pass\n        ')

    def test_redefinedByExcept(self):
        expected = [
         m.RedefinedWhileUnused]
        if version_info >= (3, ):
            expected.append(m.UnusedVariable)
        (self.flakes)(*('\n        import fu\n        try: pass\n        except Exception as fu: pass\n        ', ), *expected)

    def test_usedInRaise(self):
        self.flakes('\n        import fu\n        raise fu.bar\n        ')

    def test_usedInYield(self):
        self.flakes('\n        import fu\n        def gen():\n            yield fu\n        ')

    def test_usedInDict(self):
        self.flakes('import fu; {fu:None}')
        self.flakes('import fu; {1:fu}')

    def test_usedInParameterDefault(self):
        self.flakes('\n        import fu\n        def f(bar=fu):\n            pass\n        ')

    def test_usedInAttributeAssign(self):
        self.flakes('import fu; fu.bar = 1')

    def test_usedInKeywordArg(self):
        self.flakes('import fu; fu.bar(stuff=fu)')

    def test_usedInAssignment(self):
        self.flakes('import fu; bar=fu')
        self.flakes('import fu; n=0; n+=fu')

    def test_usedInListComp(self):
        self.flakes('import fu; [fu for _ in range(1)]')
        self.flakes('import fu; [1 for _ in range(1) if fu]')

    @skipIf(version_info >= (3, ), 'in Python 3 list comprehensions execute in a separate scope')
    def test_redefinedByListComp(self):
        self.flakes('import fu; [1 for fu in range(1)]', m.RedefinedInListComp)

    def test_usedInTryFinally(self):
        self.flakes('\n        import fu\n        try: pass\n        finally: fu\n        ')
        self.flakes('\n        import fu\n        try: fu\n        finally: pass\n        ')

    def test_usedInWhile(self):
        self.flakes('\n        import fu\n        while 0:\n            fu\n        ')
        self.flakes('\n        import fu\n        while fu: pass\n        ')

    def test_usedInGlobal(self):
        """
        A 'global' statement shadowing an unused import should not prevent it
        from being reported.
        """
        self.flakes('\n        import fu\n        def f(): global fu\n        ', m.UnusedImport)

    def test_usedAndGlobal(self):
        """
        A 'global' statement shadowing a used import should not cause it to be
        reported as unused.
        """
        self.flakes('\n            import foo\n            def f(): global foo\n            def g(): foo.is_used()\n        ')

    def test_assignedToGlobal(self):
        """
        Binding an import to a declared global should not cause it to be
        reported as unused.
        """
        self.flakes('\n            def f(): global foo; import foo\n            def g(): foo.is_used()\n        ')

    @skipIf(version_info >= (3, ), 'deprecated syntax')
    def test_usedInBackquote(self):
        self.flakes('import fu; `fu`')

    def test_usedInExec(self):
        if version_info < (3, ):
            exec_stmt = 'exec "print 1" in fu.bar'
        else:
            exec_stmt = 'exec("print(1)", fu.bar)'
        self.flakes('import fu; %s' % exec_stmt)

    def test_usedInLambda(self):
        self.flakes('import fu; lambda: fu')

    def test_shadowedByLambda(self):
        self.flakes('import fu; lambda fu: fu', m.UnusedImport, m.RedefinedWhileUnused)
        self.flakes('import fu; lambda fu: fu\nfu()')

    def test_usedInSliceObj(self):
        self.flakes('import fu; "meow"[::fu]')

    def test_unusedInNestedScope(self):
        self.flakes('\n        def bar():\n            import fu\n        fu\n        ', m.UnusedImport, m.UndefinedName)

    def test_methodsDontUseClassScope(self):
        self.flakes('\n        class bar:\n            import fu\n            def fun(self):\n                fu\n        ', m.UndefinedName)

    def test_nestedFunctionsNestScope(self):
        self.flakes('\n        def a():\n            def b():\n                fu\n            import fu\n        ')

    def test_nestedClassAndFunctionScope(self):
        self.flakes('\n        def a():\n            import fu\n            class b:\n                def c(self):\n                    print(fu)\n        ')

    def test_importStar(self):
        """Use of import * at module level is reported."""
        self.flakes('from fu import *', m.ImportStarUsed, m.UnusedImport)
        self.flakes('\n        try:\n            from fu import *\n        except:\n            pass\n        ', m.ImportStarUsed, m.UnusedImport)
        checker = self.flakes('from fu import *', m.ImportStarUsed, m.UnusedImport)
        error = checker.messages[0]
        if not error.message.startswith("'from %s import *' used; unable "):
            raise AssertionError
        else:
            if not error.message_args == ('fu', ):
                raise AssertionError
            else:
                error = checker.messages[1]
                assert error.message == '%r imported but unused'
            assert error.message_args == ('fu.*', )

    def test_importStar_relative(self):
        """Use of import * from a relative import is reported."""
        self.flakes('from .fu import *', m.ImportStarUsed, m.UnusedImport)
        self.flakes('\n        try:\n            from .fu import *\n        except:\n            pass\n        ', m.ImportStarUsed, m.UnusedImport)
        checker = self.flakes('from .fu import *', m.ImportStarUsed, m.UnusedImport)
        error = checker.messages[0]
        if not error.message.startswith("'from %s import *' used; unable "):
            raise AssertionError
        else:
            if not error.message_args == ('.fu', ):
                raise AssertionError
            else:
                error = checker.messages[1]
                assert error.message == '%r imported but unused'
                assert error.message_args == ('.fu.*', )
                checker = self.flakes('from .. import *', m.ImportStarUsed, m.UnusedImport)
                error = checker.messages[0]
                assert error.message.startswith("'from %s import *' used; unable ")
                assert error.message_args == ('..', )
                error = checker.messages[1]
                assert error.message == '%r imported but unused'
            assert error.message_args == ('from .. import *', )

    @skipIf(version_info < (3, ), 'import * below module level is a warning on Python 2')
    def test_localImportStar(self):
        """import * is only allowed at module level."""
        self.flakes('\n        def a():\n            from fu import *\n        ', m.ImportStarNotPermitted)
        self.flakes('\n        class a:\n            from fu import *\n        ', m.ImportStarNotPermitted)
        checker = self.flakes('\n        class a:\n            from .. import *\n        ', m.ImportStarNotPermitted)
        error = checker.messages[0]
        if not error.message == "'from %s import *' only allowed at module level":
            raise AssertionError
        elif not error.message_args == ('..', ):
            raise AssertionError

    @skipIf(version_info > (3, ), 'import * below module level is an error on Python 3')
    def test_importStarNested(self):
        """All star imports are marked as used by an undefined variable."""
        self.flakes('\n        from fu import *\n        def f():\n            from bar import *\n            x\n        ', m.ImportStarUsed, m.ImportStarUsed, m.ImportStarUsage)

    def test_packageImport(self):
        """
        If a dotted name is imported and used, no warning is reported.
        """
        self.flakes('\n        import fu.bar\n        fu.bar\n        ')

    def test_unusedPackageImport(self):
        """
        If a dotted name is imported and not used, an unused import warning is
        reported.
        """
        self.flakes('import fu.bar', m.UnusedImport)

    def test_duplicateSubmoduleImport(self):
        """
        If a submodule of a package is imported twice, an unused import warning
        and a redefined while unused warning are reported.
        """
        self.flakes('\n        import fu.bar, fu.bar\n        fu.bar\n        ', m.RedefinedWhileUnused)
        self.flakes('\n        import fu.bar\n        import fu.bar\n        fu.bar\n        ', m.RedefinedWhileUnused)

    def test_differentSubmoduleImport(self):
        """
        If two different submodules of a package are imported, no duplicate
        import warning is reported for the package.
        """
        self.flakes('\n        import fu.bar, fu.baz\n        fu.bar, fu.baz\n        ')
        self.flakes('\n        import fu.bar\n        import fu.baz\n        fu.bar, fu.baz\n        ')

    def test_used_package_with_submodule_import(self):
        """
        Usage of package marks submodule imports as used.
        """
        self.flakes('\n        import fu\n        import fu.bar\n        fu.x\n        ')
        self.flakes('\n        import fu.bar\n        import fu\n        fu.x\n        ')

    def test_used_package_with_submodule_import_of_alias(self):
        """
        Usage of package by alias marks submodule imports as used.
        """
        self.flakes('\n        import foo as f\n        import foo.bar\n        f.bar.do_something()\n        ')
        self.flakes('\n        import foo as f\n        import foo.bar.blah\n        f.bar.blah.do_something()\n        ')

    def test_unused_package_with_submodule_import(self):
        """
        When a package and its submodule are imported, only report once.
        """
        checker = self.flakes('\n        import fu\n        import fu.bar\n        ', m.UnusedImport)
        error = checker.messages[0]
        if not error.message == '%r imported but unused':
            raise AssertionError
        else:
            assert error.message_args == ('fu.bar', )
            assert error.lineno == 5 if self.withDoctest else 3

    def test_assignRHSFirst(self):
        self.flakes('import fu; fu = fu')
        self.flakes('import fu; fu, bar = fu')
        self.flakes('import fu; [fu, bar] = fu')
        self.flakes('import fu; fu += fu')

    def test_tryingMultipleImports(self):
        self.flakes('\n        try:\n            import fu\n        except ImportError:\n            import bar as fu\n        fu\n        ')

    def test_nonGlobalDoesNotRedefine(self):
        self.flakes('\n        import fu\n        def a():\n            fu = 3\n            return fu\n        fu\n        ')

    def test_functionsRunLater(self):
        self.flakes('\n        def a():\n            fu\n        import fu\n        ')

    def test_functionNamesAreBoundNow(self):
        self.flakes('\n        import fu\n        def fu():\n            fu\n        fu\n        ', m.RedefinedWhileUnused)

    def test_ignoreNonImportRedefinitions(self):
        self.flakes('a = 1; a = 2')

    @skip('todo')
    def test_importingForImportError(self):
        self.flakes('\n        try:\n            import fu\n        except ImportError:\n            pass\n        ')

    def test_importedInClass(self):
        """Imports in class scope can be used through self."""
        self.flakes('\n        class c:\n            import i\n            def __init__(self):\n                self.i\n        ')

    def test_importUsedInMethodDefinition(self):
        """
        Method named 'foo' with default args referring to module named 'foo'.
        """
        self.flakes('\n        import foo\n\n        class Thing(object):\n            def foo(self, parser=foo.parse_foo):\n                pass\n        ')

    def test_futureImport(self):
        """__future__ is special."""
        self.flakes('from __future__ import division')
        self.flakes('\n        "docstring is allowed before future import"\n        from __future__ import division\n        ')

    def test_futureImportFirst(self):
        """
        __future__ imports must come before anything else.
        """
        self.flakes('\n        x = 5\n        from __future__ import division\n        ', m.LateFutureImport)
        self.flakes('\n        from foo import bar\n        from __future__ import division\n        bar\n        ', m.LateFutureImport)

    def test_futureImportUsed(self):
        """__future__ is special, but names are injected in the namespace."""
        self.flakes('\n        from __future__ import division\n        from __future__ import print_function\n\n        assert print_function is not division\n        ')

    def test_futureImportUndefined(self):
        """Importing undefined names from __future__ fails."""
        self.flakes('\n        from __future__ import print_statement\n        ', m.FutureFeatureNotDefined)

    def test_futureImportStar(self):
        """Importing '*' from __future__ fails."""
        self.flakes('\n        from __future__ import *\n        ', m.FutureFeatureNotDefined)


class TestSpecialAll(TestCase):
    __doc__ = '\n    Tests for suppression of unused import warnings by C{__all__}.\n    '

    def test_ignoredInFunction(self):
        """
        An C{__all__} definition does not suppress unused import warnings in a
        function scope.
        """
        self.flakes('\n        def foo():\n            import bar\n            __all__ = ["bar"]\n        ', m.UnusedImport, m.UnusedVariable)

    def test_ignoredInClass(self):
        """
        An C{__all__} definition in a class does not suppress unused import warnings.
        """
        self.flakes('\n        import bar\n        class foo:\n            __all__ = ["bar"]\n        ', m.UnusedImport)

    def test_warningSuppressed(self):
        """
        If a name is imported and unused but is named in C{__all__}, no warning
        is reported.
        """
        self.flakes('\n        import foo\n        __all__ = ["foo"]\n        ')
        self.flakes('\n        import foo\n        __all__ = ("foo",)\n        ')

    def test_augmentedAssignment(self):
        """
        The C{__all__} variable is defined incrementally.
        """
        self.flakes("\n        import a\n        import c\n        __all__ = ['a']\n        __all__ += ['b']\n        if 1 < 3:\n            __all__ += ['c', 'd']\n        ", m.UndefinedExport, m.UndefinedExport)

    def test_concatenationAssignment(self):
        """
        The C{__all__} variable is defined through list concatenation.
        """
        self.flakes("\n        import sys\n        __all__ = ['a'] + ['b'] + ['c']\n        ", m.UndefinedExport, m.UndefinedExport, m.UndefinedExport, m.UnusedImport)

    def test_all_with_attributes(self):
        self.flakes('\n        from foo import bar\n        __all__ = [bar.__name__]\n        ')

    def test_all_with_names(self):
        self.flakes('\n        from foo import bar\n        __all__ = [bar]\n        ')

    def test_all_with_attributes_added(self):
        self.flakes('\n        from foo import bar\n        from bar import baz\n        __all__ = [bar.__name__] + [baz.__name__]\n        ')

    def test_all_mixed_attributes_and_strings(self):
        self.flakes("\n        from foo import bar\n        from foo import baz\n        __all__ = ['bar', baz.__name__]\n        ")

    def test_unboundExported(self):
        """
        If C{__all__} includes a name which is not bound, a warning is emitted.
        """
        self.flakes('\n        __all__ = ["foo"]\n        ', m.UndefinedExport)
        for filename in ('foo/__init__.py', '__init__.py'):
            self.flakes('\n            __all__ = ["foo"]\n            ',
              filename=filename)

    def test_importStarExported(self):
        """
        Report undefined if import * is used
        """
        self.flakes("\n        from math import *\n        __all__ = ['sin', 'cos']\n        csc(1)\n        ", m.ImportStarUsed, m.ImportStarUsage, m.ImportStarUsage, m.ImportStarUsage)

    def test_importStarNotExported(self):
        """Report unused import when not needed to satisfy __all__."""
        self.flakes("\n        from foolib import *\n        a = 1\n        __all__ = ['a']\n        ", m.ImportStarUsed, m.UnusedImport)

    def test_usedInGenExp(self):
        """
        Using a global in a generator expression results in no warnings.
        """
        self.flakes('import fu; (fu for _ in range(1))')
        self.flakes('import fu; (1 for _ in range(1) if fu)')

    def test_redefinedByGenExp(self):
        """
        Re-using a global name as the loop variable for a generator
        expression results in a redefinition warning.
        """
        self.flakes('import fu; (1 for fu in range(1))', m.RedefinedWhileUnused, m.UnusedImport)

    def test_usedAsDecorator(self):
        """
        Using a global name in a decorator statement results in no warnings,
        but using an undefined name in a decorator statement results in an
        undefined name warning.
        """
        self.flakes('\n        from interior import decorate\n        @decorate\n        def f():\n            return "hello"\n        ')
        self.flakes('\n        from interior import decorate\n        @decorate(\'value\')\n        def f():\n            return "hello"\n        ')
        self.flakes('\n        @decorate\n        def f():\n            return "hello"\n        ', m.UndefinedName)

    def test_usedAsClassDecorator(self):
        """
        Using an imported name as a class decorator results in no warnings,
        but using an undefined name as a class decorator results in an
        undefined name warning.
        """
        self.flakes('\n        from interior import decorate\n        @decorate\n        class foo:\n            pass\n        ')
        self.flakes('\n        from interior import decorate\n        @decorate("foo")\n        class bar:\n            pass\n        ')
        self.flakes('\n        @decorate\n        class foo:\n            pass\n        ', m.UndefinedName)