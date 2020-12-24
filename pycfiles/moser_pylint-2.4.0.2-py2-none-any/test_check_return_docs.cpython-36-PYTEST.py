# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_check_return_docs.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 18624 bytes
"""Unit tests for the return documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""
from __future__ import absolute_import, division, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid
from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase, Message, set_config

class TestDocstringCheckerReturn(CheckerTestCase):
    __doc__ = 'Tests for pylint_plugin.RaiseDocChecker'
    CHECKER_CLASS = DocstringParameterChecker

    def test_ignores_no_docstring(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            return False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    @set_config(accept_no_return_doc=False)
    def test_warns_no_docstring(self):
        node = astroid.extract_node('\n        def my_func(self):\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node), Message(msg_id='missing-return-type-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_ignores_unknown_style(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring."""\n            return False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_warn_partial_sphinx_returns(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: Always False\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-type-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_sphinx_returns_annotations(self):
        node = astroid.extract_node('\n        def my_func(self) -> bool:\n            """This is a docstring.\n\n            :returns: Always False\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_sphinx_missing_return_type_with_annotations(self):
        node = astroid.extract_node('\n           def my_func(self) -> bool:\n               """This is a docstring.\n\n               :returns: Always False\n               """\n               return False\n           ')
        return_node = node.body[0]
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_warn_partial_sphinx_returns_type(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :rtype: bool\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_sphinx_returns(self):
        node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            :param doc_type: Sphinx\n            :type doc_type: str\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node), Message(msg_id='missing-return-type-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warn_partial_google_returns(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                Always False\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-type-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warn_partial_google_returns_type(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                bool:\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_google_returns(self):
        node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            Parameters:\n                doc_type (str): Google\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node), Message(msg_id='missing-return-type-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warn_partial_numpy_returns_type(self):
        node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            Arguments\n            ---------\n            doc_type : str\n                Numpy\n\n            Returns\n            -------\n            bool\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warn_missing_numpy_returns(self):
        node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            Arguments\n            ---------\n            doc_type : str\n                Numpy\n            """\n            return False\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node), Message(msg_id='missing-return-type-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_find_sphinx_returns(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :return: Always False\n            :rtype: bool\n            """\n            return False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_google_returns(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                bool: Always False\n            """\n            return False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_numpy_returns(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n            bool\n                Always False\n            """\n            return False #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_find_numpy_returns_with_of(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n            :obj:`list` of :obj:`str`\n                List of strings\n            """\n            return ["hi", "bye"] #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_sphinx_return_none(self):
        return_node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            :param doc_type: Sphinx\n            :type doc_type: str\n            """\n            return #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_google_return_none(self):
        return_node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            Args:\n                doc_type (str): Google\n            """\n            return #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_ignores_numpy_return_none(self):
        return_node = astroid.extract_node('\n        def my_func(self, doc_type):\n            """This is a docstring.\n\n            Arguments\n            ---------\n            doc_type : str\n                Numpy\n            """\n            return #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_sphinx_return_custom_class(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: An object\n            :rtype: :class:`mymodule.Class`\n            """\n            return mymodule.Class() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_google_return_custom_class(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                mymodule.Class: An object\n            """\n            return mymodule.Class() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_numpy_return_custom_class(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n                mymodule.Class\n                    An object\n            """\n            return mymodule.Class() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_sphinx_return_list_of_custom_class(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: An object\n            :rtype: list(:class:`mymodule.Class`)\n            """\n            return [mymodule.Class()] #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_google_return_list_of_custom_class(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                list(:class:`mymodule.Class`): An object\n            """\n            return [mymodule.Class()] #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_finds_numpy_return_list_of_custom_class(self):
        return_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n                list(:class:`mymodule.Class`)\n                    An object\n            """\n            return [mymodule.Class()] #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_return(return_node)

    def test_warns_sphinx_return_list_of_custom_class_without_description(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :rtype: list(:class:`mymodule.Class`)\n            """\n            return [mymodule.Class()]\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warns_google_return_list_of_custom_class_without_description(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                list(:class:`mymodule.Class`):\n            """\n            return [mymodule.Class()]\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warns_numpy_return_list_of_custom_class_without_description(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n                list(:class:`mymodule.Class`)\n            """\n            return [mymodule.Class()]\n        ')
        return_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-return-doc', node=node)):
            self.checker.visit_return(return_node)

    def test_warns_sphinx_redundant_return_doc(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: One\n            """\n            return None\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_warns_sphinx_redundant_rtype_doc(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :rtype: int\n            """\n            return None\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_return_doc(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                One\n            """\n            return None\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_rtype_doc(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                int:\n            """\n            return None\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_return_doc(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n                int\n                    One\n            """\n            return None\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_rtype_doc(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n                int\n            """\n            return None\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_ignores_sphinx_redundant_return_doc_multiple_returns(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :returns: One\n            :rtype: int\n\n            :returns: None sometimes\n            :rtype: None\n            """\n            if a_func():\n                return None\n            return 1\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_google_redundant_return_doc_multiple_returns(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                int or None: One, or sometimes None.\n            """\n            if a_func():\n                return None\n            return 1\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_numpy_redundant_return_doc_multiple_returns(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n                int\n                    One\n                None\n                    Sometimes\n            """\n            if a_func():\n                return None\n            return 1\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignore_sphinx_redundant_return_doc_yield(self):
        node = astroid.extract_node('\n        def my_func_with_yield(self):\n            """This is a docstring.\n\n            :returns: One\n            :rtype: generator\n            """\n            for value in range(3):\n                yield value\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_return_doc_yield(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns:\n                int: One\n            """\n            yield 1\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_return_doc_yield(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Returns\n            -------\n                int\n                    One\n            """\n            yield 1\n        ')
        with self.assertAddsMessages(Message(msg_id='redundant-returns-doc', node=node)):
            self.checker.visit_functiondef(node)