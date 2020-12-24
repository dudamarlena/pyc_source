# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_checker.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 6047 bytes
import ast, sys
from pyflakes import checker
from pyflakes.test.harness import TestCase, skipIf

class TypeableVisitorTests(TestCase):
    __doc__ = '\n    Tests of L{_TypeableVisitor}\n    '

    @staticmethod
    def _run_visitor(s):
        """
        Run L{_TypeableVisitor} on the parsed source and return the visitor.
        """
        tree = ast.parse(s)
        visitor = checker._TypeableVisitor()
        visitor.visit(tree)
        return visitor

    def test_node_types(self):
        """
        Test that the typeable node types are collected
        """
        visitor = self._run_visitor('x = 1  # assignment\nfor x in range(1): pass  # for loop\ndef f(): pass  # function definition\nwith a as b: pass  # with statement\n')
        self.assertEqual(visitor.typeable_lines, [1, 2, 3, 4])
        self.assertIsInstance(visitor.typeable_nodes[1], ast.Assign)
        self.assertIsInstance(visitor.typeable_nodes[2], ast.For)
        self.assertIsInstance(visitor.typeable_nodes[3], ast.FunctionDef)
        self.assertIsInstance(visitor.typeable_nodes[4], ast.With)

    def test_visitor_recurses(self):
        """
        Test the common pitfall of missing `generic_visit` in visitors by
        ensuring that nested nodes are reported
        """
        visitor = self._run_visitor('def f():\n    x = 1\n')
        self.assertEqual(visitor.typeable_lines, [1, 2])
        self.assertIsInstance(visitor.typeable_nodes[1], ast.FunctionDef)
        self.assertIsInstance(visitor.typeable_nodes[2], ast.Assign)

    @skipIf(sys.version_info < (3, 5), 'async syntax introduced in py35')
    def test_py35_node_types(self):
        """
        Test that the PEP 492 node types are collected
        """
        visitor = self._run_visitor('async def f():  # async def\n    async for x in y:  pass  # async for\n    async with a as b: pass  # async with\n')
        self.assertEqual(visitor.typeable_lines, [1, 2, 3])
        self.assertIsInstance(visitor.typeable_nodes[1], ast.AsyncFunctionDef)
        self.assertIsInstance(visitor.typeable_nodes[2], ast.AsyncFor)
        self.assertIsInstance(visitor.typeable_nodes[3], ast.AsyncWith)

    def test_last_node_wins(self):
        """
        Test that when two typeable nodes are present on a line, the last
        typeable one wins.
        """
        visitor = self._run_visitor('x = 1; y = 1')
        self.assertEqual(visitor.typeable_lines, [1, 1])
        self.assertEqual(visitor.typeable_nodes[1].targets[0].id, 'y')


class CollectTypeCommentsTests(TestCase):
    __doc__ = '\n    Tests of L{_collect_type_comments}\n    '

    @staticmethod
    def _collect(s):
        """
        Run L{_collect_type_comments} on the parsed source and return the
        mapping from nodes to comments.  The return value is converted to
        a set: {(node_type, tuple of comments), ...}
        """
        tree = ast.parse(s)
        tokens = checker.make_tokens(s)
        ret = checker._collect_type_comments(tree, tokens)
        return {(type(k), tuple(s for _, s in v)) for k, v in ret.items()}

    def test_bytes(self):
        """
        Test that the function works for binary source
        """
        ret = self._collect(b'x = 1  # type: int')
        self.assertSetEqual(ret, {(ast.Assign, ('# type: int', ))})

    def test_text(self):
        """
        Test that the function works for text source
        """
        ret = self._collect('x = 1  # type: int')
        self.assertEqual(ret, {(ast.Assign, ('# type: int', ))})

    def test_non_type_comment_ignored(self):
        """
        Test that a non-type comment is ignored
        """
        ret = self._collect('x = 1  # noqa')
        self.assertSetEqual(ret, set())

    def test_type_comment_before_typeable(self):
        """
        Test that a type comment before something typeable is ignored.
        """
        ret = self._collect('# type: int\nx = 1')
        self.assertSetEqual(ret, set())

    def test_type_ignore_comment_ignored(self):
        """
        Test that `# type: ignore` comments are not collected.
        """
        ret = self._collect('x = 1  # type: ignore')
        self.assertSetEqual(ret, set())

    def test_type_ignore_with_other_things_ignored(self):
        """
        Test that `# type: ignore` comments with more content are also not
        collected.
        """
        ret = self._collect('x = 1  # type: ignore # noqa')
        self.assertSetEqual(ret, set())
        ret = self._collect('x = 1  #type:ignore#noqa')
        self.assertSetEqual(ret, set())

    def test_type_comment_with_extra_still_collected(self):
        ret = self._collect('x = 1  # type: int  # noqa')
        self.assertSetEqual(ret, {(ast.Assign, ('# type: int  # noqa', ))})

    def test_type_comment_without_whitespace(self):
        ret = self._collect('x = 1 #type:int')
        self.assertSetEqual(ret, {(ast.Assign, ('#type:int', ))})

    def test_type_comment_starts_with_word_ignore(self):
        ret = self._collect('x = 1 # type: ignore[T]')
        self.assertSetEqual(ret, {(ast.Assign, ('# type: ignore[T]', ))})

    def test_last_node_wins(self):
        """
        Test that when two typeable nodes are present on a line, the last
        typeable one wins.
        """
        ret = self._collect('def f(): x = 1  # type: int')
        self.assertSetEqual(ret, {(ast.Assign, ('# type: int', ))})

    def test_function_def_assigned_comments(self):
        """
        Test that type comments for function arguments are all attributed to
        the function definition.
        """
        ret = self._collect('def f(\n        a,  # type: int\n        b,  # type: str\n):\n    # type: (...) -> None\n    pass\n')
        expected = {
         (
          ast.FunctionDef,
          ('# type: int', '# type: str', '# type: (...) -> None'))}
        self.assertSetEqual(ret, expected)