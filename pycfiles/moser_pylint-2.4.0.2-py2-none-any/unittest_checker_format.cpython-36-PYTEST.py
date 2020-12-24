# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_format.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 18277 bytes
"""Check format checker helper functions"""
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, tempfile, tokenize, astroid
from pylint import lint, reporters
from pylint.checkers.format import *
from pylint.testutils import CheckerTestCase, Message, _tokenize_str, set_config

class TestMultiStatementLine(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testSingleLineIfStmts(self):
        stmt = astroid.extract_node('\n        if True: pass  #@\n        ')
        self.checker.config.single_line_if_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=(stmt.body[0]))):
            self.visitFirst(stmt)
        self.checker.config.single_line_if_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)
        stmt = astroid.extract_node('\n        if True: pass  #@\n        else:\n            pass\n        ')
        with self.assertAddsMessages(Message('multiple-statements', node=(stmt.body[0]))):
            self.visitFirst(stmt)

    def testSingleLineClassStmts(self):
        stmt = astroid.extract_node('\n        class MyError(Exception): pass  #@\n        ')
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=(stmt.body[0]))):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)
        stmt = astroid.extract_node("\n        class MyError(Exception): a='a'  #@\n        ")
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=(stmt.body[0]))):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)
        stmt = astroid.extract_node("\n        class MyError(Exception): a='a'; b='b'  #@\n        ")
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=(stmt.body[0]))):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertAddsMessages(Message('multiple-statements', node=(stmt.body[0]))):
            self.visitFirst(stmt)

    def testTryExceptFinallyNoMultipleStatement(self):
        tree = astroid.extract_node('\n        try:  #@\n            pass\n        except:\n            pass\n        finally:\n            pass')
        with self.assertNoMessages():
            self.visitFirst(tree)

    def visitFirst(self, tree):
        self.checker.process_tokens([])
        self.checker.visit_default(tree.body[0])


class TestSuperfluousParentheses(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testCheckKeywordParensHandlesValidCases(self):
        self.checker._keywords_with_parens = set()
        cases = [
         'if foo:',
         'if foo():',
         'if (x and y) or z:',
         'assert foo()',
         'assert ()',
         'if (1, 2) in (3, 4):',
         'if (a or b) in c:',
         'return (x for x in x)',
         'if (x for x in x):',
         'for x in (x for x in x):',
         'not (foo or bar)',
         'not (foo or bar) and baz']
        with self.assertNoMessages():
            for code in cases:
                self.checker._check_keyword_parentheses(_tokenize_str(code), 0)

    def testCheckKeywordParensHandlesUnnecessaryParens(self):
        self.checker._keywords_with_parens = set()
        cases = [
         (
          Message('superfluous-parens', line=1, args='if'), 'if (foo):', 0),
         (
          Message('superfluous-parens', line=1, args='if'), 'if ((foo, bar)):', 0),
         (
          Message('superfluous-parens', line=1, args='if'), 'if (foo(bar)):', 0),
         (
          Message('superfluous-parens', line=1, args='return'),
          'return ((x for x in x))',
          0),
         (
          Message('superfluous-parens', line=1, args='not'), 'not (foo)', 0),
         (
          Message('superfluous-parens', line=1, args='not'), 'if not (foo):', 1),
         (
          Message('superfluous-parens', line=1, args='if'), 'if (not (foo)):', 0),
         (
          Message('superfluous-parens', line=1, args='not'), 'if (not (foo)):', 2),
         (
          Message('superfluous-parens', line=1, args='for'),
          'for (x) in (1, 2, 3):',
          0),
         (
          Message('superfluous-parens', line=1, args='if'),
          'if (1) in (1, 2, 3):',
          0)]
        for msg, code, offset in cases:
            with self.assertAddsMessages(msg):
                self.checker._check_keyword_parentheses(_tokenize_str(code), offset)

    def testCheckIfArgsAreNotUnicode(self):
        self.checker._keywords_with_parens = set()
        cases = [('if (foo):', 0), ('assert (1 == 1)', 0)]
        for code, offset in cases:
            self.checker._check_keyword_parentheses(_tokenize_str(code), offset)
            got = self.linter.release_messages()
            @py_assert1 = got[(-1)]
            @py_assert3 = @py_assert1.args
            @py_assert6 = isinstance(@py_assert3, str)
            if @py_assert6 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_format.py', lineno=178)
            if not @py_assert6:
                @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py4)s\n{%(py4)s = %(py2)s.args\n}, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py7':@pytest_ar._saferepr(@py_assert6)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert6 = None

    def testFuturePrintStatementWithoutParensWarning(self):
        code = "from __future__ import print_function\nprint('Hello world!')\n"
        tree = astroid.parse(code)
        with self.assertNoMessages():
            self.checker.process_module(tree)
            self.checker.process_tokens(_tokenize_str(code))

    def testKeywordParensFalsePositive(self):
        self.checker._keywords_with_parens = set()
        code = "if 'bar' in (DICT or {}):"
        with self.assertNoMessages():
            self.checker._check_keyword_parentheses((_tokenize_str(code)), start=2)


class TestCheckSpace(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testParenthesesGood(self):
        good_cases = [
         '(a)\n', '(a * (b + c))\n', '(#\n    a)\n']
        with self.assertNoMessages():
            for code in good_cases:
                self.checker.process_tokens(_tokenize_str(code))

    def testParenthesesBad(self):
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'after', 'bracket', '( a)\n^'))):
            self.checker.process_tokens(_tokenize_str('( a)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'before', 'bracket', '(a )\n   ^'))):
            self.checker.process_tokens(_tokenize_str('(a )\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'before', 'bracket', 'foo (a)\n    ^'))):
            self.checker.process_tokens(_tokenize_str('foo (a)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'before', 'bracket', '{1: 2} [1]\n       ^'))):
            self.checker.process_tokens(_tokenize_str('{1: 2} [1]\n'))

    def testTrailingCommaGood(self):
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('(a, )\n'))
            self.checker.process_tokens(_tokenize_str('(a,)\n'))
        self.checker.config.no_space_check = []
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('(a,)\n'))

    @set_config(no_space_check=[])
    def testTrailingCommaBad(self):
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'before', 'bracket', '(a, )\n    ^'))):
            self.checker.process_tokens(_tokenize_str('(a, )\n'))

    def testComma(self):
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'before', 'comma', '(a , b)\n   ^'))):
            self.checker.process_tokens(_tokenize_str('(a , b)\n'))

    def testSpacesAllowedInsideSlices(self):
        good_cases = ['[a:b]\n', '[a : b]\n', '[a : ]\n', '[:a]\n', '[:]\n', '[::]\n']
        with self.assertNoMessages():
            for code in good_cases:
                self.checker.process_tokens(_tokenize_str(code))

    def testKeywordSpacingGood(self):
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('foo(foo=bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: int = bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: module.classname = bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: Dict[int, str] = bar)\n'))
            self.checker.process_tokens(_tokenize_str("foo(foo: 'int' = bar)\n"))
            self.checker.process_tokens(_tokenize_str("foo(foo: Dict[int, 'str'] = bar)\n"))
            self.checker.process_tokens(_tokenize_str('lambda x=1: x\n'))

    def testKeywordSpacingBad(self):
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'before', 'keyword argument assignment', '(foo =bar)\n     ^'))):
            self.checker.process_tokens(_tokenize_str('(foo =bar)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'after', 'keyword argument assignment', '(foo= bar)\n    ^'))):
            self.checker.process_tokens(_tokenize_str('(foo= bar)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('No', 'allowed', 'around', 'keyword argument assignment', '(foo = bar)\n     ^'))):
            self.checker.process_tokens(_tokenize_str('(foo = bar)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'before', 'keyword argument assignment',
                '(foo: int= bar)\n         ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: int= bar)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'after', 'keyword argument assignment',
                '(foo: int =bar)\n          ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: int =bar)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'around', 'keyword argument assignment',
                '(foo: int=bar)\n         ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: int=bar)\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'around', 'keyword argument assignment',
                '(foo: List[int]=bar)\n               ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: List[int]=bar)\n'))
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('(arg: Tuple[\n    int, str] = None):\n'))

    def testOperatorSpacingGood(self):
        good_cases = [
         'a = b\na < b\na\n< b\n']
        with self.assertNoMessages():
            for code in good_cases:
                self.checker.process_tokens(_tokenize_str(code))

    def testOperatorSpacingBad(self):
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'before', 'comparison', 'a< b\n ^'))):
            self.checker.process_tokens(_tokenize_str('a< b\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'after', 'comparison', 'a <b\n  ^'))):
            self.checker.process_tokens(_tokenize_str('a <b\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'around', 'comparison', 'a<b\n ^'))):
            self.checker.process_tokens(_tokenize_str('a<b\n'))
        with self.assertAddsMessages(Message('bad-whitespace',
          line=1,
          args=('Exactly one', 'required', 'around', 'comparison', 'a<  b\n ^'))):
            self.checker.process_tokens(_tokenize_str('a<  b\n'))

    def testValidTypingAnnotationEllipses(self):
        """Make sure ellipses in function typing annotation
        doesn't cause a false positive bad-whitespace message"""
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('def foo(t: Tuple[str, ...] = None):\n'))

    def testEmptyLines(self):
        self.checker.config.no_space_check = []
        with self.assertAddsMessages(Message('trailing-whitespace', line=2)):
            self.checker.process_tokens(_tokenize_str('a = 1\n \nb = 2\n'))
        with self.assertAddsMessages(Message('trailing-whitespace', line=2)):
            self.checker.process_tokens(_tokenize_str('a = 1\n\t\nb = 2\n'))
        with self.assertAddsMessages(Message('trailing-whitespace', line=2)):
            self.checker.process_tokens(_tokenize_str('a = 1\n\x0b\nb = 2\n'))
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n\x0c\nb = 2\n'))
        self.checker.config.no_space_check = ['empty-line']
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n \nb = 2\n'))
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n\t\nb = 2\n'))
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n\x0b\nb = 2\n'))

    def test_encoding_token(self):
        """Make sure the encoding token doesn't change the checker's behavior

        _tokenize_str doesn't produce an encoding token, but
        reading a file does
        """
        with self.assertNoMessages():
            encoding_token = tokenize.TokenInfo(tokenize.ENCODING, 'utf-8', (0, 0), (0,
                                                                                     0), '')
            tokens = [
             encoding_token] + _tokenize_str('if (\n        None):\n    pass\n')
            self.checker.process_tokens(tokens)


def test_disable_global_option_end_of_line():
    """
    Test for issue with disabling tokenizer messages
    that extend beyond the scope of the ast tokens
    """
    file_ = tempfile.NamedTemporaryFile('w', delete=False)
    with file_:
        file_.write('\nmylist = [\n    None\n        ]\n    ')
    try:
        linter = lint.PyLinter()
        checker = FormatChecker(linter)
        linter.register_checker(checker)
        args = linter.load_command_line_configuration([
         file_.name, '-d', 'bad-continuation'])
        myreporter = reporters.CollectingReporter()
        linter.set_reporter(myreporter)
        linter.check(args)
        @py_assert1 = myreporter.messages
        @py_assert3 = not @py_assert1
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_format.py', lineno=520)
        if not @py_assert3:
            @py_format4 = 'assert not %(py2)s\n{%(py2)s = %(py0)s.messages\n}' % {'py0':@pytest_ar._saferepr(myreporter) if 'myreporter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(myreporter) else 'myreporter',  'py2':@pytest_ar._saferepr(@py_assert1)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert1 = @py_assert3 = None
    finally:
        os.remove(file_.name)