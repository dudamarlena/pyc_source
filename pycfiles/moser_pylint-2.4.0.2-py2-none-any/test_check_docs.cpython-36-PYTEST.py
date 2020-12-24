# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_check_docs.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 65581 bytes
"""Unit tests for the pylint checkers in :mod:`pylint.extensions.check_docs`,
in particular the parameter documentation checker `DocstringChecker`
"""
from __future__ import absolute_import, division, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, astroid, pytest
from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase, Message, set_config

class TestParamDocChecker(CheckerTestCase):
    __doc__ = 'Tests for pylint_plugin.ParamDocChecker'
    CHECKER_CLASS = DocstringParameterChecker
    CONFIG = {'accept_no_param_doc': False}

    def test_missing_func_params_in_sphinx_docstring(self):
        """Example of a function with missing Sphinx parameter documentation in
        the docstring
        """
        node = astroid.extract_node("\n        def function_foo(x, y, z):\n            '''docstring ...\n\n            :param x: bla\n\n            :param int z: bar\n            '''\n            pass\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('y', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', ))):
            self.checker.visit_functiondef(node)

    def test_missing_func_params_in_google_docstring(self):
        """Example of a function with missing Google style parameter
        documentation in the docstring
        """
        node = astroid.extract_node("\n        def function_foo(x, y, z):\n            '''docstring ...\n\n            Args:\n                x: bla\n                z (int): bar\n\n            some other stuff\n            '''\n            pass\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('y', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', ))):
            self.checker.visit_functiondef(node)

    def test_missing_func_params_with_annotations_in_google_docstring(self):
        """Example of a function with missing Google style parameter
        documentation in the docstring.
        """
        node = astroid.extract_node("\n        def function_foo(x: int, y: bool, z):\n            '''docstring ...\n\n            Args:\n                x: bla\n                y: blah blah\n                z (int): bar\n\n            some other stuff\n            '''\n            pass\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_default_arg_with_annotations_in_google_docstring(self):
        """Example of a function with missing Google style parameter
        documentation in the docstring.
        """
        node = astroid.extract_node("\n        def function_foo(x: int, y: bool, z: int = 786):\n            '''docstring ...\n\n            Args:\n                x: bla\n                y: blah blah\n                z: bar\n\n            some other stuff\n            '''\n            pass\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_missing_func_params_with_partial_annotations_in_google_docstring(self):
        """Example of a function with missing Google style parameter
        documentation in the docstring.
        """
        node = astroid.extract_node("\n        def function_foo(x, y: bool, z):\n            '''docstring ...\n\n            Args:\n                x: bla\n                y: blah blah\n                z (int): bar\n\n            some other stuff\n            '''\n            pass\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-type-doc',
          node=node,
          args=('x', ))):
            self.checker.visit_functiondef(node)

    def test_non_builtin_annotations_in_google_docstring(self):
        """Example of a function with missing Google style parameter
        documentation in the docstring.
        """
        node = astroid.extract_node("\n        def area(bottomleft: Point, topright: Point) -> float:\n            '''Calculate area of fake rectangle.\n                Args:\n                    bottomleft: bottom left point of rectangle\n                    topright: top right point of rectangle\n            '''\n            pass\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_non_builtin_annotations_for_returntype_in_google_docstring(self):
        """Example of a function with missing Google style parameter
        documentation in the docstring.
        """
        node = astroid.extract_node("\n        def get_midpoint(bottomleft: Point, topright: Point) -> Point:\n            '''Calculate midpoint of fake rectangle.\n                Args:\n                    bottomleft: bottom left point of rectangle\n                    topright: top right point of rectangle\n            '''\n            pass\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_func_params_and_keyword_params_in_google_docstring(self):
        """Example of a function with Google style parameter splitted
        in Args and Keyword Args in the docstring
        """
        node = astroid.extract_node("\n        def my_func(this, other, that=True):\n            '''Prints this, other and that\n\n                Args:\n                    this (str): Printed first\n                    other (int): Other args\n\n                Keyword Args:\n                    that (bool): Printed second\n            '''\n            print(this, that, other)\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_func_params_and_wrong_keyword_params_in_google_docstring(self):
        """Example of a function with Google style parameter splitted
        in Args and Keyword Args in the docstring but with wrong keyword args
        """
        node = astroid.extract_node("\n        def my_func(this, other, that=True):\n            '''Prints this, other and that\n\n                Args:\n                    this (str): Printed first\n                    other (int): Other args\n\n                Keyword Args:\n                    these (bool): Printed second\n            '''\n            print(this, that, other)\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('that', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('that', )), Message(msg_id='differing-param-doc',
          node=node,
          args=('these', )), Message(msg_id='differing-type-doc',
          node=node,
          args=('these', ))):
            self.checker.visit_functiondef(node)

    def test_missing_func_params_in_numpy_docstring(self):
        """Example of a function with missing NumPy style parameter
        documentation in the docstring
        """
        node = astroid.extract_node("\n        def function_foo(x, y, z):\n            '''docstring ...\n\n            Parameters\n            ----------\n            x:\n                bla\n            z: int\n                bar\n\n            some other stuff\n            '''\n            pass\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('y', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', ))):
            self.checker.visit_functiondef(node)

    @set_config(accept_no_param_doc=True)
    def test_tolerate_no_param_documentation_at_all(self):
        """Example of a function with no parameter documentation at all

        No error message is emitted.
        """
        node = astroid.extract_node("\n        def function_foo(x, y):\n            '''docstring ...\n\n            missing parameter documentation'''\n            pass\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_don_t_tolerate_no_param_documentation_at_all(self):
        """Example of a function with no parameter documentation at all

        Missing documentation error message is emitted.
        """
        node = astroid.extract_node("\n        def function_foo(x, y):\n            '''docstring ...\n\n            missing parameter documentation'''\n            pass\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('x, y', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', ))):
            self.checker.visit_functiondef(node)

    def test_see_tolerate_no_param_documentation_at_all(self):
        """Example for the usage of "For the parameters, see"
        to suppress missing-param warnings.
        """
        node = astroid.extract_node("\n        def function_foo(x, y):\n            '''docstring ...\n\n            For the parameters, see :func:`blah`\n            '''\n            pass\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def _visit_methods_of_class(self, node):
        """Visit all methods of a class node

        :param node: class node
        :type node: :class:`astroid.scoped_nodes.Class`
        """
        for body_item in node.body:
            if isinstance(body_item, astroid.FunctionDef) and hasattr(body_item, 'name'):
                self.checker.visit_functiondef(body_item)

    def test_missing_method_params_in_sphinx_docstring(self):
        """Example of a class method with missing parameter documentation in
        the Sphinx style docstring
        """
        node = astroid.extract_node("\n        class Foo(object):\n            def method_foo(self, x, y):\n                '''docstring ...\n\n                missing parameter documentation\n\n                :param x: bla\n                '''\n                pass\n        ")
        method_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=method_node,
          args=('y', )), Message(msg_id='missing-type-doc',
          node=method_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_missing_method_params_in_google_docstring(self):
        """Example of a class method with missing parameter documentation in
        the Google style docstring
        """
        node = astroid.extract_node("\n        class Foo(object):\n            def method_foo(self, x, y):\n                '''docstring ...\n\n                missing parameter documentation\n\n                Args:\n                    x: bla\n                '''\n                pass\n        ")
        method_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=method_node,
          args=('y', )), Message(msg_id='missing-type-doc',
          node=method_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_missing_method_params_in_numpy_docstring(self):
        """Example of a class method with missing parameter documentation in
        the Numpy style docstring
        """
        node = astroid.extract_node("\n        class Foo(object):\n            def method_foo(self, x, y):\n                '''docstring ...\n\n                missing parameter documentation\n\n                Parameters\n                ----------\n                x:\n                    bla\n                '''\n                pass\n        ")
        method_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=method_node,
          args=('y', )), Message(msg_id='missing-type-doc',
          node=method_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_existing_func_params_in_sphinx_docstring(self):
        """Example of a function with correctly documented parameters and
        return values (Sphinx style)
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg, zarg, warg):\n            '''function foo ...\n\n            :param xarg: bla xarg\n            :type xarg: int\n\n            :parameter yarg: bla yarg\n            :type yarg: my.qualified.type\n\n            :arg int zarg: bla zarg\n\n            :keyword my.qualified.type warg: bla warg\n\n            :return: sum\n            :rtype: float\n            '''\n            return xarg + yarg\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_existing_func_params_in_google_docstring(self):
        """Example of a function with correctly documented parameters and
        return values (Google style)
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg, zarg, warg):\n            '''function foo ...\n\n            Args:\n                xarg (int): bla xarg\n                yarg (my.qualified.type): bla\n                    bla yarg\n\n                zarg (int): bla zarg\n                warg (my.qualified.type): bla warg\n\n            Returns:\n                float: sum\n            '''\n            return xarg + yarg\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_existing_func_params_in_numpy_docstring(self):
        """Example of a function with correctly documented parameters and
        return values (Numpy style)
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg, zarg, warg):\n            '''function foo ...\n\n            Parameters\n            ----------\n            xarg: int\n                bla xarg\n            yarg: my.qualified.type\n                bla yarg\n\n            zarg: int\n                bla zarg\n            warg: my.qualified.type\n                bla warg\n\n            Returns\n            -------\n            float\n                sum\n            '''\n            return xarg + yarg\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_wrong_name_of_func_params_in_sphinx_docstring(self):
        """Example of functions with inconsistent parameter names in the
        signature and in the Sphinx style documentation
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg, zarg):\n            '''function foo ...\n\n            :param xarg1: bla xarg\n            :type xarg: int\n\n            :param yarg: bla yarg\n            :type yarg1: float\n\n            :param str zarg1: bla zarg\n            '''\n            return xarg + yarg\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('xarg, zarg', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('yarg, zarg', )), Message(msg_id='differing-param-doc',
          node=node,
          args=('xarg1, zarg1', )), Message(msg_id='differing-type-doc',
          node=node,
          args=('yarg1, zarg1', ))):
            self.checker.visit_functiondef(node)
        node = astroid.extract_node("\n        def function_foo(xarg, yarg):\n            '''function foo ...\n\n            :param yarg1: bla yarg\n            :type yarg1: float\n\n            For the other parameters, see bla.\n            '''\n            return xarg + yarg\n        ")
        with self.assertAddsMessages(Message(msg_id='differing-param-doc',
          node=node,
          args=('yarg1', )), Message(msg_id='differing-type-doc',
          node=node,
          args=('yarg1', ))):
            self.checker.visit_functiondef(node)

    def test_wrong_name_of_func_params_in_google_docstring(self):
        """Example of functions with inconsistent parameter names in the
        signature and in the Google style documentation
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg, zarg):\n            '''function foo ...\n\n            Args:\n                xarg1 (int): bla xarg\n                yarg (float): bla yarg\n\n                zarg1 (str): bla zarg\n            '''\n            return xarg + yarg\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('xarg, zarg', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('xarg, zarg', )), Message(msg_id='differing-param-doc',
          node=node,
          args=('xarg1, zarg1', )), Message(msg_id='differing-type-doc',
          node=node,
          args=('xarg1, zarg1', ))):
            self.checker.visit_functiondef(node)
        node = astroid.extract_node("\n        def function_foo(xarg, yarg):\n            '''function foo ...\n\n            Args:\n                yarg1 (float): bla yarg\n\n            For the other parameters, see bla.\n            '''\n            return xarg + yarg\n        ")
        with self.assertAddsMessages(Message(msg_id='differing-param-doc',
          node=node,
          args=('yarg1', )), Message(msg_id='differing-type-doc',
          node=node,
          args=('yarg1', ))):
            self.checker.visit_functiondef(node)

    def test_wrong_name_of_func_params_in_numpy_docstring(self):
        """Example of functions with inconsistent parameter names in the
        signature and in the Numpy style documentation
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg, zarg):\n            '''function foo ...\n\n            Parameters\n            ----------\n            xarg1: int\n                bla xarg\n            yarg: float\n                bla yarg\n\n            zarg1: str\n                bla zarg\n            '''\n            return xarg + yarg\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('xarg, zarg', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('xarg, zarg', )), Message(msg_id='differing-param-doc',
          node=node,
          args=('xarg1, zarg1', )), Message(msg_id='differing-type-doc',
          node=node,
          args=('xarg1, zarg1', ))):
            self.checker.visit_functiondef(node)
        node = astroid.extract_node("\n        def function_foo(xarg, yarg):\n            '''function foo ...\n\n            Parameters\n            ----------\n            yarg1: float\n                bla yarg\n\n            For the other parameters, see bla.\n            '''\n            return xarg + yarg\n        ")
        with self.assertAddsMessages(Message(msg_id='differing-param-doc',
          node=node,
          args=('yarg1', )), Message(msg_id='differing-type-doc',
          node=node,
          args=('yarg1', ))):
            self.checker.visit_functiondef(node)

    def test_see_sentence_for_func_params_in_sphinx_docstring(self):
        """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Sphinx style)
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg):\n            '''function foo ...\n\n            :param yarg: bla yarg\n            :type yarg: float\n\n            For the other parameters, see :func:`bla`\n            '''\n            return xarg + yarg\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_see_sentence_for_func_params_in_google_docstring(self):
        """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Google style)
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg):\n            '''function foo ...\n\n            Args:\n                yarg (float): bla yarg\n\n            For the other parameters, see :func:`bla`\n            '''\n            return xarg + yarg\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_see_sentence_for_func_params_in_numpy_docstring(self):
        """Example for the usage of "For the other parameters, see" to avoid
        too many repetitions, e.g. in functions or methods adhering to a
        given interface (Numpy style)
        """
        node = astroid.extract_node("\n        def function_foo(xarg, yarg):\n            '''function foo ...\n\n            Parameters\n            ----------\n            yarg: float\n                bla yarg\n\n            For the other parameters, see :func:`bla`\n            '''\n            return xarg + yarg\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_constr_params_in_class_sphinx(self):
        """Example of a class with missing constructor parameter documentation
        (Sphinx style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''docstring foo\n\n            :param y: bla\n\n            missing constructor parameter documentation\n            '''\n\n            def __init__(self, x, y):\n                pass\n\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_constr_params_in_class_google(self):
        """Example of a class with missing constructor parameter documentation
        (Google style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''docstring foo\n\n            Args:\n                y: bla\n\n            missing constructor parameter documentation\n            '''\n\n            def __init__(self, x, y):\n                pass\n\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_constr_params_in_class_numpy(self):
        """Example of a class with missing constructor parameter documentation
        (Numpy style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''docstring foo\n\n            Parameters\n            ----------\n            y:\n                bla\n\n            missing constructor parameter documentation\n            '''\n\n            def __init__(self, x, y):\n                pass\n\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_constr_params_and_attributes_in_class_numpy(self):
        """Example of a class with correct constructor parameter documentation
        and an attributes section (Numpy style)
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''\n            Parameters\n            ----------\n            foo : str\n                Something.\n\n            Attributes\n            ----------\n            bar : str\n                Something.\n            '''\n            def __init__(self, foo):\n                self.bar = None\n        ")
        with self.assertNoMessages():
            self._visit_methods_of_class(node)

    def test_constr_params_in_init_sphinx(self):
        """Example of a class with missing constructor parameter documentation
        (Sphinx style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            def __init__(self, x, y):\n                '''docstring foo constructor\n\n                :param y: bla\n\n                missing constructor parameter documentation\n                '''\n\n                pass\n\n        ")
        constructor_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=constructor_node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=constructor_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_constr_params_in_init_google(self):
        """Example of a class with missing constructor parameter documentation
        (Google style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            def __init__(self, x, y):\n                '''docstring foo constructor\n\n                Args:\n                    y: bla\n\n                missing constructor parameter documentation\n                '''\n                pass\n\n        ")
        constructor_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=constructor_node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=constructor_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_constr_params_in_init_numpy(self):
        """Example of a class with missing constructor parameter documentation
        (Numpy style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            def __init__(self, x, y):\n                '''docstring foo constructor\n\n                Parameters\n                ----------\n                y:\n                    bla\n\n                missing constructor parameter documentation\n                '''\n                pass\n\n        ")
        constructor_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=constructor_node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=constructor_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_see_sentence_for_constr_params_in_class(self):
        """Example usage of "For the parameters, see" in class docstring"""
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''docstring foo\n\n            For the parameters, see :func:`bla`\n            '''\n\n            def __init__(self, x, y):\n                '''init'''\n                pass\n\n        ")
        with self.assertNoMessages():
            self._visit_methods_of_class(node)

    def test_see_sentence_for_constr_params_in_init(self):
        """Example usage of "For the parameters, see" in init docstring"""
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''foo'''\n\n            def __init__(self, x, y):\n                '''docstring foo constructor\n\n                For the parameters, see :func:`bla`\n                '''\n                pass\n\n        ")
        with self.assertNoMessages():
            self._visit_methods_of_class(node)

    def test_constr_params_in_class_and_init_sphinx(self):
        """Example of a class with missing constructor parameter documentation
        in both the init docstring and the class docstring
        (Sphinx style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''docstring foo\n\n            :param y: None\n\n            missing constructor parameter documentation\n            '''\n\n            def __init__(self, x, y):\n                '''docstring foo\n\n                :param y: bla\n\n                missing constructor parameter documentation\n                '''\n                pass\n\n        ")
        constructor_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='multiple-constructor-doc',
          node=node,
          args=(
         node.name,)), Message(msg_id='missing-param-doc',
          node=node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', )), Message(msg_id='missing-param-doc',
          node=constructor_node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=constructor_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_constr_params_in_class_and_init_google(self):
        """Example of a class with missing constructor parameter documentation
        in both the init docstring and the class docstring
        (Google style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''docstring foo\n\n            Args:\n                y: bla\n\n            missing constructor parameter documentation\n            '''\n\n            def __init__(self, x, y):\n                '''docstring foo\n\n                Args:\n                    y: bla\n\n                missing constructor parameter documentation\n                '''\n                pass\n\n        ")
        constructor_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='multiple-constructor-doc',
          node=node,
          args=(
         node.name,)), Message(msg_id='missing-param-doc',
          node=node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', )), Message(msg_id='missing-param-doc',
          node=constructor_node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=constructor_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    def test_constr_params_in_class_and_init_numpy(self):
        """Example of a class with missing constructor parameter documentation
        in both the init docstring and the class docstring
        (Numpy style)

        Everything is completely analogous to functions.
        """
        node = astroid.extract_node("\n        class ClassFoo(object):\n            '''docstring foo\n\n            Parameters\n            ----------\n            y:\n                bla\n\n            missing constructor parameter documentation\n            '''\n\n            def __init__(self, x, y):\n                '''docstring foo\n\n                Parameters\n                ----------\n                y:\n                    bla\n\n                missing constructor parameter documentation\n                '''\n                pass\n\n        ")
        constructor_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='multiple-constructor-doc',
          node=node,
          args=(
         node.name,)), Message(msg_id='missing-param-doc',
          node=node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('x, y', )), Message(msg_id='missing-param-doc',
          node=constructor_node,
          args=('x', )), Message(msg_id='missing-type-doc',
          node=constructor_node,
          args=('x, y', ))):
            self._visit_methods_of_class(node)

    @pytest.mark.skipif((sys.version_info[0] != 3), reason='Enabled on Python 3')
    def test_kwonlyargs_are_taken_in_account(self):
        node = astroid.extract_node('\n        def my_func(arg, *, kwonly, missing_kwonly):\n            """The docstring\n\n            :param int arg: The argument.\n            :param bool kwonly: A keyword-arg.\n            """\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('missing_kwonly', )), Message(msg_id='missing-type-doc',
          node=node,
          args=('missing_kwonly', ))):
            self.checker.visit_functiondef(node)

    def test_warns_missing_args_sphinx(self):
        node = astroid.extract_node('\n        def my_func(named_arg, *args):\n            """The docstring\n\n            :param named_arg: Returned\n            :type named_arg: object\n            :returns: Maybe named_arg\n            :rtype: object or None\n            """\n            if args:\n                return named_arg\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('args', ))):
            self.checker.visit_functiondef(node)

    def test_warns_missing_kwargs_sphinx(self):
        node = astroid.extract_node('\n        def my_func(named_arg, **kwargs):\n            """The docstring\n\n            :param named_arg: Returned\n            :type named_arg: object\n            :returns: Maybe named_arg\n            :rtype: object or None\n            """\n            if kwargs:\n                return named_arg\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('kwargs', ))):
            self.checker.visit_functiondef(node)

    def test_warns_missing_args_google(self):
        node = astroid.extract_node('\n        def my_func(named_arg, *args):\n            """The docstring\n\n            Args:\n                named_arg (object): Returned\n\n            Returns:\n                object or None: Maybe named_arg\n            """\n            if args:\n                return named_arg\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('args', ))):
            self.checker.visit_functiondef(node)

    def test_warns_missing_kwargs_google(self):
        node = astroid.extract_node('\n        def my_func(named_arg, **kwargs):\n            """The docstring\n\n            Args:\n                named_arg (object): Returned\n\n            Returns:\n                object or None: Maybe named_arg\n            """\n            if kwargs:\n                return named_arg\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('kwargs', ))):
            self.checker.visit_functiondef(node)

    def test_warns_missing_args_numpy(self):
        node = astroid.extract_node('\n        def my_func(named_arg, *args):\n            """The docstring\n\n            Args\n            ----\n            named_arg : object\n                Returned\n\n            Returns\n            -------\n                object or None\n                    Maybe named_arg\n            """\n            if args:\n                return named_arg\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('args', ))):
            self.checker.visit_functiondef(node)

    def test_warns_missing_kwargs_numpy(self):
        node = astroid.extract_node('\n        def my_func(named_arg, **kwargs):\n            """The docstring\n\n            Args\n            ----\n            named_arg : object\n                Returned\n\n            Returns\n            -------\n                object or None\n                    Maybe named_arg\n            """\n            if kwargs:\n                return named_arg\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-param-doc',
          node=node,
          args=('kwargs', ))):
            self.checker.visit_functiondef(node)

    def test_finds_args_without_type_sphinx(self):
        node = astroid.extract_node('\n        def my_func(named_arg, *args):\n            """The docstring\n\n            :param named_arg: Returned\n            :type named_arg: object\n            :param args: Optional arguments\n            :returns: Maybe named_arg\n            :rtype: object or None\n            """\n            if args:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_kwargs_without_type_sphinx(self):
        node = astroid.extract_node('\n        def my_func(named_arg, **kwargs):\n            """The docstring\n\n            :param named_arg: Returned\n            :type named_arg: object\n            :param kwargs: Keyword arguments\n            :returns: Maybe named_arg\n            :rtype: object or None\n            """\n            if kwargs:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_args_without_type_google(self):
        node = astroid.extract_node('\n        def my_func(named_arg, *args):\n            """The docstring\n\n            Args:\n                named_arg (object): Returned\n                *args: Optional arguments\n\n            Returns:\n                object or None: Maybe named_arg\n            """\n            if args:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_kwargs_without_type_google(self):
        node = astroid.extract_node('\n        def my_func(named_arg, **kwargs):\n            """The docstring\n\n            Args:\n                named_arg (object): Returned\n                **kwargs: Keyword arguments\n\n            Returns:\n                object or None: Maybe named_arg\n            """\n            if kwargs:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_args_without_type_numpy(self):
        node = astroid.extract_node('\n        def my_func(named_arg, *args):\n            """The docstring\n\n            Args\n            ----\n            named_arg : object\n                Returned\n            args :\n                Optional Arguments\n\n            Returns\n            -------\n                object or None\n                    Maybe named_arg\n            """\n            if args:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_args_with_xref_type_google(self):
        node = astroid.extract_node('\n        def my_func(named_arg, **kwargs):\n            """The docstring\n\n            Args:\n                named_arg (`example.value`): Returned\n                **kwargs: Keyword arguments\n\n            Returns:\n                `example.value`: Maybe named_arg\n            """\n            if kwargs:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_args_with_xref_type_numpy(self):
        node = astroid.extract_node('\n        def my_func(named_arg, *args):\n            """The docstring\n\n            Args\n            ----\n            named_arg : `example.value`\n                Returned\n            args :\n                Optional Arguments\n\n            Returns\n            -------\n                `example.value`\n                    Maybe named_arg\n            """\n            if args:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_kwargs_without_type_numpy(self):
        node = astroid.extract_node('\n        def my_func(named_arg, **kwargs):\n            """The docstring\n\n            Args\n            ----\n            named_arg : object\n                Returned\n            kwargs :\n                Keyword arguments\n\n            Returns\n            -------\n                object or None\n                    Maybe named_arg\n            """\n            if kwargs:\n                return named_arg\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    CONTAINER_TYPES = [
     'dict(str,str)',
     'dict[str,str]',
     'tuple(int)',
     'list[tokenize.TokenInfo]']
    COMPLEX_TYPES = CONTAINER_TYPES + [
     'dict(str, str)',
     'dict[str, str]',
     'int or str',
     'tuple(int or str)',
     'tuple(int) or list(int)',
     'tuple(int or str) or list(int or str)']

    @pytest.mark.parametrize('complex_type', COMPLEX_TYPES)
    def test_finds_multiple_types_sphinx(self, complex_type):
        node = astroid.extract_node('\n        def my_func(named_arg):\n            """The docstring\n\n            :param named_arg: Returned\n            :type named_arg: {0}\n\n            :returns: named_arg\n            :rtype: {0}\n            """\n            return named_arg\n        '.format(complex_type))
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    @pytest.mark.parametrize('complex_type', COMPLEX_TYPES)
    def test_finds_multiple_types_google(self, complex_type):
        node = astroid.extract_node('\n        def my_func(named_arg):\n            """The docstring\n\n            Args:\n                named_arg ({0}): Returned\n\n            Returns:\n                {0}: named_arg\n            """\n            return named_arg\n        '.format(complex_type))
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    @pytest.mark.parametrize('complex_type', COMPLEX_TYPES)
    def test_finds_multiple_types_numpy(self, complex_type):
        node = astroid.extract_node('\n        def my_func(named_arg):\n            """The docstring\n\n            Args\n            ----\n            named_arg : {0}\n                Returned\n\n            Returns\n            -------\n                {0}\n                    named_arg\n            """\n            return named_arg\n        '.format(complex_type))
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    @pytest.mark.parametrize('container_type', CONTAINER_TYPES)
    def test_finds_compact_container_types_sphinx(self, container_type):
        node = astroid.extract_node('\n        def my_func(named_arg):\n            """The docstring\n\n            :param {0} named_arg: Returned\n\n            :returns: named_arg\n            :rtype: {0}\n            """\n            return named_arg\n        '.format(container_type))
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_optional_specifier_google(self):
        node = astroid.extract_node('\n        def do_something(param1, param2, param3=(), param4=[], param5=[], param6=True):\n            """Do something.\n\n            Args:\n                param1 (str): Description.\n                param2 (dict(str, int)): Description.\n                param3 (tuple(str), optional): Defaults to empty. Description.\n                param4 (List[str], optional): Defaults to empty. Description.\n                param5 (list[tuple(str)], optional): Defaults to empty. Description.\n                param6 (bool, optional): Defaults to True. Description.\n\n            Returns:\n                int: Description.\n            """\n            return param1, param2, param3, param4, param5, param6\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_optional_specifier_numpy(self):
        node = astroid.extract_node('\n        def do_something(param, param2=\'all\'):\n            """Do something.\n\n            Parameters\n            ----------\n            param : str\n                Description.\n            param2 : str, optional\n                Description (the default is \'all\').\n\n            Returns\n            -------\n            int\n                Description.\n            """\n            return param, param2\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_short_name_exception(self):
        node = astroid.extract_node('\n        from fake_package import BadError\n\n        def do_something(): #@\n            """Do something.\n\n            Raises:\n                ~fake_package.exceptions.BadError: When something bad happened.\n            """\n            raise BadError("A bad thing happened.")\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_missing_raises_from_setter_sphinx(self):
        """Example of a setter having missing raises documentation in
        the Sphinx style docstring of the property
        """
        property_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self): #@\n                '''docstring ...\n\n                :type: int\n                '''\n                return 10\n\n            @foo.setter\n            def foo(self, value):\n                raise AttributeError() #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=property_node,
          args=('AttributeError', ))):
            self.checker.visit_raise(node)

    def test_finds_missing_raises_from_setter_google(self):
        """Example of a setter having missing raises documentation in
        the Google style docstring of the property
        """
        property_node, node = astroid.extract_node('\n        class Foo(object):\n            @property\n            def foo(self): #@\n                \'\'\'int: docstring\n\n                Include a "Raises" section so that this is identified\n                as a Google docstring and not a Numpy docstring.\n\n                Raises:\n                    RuntimeError: Always\n                \'\'\'\n                raise RuntimeError()\n                return 10\n\n            @foo.setter\n            def foo(self, value):\n                raises AttributeError() #@\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=property_node,
          args=('AttributeError', ))):
            self.checker.visit_raise(node)

    def test_finds_missing_raises_from_setter_numpy(self):
        """Example of a setter having missing raises documentation in
        the Numpy style docstring of the property
        """
        property_node, node = astroid.extract_node('\n        class Foo(object):\n            @property\n            def foo(self): #@\n                \'\'\'int: docstring\n\n                Include a "Raises" section so that this is identified\n                as a Numpy docstring and not a Google docstring.\n\n                Raises\n                ------\n                RuntimeError\n                    Always\n                \'\'\'\n                raise RuntimeError()\n                return 10\n\n            @foo.setter\n            def foo(self, value):\n                raises AttributeError() #@\n        ')
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=property_node,
          args=('AttributeError', ))):
            self.checker.visit_raise(node)

    def test_finds_missing_raises_in_setter_sphinx(self):
        """Example of a setter having missing raises documentation in
        its own Sphinx style docstring
        """
        setter_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self):\n                '''docstring ...\n\n                :type: int\n                :raises RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10\n\n            @foo.setter\n            def foo(self, value): #@\n                '''setter docstring ...\n\n                :type: None\n                '''\n                raise AttributeError() #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=setter_node,
          args=('AttributeError', ))):
            self.checker.visit_raise(node)

    def test_finds_missing_raises_from_setter_google(self):
        """Example of a setter having missing raises documentation in
        its own Google style docstring of the property
        """
        setter_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self):\n                '''int: docstring ...\n\n                Raises:\n                    RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10\n\n            @foo.setter\n            def foo(self, value): #@\n                '''setter docstring ...\n\n                Raises:\n                    RuntimeError: Never\n                '''\n                if True:\n                    raise AttributeError() #@\n                raise RuntimeError()\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=setter_node,
          args=('AttributeError', ))):
            self.checker.visit_raise(node)

    def test_finds_missing_raises_from_setter_numpy(self):
        """Example of a setter having missing raises documentation in
        its own Numpy style docstring of the property
        """
        setter_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self):\n                '''int: docstring ...\n\n                Raises\n                ------\n                RuntimeError\n                    Always\n                '''\n                raise RuntimeError()\n                return 10\n\n            @foo.setter\n            def foo(self, value): #@\n                '''setter docstring ...\n\n                Raises\n                ------\n                RuntimeError\n                    Never\n                '''\n                if True:\n                    raise AttributeError() #@\n                raise RuntimeError()\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=setter_node,
          args=('AttributeError', ))):
            self.checker.visit_raise(node)

    def test_finds_property_return_type_sphinx(self):
        """Example of a property having return documentation in
        a Sphinx style docstring
        """
        node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self): #@\n                '''docstring ...\n\n                :type: int\n                '''\n                return 10\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_property_return_type_google(self):
        """Example of a property having return documentation in
        a Google style docstring
        """
        node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self): #@\n                '''int: docstring ...\n\n                Raises:\n                    RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_property_return_type_numpy(self):
        """Example of a property having return documentation in
        a numpy style docstring
        """
        node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self): #@\n                '''int: docstring ...\n\n                Raises\n                ------\n                RuntimeError\n                    Always\n                '''\n                raise RuntimeError()\n                return 10\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_finds_annotation_property_return_type_sphinx(self):
        """Example of a property having missing return documentation in
        a Sphinx style docstring
        """
        property_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self) -> int: #@\n                '''docstring ...\n\n                :raises RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertNoMessages():
            self.checker.visit_return(node)

    def test_finds_missing_property_return_type_sphinx(self):
        """Example of a property having missing return documentation in
        a Sphinx style docstring
        """
        property_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self): #@\n                '''docstring ...\n\n                :raises RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-return-type-doc',
          node=property_node)):
            self.checker.visit_return(node)

    def test_finds_annotation_property_return_type_google(self):
        """Example of a property having return documentation in
        a Google style docstring
        """
        property_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self) -> int: #@\n                '''docstring ...\n\n                Raises:\n                    RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertNoMessages():
            self.checker.visit_return(node)

    def test_finds_missing_property_return_type_google(self):
        """Example of a property having return documentation in
        a Google style docstring
        """
        property_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self): #@\n                '''docstring ...\n\n                Raises:\n                    RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-return-type-doc',
          node=property_node)):
            self.checker.visit_return(node)

    def test_finds_missing_property_return_type_numpy(self):
        """Example of a property having return documentation in
        a numpy style docstring
        """
        property_node, node = astroid.extract_node("\n        class Foo(object):\n            @property\n            def foo(self): #@\n                '''docstring ...\n\n                Raises\n                ------\n                RuntimeError\n                    Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-return-type-doc',
          node=property_node)):
            self.checker.visit_return(node)

    def test_ignores_non_property_return_type_sphinx(self):
        """Example of a class function trying to use `type` as return
        documentation in a Sphinx style docstring
        """
        func_node, node = astroid.extract_node("\n        class Foo(object):\n            def foo(self): #@\n                '''docstring ...\n\n                :type: int\n                '''\n                return 10 #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-return-doc',
          node=func_node), Message(msg_id='missing-return-type-doc',
          node=func_node)):
            self.checker.visit_return(node)

    def test_ignores_non_property_return_type_google(self):
        """Example of a class function trying to use `type` as return
        documentation in a Google style docstring
        """
        func_node, node = astroid.extract_node("\n        class Foo(object):\n            def foo(self): #@\n                '''int: docstring ...\n\n                Raises:\n                    RuntimeError: Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-return-doc',
          node=func_node), Message(msg_id='missing-return-type-doc',
          node=func_node)):
            self.checker.visit_return(node)

    def test_ignores_non_property_return_type_numpy(self):
        """Example of a class function trying to use `type` as return
        documentation in a numpy style docstring
        """
        func_node, node = astroid.extract_node("\n        class Foo(object):\n            def foo(self): #@\n                '''int: docstring ...\n\n                Raises\n                ------\n                RuntimeError\n                    Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-return-doc',
          node=func_node), Message(msg_id='missing-return-type-doc',
          node=func_node)):
            self.checker.visit_return(node)

    def test_non_property_annotation_return_type_numpy(self):
        """Example of a class function trying to use `type` as return
        documentation in a numpy style docstring
        """
        func_node, node = astroid.extract_node("\n        class Foo(object):\n            def foo(self) -> int: #@\n                '''int: docstring ...\n\n                Raises\n                ------\n                RuntimeError\n                    Always\n                '''\n                raise RuntimeError()\n                return 10 #@\n        ")
        with self.assertAddsMessages(Message(msg_id='missing-return-doc',
          node=func_node)):
            self.checker.visit_return(node)

    def test_ignores_return_in_abstract_method_sphinx(self):
        """Example of an abstract method documenting the return type that an
        implementation should return.
        """
        node = astroid.extract_node("\n        import abc\n        class Foo(object):\n            @abc.abstractmethod\n            def foo(self): #@\n                '''docstring ...\n\n                :returns: Ten\n                :rtype: int\n                '''\n                return 10\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_return_in_abstract_method_google(self):
        """Example of an abstract method documenting the return type that an
        implementation should return.
        """
        node = astroid.extract_node("\n        import abc\n        class Foo(object):\n            @abc.abstractmethod\n            def foo(self): #@\n                '''docstring ...\n\n                Returns:\n                    int: Ten\n                '''\n                return 10\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_return_in_abstract_method_numpy(self):
        """Example of an abstract method documenting the return type that an
        implementation should return.
        """
        node = astroid.extract_node("\n        import abc\n        class Foo(object):\n            @abc.abstractmethod\n            def foo(self): #@\n                '''docstring ...\n\n                Returns\n                -------\n                int\n                    Ten\n                '''\n                return 10\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_raise_notimplementederror_sphinx(self):
        """Example of an abstract
        """
        node = astroid.extract_node("\n        class Foo(object):\n            def foo(self, arg): #@\n                '''docstring ...\n\n                :param arg: An argument.\n                :type arg: int\n                '''\n                raise NotImplementedError()\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_return_in_abstract_method_google(self):
        """Example of a method documenting the return type that an
        implementation should return.
        """
        node = astroid.extract_node("\n        class Foo(object):\n            def foo(self, arg): #@\n                '''docstring ...\n\n                Args:\n                    arg (int): An argument.\n                '''\n                raise NotImplementedError()\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_return_in_abstract_method_numpy(self):
        """Example of a method documenting the return type that an
        implementation should return.
        """
        node = astroid.extract_node("\n        class Foo(object):\n            def foo(self, arg): #@\n                '''docstring ...\n\n                Parameters\n                ----------\n                arg : int\n                    An argument.\n                '''\n                raise NotImplementedError()\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)