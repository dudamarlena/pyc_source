# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_check_yields_docs.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 12270 bytes
"""Unit tests for the yield documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""
from __future__ import absolute_import, division, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid
from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase, Message, set_config

class TestDocstringCheckerYield(CheckerTestCase):
    __doc__ = 'Tests for pylint_plugin.RaiseDocChecker'
    CHECKER_CLASS = DocstringParameterChecker

    def test_ignores_no_docstring(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            yield False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    @set_config(accept_no_yields_doc=False)
    def test_warns_no_docstring(self):
        node = astroid.extract_node('\n        def my_func(self):\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node), Message(msg_id='missing-yield-type-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_ignores_unknown_style(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring."""\n            yield False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_warn_partial_sphinx_yields(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: Always False\n            """\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-type-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warn_partial_sphinx_yields_type(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :rtype: bool\n            """\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warn_missing_sphinx_yields(self):
        node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            :param doc_type: Sphinx\n            :type doc_type: str\n            """\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node), Message(msg_id='missing-yield-type-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warn_partial_google_yields(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                Always False\n            """\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-type-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warn_partial_google_yields_type(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                bool:\n            """\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warn_missing_google_yields(self):
        node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            Parameters:\n                doc_type (str): Google\n            """\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node), Message(msg_id='missing-yield-type-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warn_missing_numpy_yields(self):
        node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            Arguments\n            ---------\n            doc_type : str\n                Numpy\n            """\n            yield False\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node), Message(msg_id='missing-yield-type-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_find_sphinx_yields(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :return: Always False\n            :rtype: bool\n            """\n            yield False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_find_google_yields(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                bool: Always False\n            """\n            yield False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_find_numpy_yields(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields\n            -------\n            bool\n                Always False\n            """\n            yield False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_finds_sphinx_yield_custom_class(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: An object\n            :rtype: :class:`mymodule.Class`\n            """\n            yield mymodule.Class() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_finds_google_yield_custom_class(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                mymodule.Class: An object\n            """\n            yield mymodule.Class() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_finds_numpy_yield_custom_class(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields\n            -------\n                mymodule.Class\n                    An object\n            """\n            yield mymodule.Class() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_finds_sphinx_yield_list_of_custom_class(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: An object\n            :rtype: list(:class:`mymodule.Class`)\n            """\n            yield [mymodule.Class()] #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_finds_google_yield_list_of_custom_class(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                list(:class:`mymodule.Class`): An object\n            """\n            yield [mymodule.Class()] #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_finds_numpy_yield_list_of_custom_class(self):
        yield_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields\n            -------\n                list(:class:`mymodule.Class`)\n                    An object\n            """\n            yield [mymodule.Class()] #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)

    def test_warns_sphinx_yield_list_of_custom_class_without_description(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :rtype: list(:class:`mymodule.Class`)\n            """\n            yield [mymodule.Class()]\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warns_google_yield_list_of_custom_class_without_description(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                list(:class:`mymodule.Class`):\n            """\n            yield [mymodule.Class()]\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_warns_numpy_yield_list_of_custom_class_without_description(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields\n            -------\n                list(:class:`mymodule.Class`)\n            """\n            yield [mymodule.Class()]\n        ')
        yield_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-yield-doc', node=node)):
            self.checker.visit_yield(yield_node)

    def test_ignores_google_redundant_yield_doc_multiple_yields(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                int or None: One, or sometimes None.\n            """\n            if a_func():\n                yield None\n            yield 1\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_numpy_redundant_yield_doc_multiple_yields(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields\n            -------\n                int\n                    One\n                None\n                    Sometimes\n            """\n            if a_func():\n                yield None\n            yield 1\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_yield_doc_return(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields:\n                int: One\n            """\n            return 1\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-yields-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_yield_doc_return(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Yields\n            -------\n                int\n                    One\n            """\n            return 1\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-yields-doc', node=node)):
            self.checker.visit_functiondef(node)