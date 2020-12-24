# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_strings.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 2493 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid
from pylint.checkers import strings
from pylint.testutils import CheckerTestCase, Message
TEST_TOKENS = ('"X"', "'X'", "'''X'''", '"""X"""', 'r"X"', "R'X'", 'u"X"', "F'X'",
               'f"X"', "F'X'", 'fr"X"', 'Fr"X"', 'fR"X"', 'FR"X"', 'rf"X"', 'rF"X"',
               'Rf"X"', 'RF"X"')

class TestStringChecker(CheckerTestCase):
    CHECKER_CLASS = strings.StringFormatChecker

    def test_format_bytes(self):
        code = "b'test'.format(1, 2)"
        node = astroid.extract_node(code)
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_format_types(self):
        for code in ("'%s' % 1", "'%d' % 1", "'%f' % 1"):
            with self.assertNoMessages():
                node = astroid.extract_node(code)
            self.checker.visit_binop(node)

        for code in ("'%s' % 1", "'%(key)s' % {'key' : 1}", "'%d' % 1", "'%(key)d' % {'key' : 1}",
                     "'%f' % 1", "'%(key)f' % {'key' : 1}", "'%d' % 1.1", "'%(key)d' % {'key' : 1.1}",
                     "'%s' % []", "'%(key)s' % {'key' : []}", "'%s' % None", "'%(key)s' % {'key' : None}"):
            with self.assertNoMessages():
                node = astroid.extract_node(code)
                self.checker.visit_binop(node)

        for code, arg_type, format_type in (("'%d' % '1'", 'builtins.str', 'd'), ("'%(key)d' % {'key' : '1'}", 'builtins.str', 'd'),
                                            ("'%x' % 1.1", 'builtins.float', 'x'),
                                            ("'%(key)x' % {'key' : 1.1}", 'builtins.float', 'x'),
                                            ("'%d' % []", 'builtins.list', 'd'),
                                            ("'%(key)d' % {'key' : []}", 'builtins.list', 'd')):
            node = astroid.extract_node(code)
            with self.assertAddsMessages(Message('bad-string-format-type',
              node=node, args=(arg_type, format_type))):
                self.checker.visit_binop(node)

    def test_str_eval(self):
        for token in TEST_TOKENS:
            @py_assert1 = strings.str_eval
            @py_assert4 = @py_assert1(token)
            @py_assert7 = 'X'
            @py_assert6 = @py_assert4 == @py_assert7
            if @py_assert6 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_strings.py', lineno=85)
            if not @py_assert6:
                @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.str_eval\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(strings) if 'strings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(strings) else 'strings',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(token) if 'token' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(token) else 'token',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None