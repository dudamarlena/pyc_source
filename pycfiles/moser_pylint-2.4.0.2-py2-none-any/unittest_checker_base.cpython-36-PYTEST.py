# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_base.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 17515 bytes
"""Unittest for the base checker."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, re, sys, unittest, astroid
from pylint.checkers import base
from pylint.testutils import CheckerTestCase, Message, set_config

class TestDocstring(CheckerTestCase):
    CHECKER_CLASS = base.DocStringChecker

    def test_missing_docstring_module(self):
        module = astroid.parse('something')
        message = Message('missing-docstring', node=module, args=('module', ))
        with self.assertAddsMessages(message):
            self.checker.visit_module(module)

    def test_missing_docstring_empty_module(self):
        module = astroid.parse('')
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_empty_docstring_module(self):
        module = astroid.parse("''''''")
        message = Message('empty-docstring', node=module, args=('module', ))
        with self.assertAddsMessages(message):
            self.checker.visit_module(module)

    def test_empty_docstring_function(self):
        func = astroid.extract_node('\n        def func(tion):\n           pass')
        message = Message('missing-docstring', node=func, args=('function', ))
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_short_function_no_docstring(self):
        func = astroid.extract_node('\n        def func(tion):\n           pass')
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_long_function_no_docstring(self):
        func = astroid.extract_node('\n        def func(tion):\n            pass\n            pass\n           ')
        message = Message('missing-docstring', node=func, args=('function', ))
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_long_function_nested_statements_no_docstring(self):
        func = astroid.extract_node('\n        def func(tion):\n            try:\n                pass\n            except:\n                pass\n           ')
        message = Message('missing-docstring', node=func, args=('function', ))
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_function_no_docstring_by_name(self):
        func = astroid.extract_node('\n        def __fun__(tion):\n           pass')
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)

    def test_class_no_docstring(self):
        klass = astroid.extract_node('\n        class Klass(object):\n           pass')
        message = Message('missing-docstring', node=klass, args=('class', ))
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(klass)

    def test_inner_function_no_docstring(self):
        func = astroid.extract_node('\n        def func(tion):\n            """Documented"""\n            def inner(fun):\n                # Not documented\n                pass\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)


class TestNameChecker(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker
    CONFIG = {'bad_names': set()}

    @set_config(attr_rgx=(re.compile('[A-Z]+')),
      property_classes=('abc.abstractproperty', '.custom_prop'))
    def test_property_names(self):
        methods = astroid.extract_node('\n        import abc\n\n        def custom_prop(f):\n          return property(f)\n\n        class FooClass(object):\n          @property\n          def FOO(self): #@\n            pass\n\n          @property\n          def bar(self): #@\n            pass\n\n          @abc.abstractproperty\n          def BAZ(self): #@\n            pass\n\n          @custom_prop\n          def QUX(self): #@\n            pass\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(methods[0])
            self.checker.visit_functiondef(methods[2])
            self.checker.visit_functiondef(methods[3])
        with self.assertAddsMessages(Message('invalid-name',
          node=(methods[1]),
          args=('Attribute', 'bar', "'[A-Z]+' pattern"))):
            self.checker.visit_functiondef(methods[1])

    @set_config(attr_rgx=(re.compile('[A-Z]+')))
    def test_property_setters(self):
        method = astroid.extract_node('\n        class FooClass(object):\n          @property\n          def foo(self): pass\n\n          @foo.setter\n          def FOOSETTER(self): #@\n             pass\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(method)

    def test_module_level_names(self):
        assign = astroid.extract_node('\n        import collections\n        Class = collections.namedtuple("a", ("b", "c")) #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])
        assign = astroid.extract_node('\n        class ClassA(object):\n            pass\n        ClassB = ClassA\n        ')
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])
        module = astroid.parse('\n        def A():\n          return 1, 2, 3\n        CONSTA, CONSTB, CONSTC = A()\n        CONSTD = A()')
        with self.assertNoMessages():
            self.checker.visit_assignname(module.body[1].targets[0].elts[0])
            self.checker.visit_assignname(module.body[2].targets[0])
        assign = astroid.extract_node('\n        CONST = "12 34 ".rstrip().split()')
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])

    @unittest.skipIf((sys.version_info >= (3, 7)), reason='Needs Python 3.6 or earlier')
    @set_config(const_rgx=(re.compile('.+')))
    @set_config(function_rgx=(re.compile('.+')))
    @set_config(class_rgx=(re.compile('.+')))
    def test_assign_to_new_keyword_py3(self):
        ast = astroid.extract_node('\n        async = "foo"  #@\n        await = "bar"  #@\n        def async():   #@\n            pass\n        class async:   #@\n            pass\n        ')
        with self.assertAddsMessages(Message(msg_id='assign-to-new-keyword',
          node=(ast[0].targets[0]),
          args=('async', '3.7'))):
            self.checker.visit_assignname(ast[0].targets[0])
        with self.assertAddsMessages(Message(msg_id='assign-to-new-keyword',
          node=(ast[1].targets[0]),
          args=('await', '3.7'))):
            self.checker.visit_assignname(ast[1].targets[0])
        with self.assertAddsMessages(Message(msg_id='assign-to-new-keyword', node=(ast[2]), args=('async',
                                                                                                  '3.7'))):
            self.checker.visit_functiondef(ast[2])
        with self.assertAddsMessages(Message(msg_id='assign-to-new-keyword', node=(ast[3]), args=('async',
                                                                                                  '3.7'))):
            self.checker.visit_classdef(ast[3])


class TestMultiNamingStyle(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker
    MULTI_STYLE_RE = re.compile('(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$')

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_majority(self):
        classes = astroid.extract_node('\n        class classb(object): #@\n            pass\n        class CLASSA(object): #@\n            pass\n        class CLASSC(object): #@\n            pass\n        ')
        message = Message('invalid-name',
          node=(classes[0]),
          args=('Class', 'classb', "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern"))
        with self.assertAddsMessages(message):
            for cls in classes:
                self.checker.visit_classdef(cls)

            self.checker.leave_module(cls.root)

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_first_invalid(self):
        classes = astroid.extract_node('\n        class class_a(object): #@\n            pass\n        class classb(object): #@\n            pass\n        class CLASSC(object): #@\n            pass\n        ')
        messages = [
         Message('invalid-name',
           node=(classes[0]),
           args=('Class', 'class_a', "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern")),
         Message('invalid-name',
           node=(classes[2]),
           args=('Class', 'CLASSC', "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern"))]
        with (self.assertAddsMessages)(*messages):
            for cls in classes:
                self.checker.visit_classdef(cls)

            self.checker.leave_module(cls.root)

    @set_config(method_rgx=MULTI_STYLE_RE,
      function_rgx=MULTI_STYLE_RE,
      name_group=('function:method', ))
    def test_multi_name_detection_group(self):
        function_defs = astroid.extract_node('\n        class First(object):\n            def func(self): #@\n                pass\n\n        def FUNC(): #@\n            pass\n        ',
          module_name='test')
        message = Message('invalid-name',
          node=(function_defs[1]),
          args=('Function', 'FUNC', "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern"))
        with self.assertAddsMessages(message):
            for func in function_defs:
                self.checker.visit_functiondef(func)

            self.checker.leave_module(func.root)

    @set_config(function_rgx=(re.compile('(?:(?P<ignore>FOO)|(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$')))
    def test_multi_name_detection_exempt(self):
        function_defs = astroid.extract_node('\n        def FOO(): #@\n            pass\n        def lower(): #@\n            pass\n        def FOO(): #@\n            pass\n        def UPPER(): #@\n            pass\n        ')
        message = Message('invalid-name',
          node=(function_defs[3]),
          args=('Function', 'UPPER', "'(?:(?P<ignore>FOO)|(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern"))
        with self.assertAddsMessages(message):
            for func in function_defs:
                self.checker.visit_functiondef(func)

            self.checker.leave_module(func.root)


class TestComparison(CheckerTestCase):
    CHECKER_CLASS = base.ComparisonChecker

    def test_comparison(self):
        node = astroid.extract_node('foo == True')
        message = Message('singleton-comparison', node=node, args=(True, "just 'expr'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)
        node = astroid.extract_node('foo == False')
        message = Message('singleton-comparison', node=node, args=(False, "'not expr'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)
        node = astroid.extract_node('foo == None')
        message = Message('singleton-comparison',
          node=node, args=(None, "'expr is None'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)
        node = astroid.extract_node('True == foo')
        messages = (
         Message('misplaced-comparison-constant', node=node, args=('foo == True', )),
         Message('singleton-comparison', node=node, args=(True, "just 'expr'")))
        with (self.assertAddsMessages)(*messages):
            self.checker.visit_compare(node)
        node = astroid.extract_node('False == foo')
        messages = (
         Message('misplaced-comparison-constant', node=node, args=('foo == False', )),
         Message('singleton-comparison', node=node, args=(False, "'not expr'")))
        with (self.assertAddsMessages)(*messages):
            self.checker.visit_compare(node)
        node = astroid.extract_node('None == foo')
        messages = (
         Message('misplaced-comparison-constant', node=node, args=('foo == None', )),
         Message('singleton-comparison', node=node, args=(None, "'expr is None'")))
        with (self.assertAddsMessages)(*messages):
            self.checker.visit_compare(node)


class TestNamePresets(unittest.TestCase):
    SNAKE_CASE_NAMES = {
     'test_snake_case', 'test_snake_case11', 'test_https_200'}
    CAMEL_CASE_NAMES = {'testCamelCase', 'testCamelCase11', 'testHTTP200'}
    UPPER_CASE_NAMES = {'TEST_UPPER_CASE', 'TEST_UPPER_CASE11', 'TEST_HTTP_200'}
    PASCAL_CASE_NAMES = {'TestPascalCase', 'TestPascalCase11', 'TestHTTP200'}
    ALL_NAMES = SNAKE_CASE_NAMES | CAMEL_CASE_NAMES | UPPER_CASE_NAMES | PASCAL_CASE_NAMES

    def _test_name_is_correct_for_all_name_types(self, naming_style, name):
        for name_type in base.KNOWN_NAME_TYPES:
            self._test_is_correct(naming_style, name, name_type)

    def _test_name_is_incorrect_for_all_name_types(self, naming_style, name):
        for name_type in base.KNOWN_NAME_TYPES:
            self._test_is_incorrect(naming_style, name, name_type)

    def _test_should_always_pass(self, naming_style):
        always_pass_data = [
         ('__add__', 'method'),
         ('__set_name__', 'method'),
         ('__version__', 'const'),
         ('__author__', 'const')]
        for name, name_type in always_pass_data:
            self._test_is_correct(naming_style, name, name_type)

    def _test_is_correct(self, naming_style, name, name_type):
        rgx = naming_style.get_regex(name_type)
        self.assertTrue(rgx.match(name), '{!r} does not match pattern {!r} (style: {}, type: {})'.format(name, rgx, naming_style, name_type))

    def _test_is_incorrect(self, naming_style, name, name_type):
        rgx = naming_style.get_regex(name_type)
        self.assertFalse(rgx.match(name), "{!r} match pattern {!r} but shouldn't (style: {}, type: {})".format(name, rgx, naming_style, name_type))

    def test_snake_case(self):
        naming_style = base.SnakeCaseStyle
        for name in self.SNAKE_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)

        for name in self.ALL_NAMES - self.SNAKE_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)

    def test_camel_case(self):
        naming_style = base.CamelCaseStyle
        for name in self.CAMEL_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)

        for name in self.ALL_NAMES - self.CAMEL_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)

    def test_upper_case(self):
        naming_style = base.UpperCaseStyle
        for name in self.UPPER_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)

        for name in self.ALL_NAMES - self.UPPER_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)

    def test_pascal_case(self):
        naming_style = base.PascalCaseStyle
        for name in self.PASCAL_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)

        for name in self.ALL_NAMES - self.PASCAL_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)