# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_stdlib.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 3749 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, contextlib, astroid
from pylint.checkers import stdlib
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, Message

@contextlib.contextmanager
def _add_transform(manager, node, transform, predicate=None):
    manager.register_transform(node, transform, predicate)
    try:
        yield
    finally:
        manager.unregister_transform(node, transform, predicate)


class TestStdlibChecker(CheckerTestCase):
    CHECKER_CLASS = stdlib.StdlibChecker

    def test_deprecated_no_qname_on_unexpected_nodes(self):

        def infer_func(node, context=None):
            new_node = astroid.AssignAttr()
            new_node.parent = node
            yield new_node

        manager = astroid.MANAGER
        transform = astroid.inference_tip(infer_func)
        with _add_transform(manager, astroid.Name, transform):
            node = astroid.extract_node('\n            call_something()\n            ')
            with self.assertNoMessages():
                self.checker.visit_call(node)

    def test_copy_environ(self):
        node = astroid.extract_node('\n        import copy, os\n        copy.copy(os.environ)\n        ')
        with self.assertAddsMessages(Message(msg_id='shallow-copy-environ', node=node, confidence=UNDEFINED)):
            self.checker.visit_call(node)

    def test_copy_environ_hidden(self):
        node = astroid.extract_node('\n        from copy import copy as test_cp\n        import os as o\n        test_cp(o.environ)\n        ')
        with self.assertAddsMessages(Message(msg_id='shallow-copy-environ', node=node, confidence=UNDEFINED)):
            self.checker.visit_call(node)

    def test_copy_dict(self):
        node = astroid.extract_node('\n        import copy\n        test_dict = {}\n        copy.copy(test_dict)\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_copy_uninferable(self):
        node = astroid.extract_node('\n        import copy\n        from missing_library import MissingObject\n        copy.copy(MissingObject)\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_deepcopy_environ(self):
        node = astroid.extract_node('\n        import copy, os\n        copy.deepcopy(os.environ)\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(node)