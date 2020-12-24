# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_imports.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 4334 bytes
"""Unit tests for the imports checker."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, astroid
from pylint.checkers import imports
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, Message, set_config
REGR_DATA = os.path.join(os.path.dirname(__file__), 'regrtest_data', '')

class TestImportsChecker(CheckerTestCase):
    CHECKER_CLASS = imports.ImportsChecker

    @set_config(ignored_modules=('external_module', 'fake_module.submodule', 'foo',
                                 'bar'))
    def test_import_error_skipped(self):
        """Make sure that imports do not emit an 'import-error' when the
        module is configured to be ignored."""
        node = astroid.extract_node('\n        from external_module import anything\n        ')
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)
        node = astroid.extract_node('\n        from external_module.another_module import anything\n        ')
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)
        node = astroid.extract_node('\n        import external_module\n        ')
        with self.assertNoMessages():
            self.checker.visit_import(node)
        node = astroid.extract_node('\n        from fake_module.submodule import anything\n        ')
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)
        node = astroid.extract_node('\n        from fake_module.submodule.deeper import anything\n        ')
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)
        node = astroid.extract_node('\n        import foo, bar\n        ')
        msg = Message('multiple-imports', node=node, args='foo, bar')
        with self.assertAddsMessages(msg):
            self.checker.visit_import(node)
        node = astroid.extract_node('\n        import foo\n        import bar\n        ')
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_reimported_same_line(self):
        """
        Test that duplicate imports on single line raise 'reimported'.
        """
        node = astroid.extract_node('from time import sleep, sleep, time')
        msg = Message(msg_id='reimported', node=node, args=('sleep', 1))
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(node)

    def test_relative_beyond_top_level(self):
        module = astroid.MANAGER.ast_from_module_name('beyond_top', REGR_DATA)
        import_from = module.body[0]
        msg = Message(msg_id='relative-beyond-top-level', node=import_from)
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[1])
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[2].body[0])

    def test_wildcard_import_init(self):
        module = astroid.MANAGER.ast_from_module_name('init_wildcard', REGR_DATA)
        import_from = module.body[0]
        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    def test_wildcard_import_non_init(self):
        module = astroid.MANAGER.ast_from_module_name('wildcard', REGR_DATA)
        import_from = module.body[0]
        msg = Message(msg_id='wildcard-import',
          node=import_from,
          args='empty',
          confidence=UNDEFINED)
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)