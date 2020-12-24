# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/utils/unittest_ast_walker.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 2085 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, warnings, astroid
from pylint.checkers.utils import check_messages
from pylint.utils import ASTWalker

class TestASTWalker(object):

    class MockLinter(object):

        def __init__(self, msgs):
            self._msgs = msgs

        def is_message_enabled(self, msgid):
            return self._msgs.get(msgid, True)

    class Checker(object):

        def __init__(self):
            self.called = set()

        @check_messages('first-message')
        def visit_module(self, module):
            self.called.add('module')

        @check_messages('second-message')
        def visit_call(self, module):
            raise NotImplementedError

        @check_messages('second-message', 'third-message')
        def visit_assignname(self, module):
            self.called.add('assignname')

        @check_messages('second-message')
        def leave_assignname(self, module):
            raise NotImplementedError

    def test_check_messages(self):
        linter = self.MockLinter({'first-message':True, 
         'second-message':False,  'third-message':True})
        walker = ASTWalker(linter)
        checker = self.Checker()
        walker.add_checker(checker)
        walker.walk(astroid.parse('x = func()'))
        @py_assert0 = {'module', 'assignname'}
        @py_assert4 = checker.called
        @py_assert2 = @py_assert0 == @py_assert4
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_ast_walker.py', lineno=50)
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.called\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(checker) if 'checker' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checker) else 'checker',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    def test_deprecated_methods(self):

        class Checker(object):

            def __init__(self):
                self.called = False

            @check_messages('first-message')
            def visit_assname(self, node):
                self.called = True

        linter = self.MockLinter({'first-message': True})
        walker = ASTWalker(linter)
        checker = Checker()
        walker.add_checker(checker)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('always')
            walker.walk(astroid.parse('x = 1'))
            @py_assert1 = checker.called
            @py_assert3 = not @py_assert1
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/utils/unittest_ast_walker.py', lineno=69)
            if not @py_assert3:
                @py_format4 = 'assert not %(py2)s\n{%(py2)s = %(py0)s.called\n}' % {'py0':@pytest_ar._saferepr(checker) if 'checker' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checker) else 'checker',  'py2':@pytest_ar._saferepr(@py_assert1)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format4))
            @py_assert1 = @py_assert3 = None