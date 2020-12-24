# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_typecheck.py
# Compiled at: 2019-05-03 09:16:30
# Size of source mod 2**32: 10580 bytes
"""Unittest for the type checker."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, astroid, pytest
from pylint.checkers import typecheck
from pylint.testutils import CheckerTestCase, Message, set_config

def c_extension_missing():
    """Coverage module has C-extension, which we can reuse for test"""
    try:
        import coverage.tracer as _
        return False
    except ImportError:
        _ = None
        return True


needs_c_extension = pytest.mark.skipif((c_extension_missing()),
  reason='Requires coverage (source of C-extension)')

class TestTypeChecker(CheckerTestCase):
    __doc__ = 'Tests for pylint.checkers.typecheck'
    CHECKER_CLASS = typecheck.TypeChecker

    def test_no_member_in_getattr(self):
        """Make sure that a module attribute access is checked by pylint.
        """
        node = astroid.extract_node('\n        import optparse\n        optparse.THIS_does_not_EXIST\n        ')
        with self.assertAddsMessages(Message('no-member',
          node=node,
          args=('Module', 'optparse', 'THIS_does_not_EXIST', ''))):
            self.checker.visit_attribute(node)

    @set_config(ignored_modules=('argparse', ))
    def test_no_member_in_getattr_ignored(self):
        """Make sure that a module attribute access check is omitted with a
        module that is configured to be ignored.
        """
        node = astroid.extract_node('\n        import argparse\n        argparse.THIS_does_not_EXIST\n        ')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('xml.etree.', ))
    def test_ignored_modules_invalid_pattern(self):
        node = astroid.extract_node('\n        import xml\n        xml.etree.Lala\n        ')
        message = Message('no-member',
          node=node, args=('Module', 'xml.etree', 'Lala', ''))
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(ignored_modules=('xml.etree*', ))
    def test_ignored_modules_patterns(self):
        node = astroid.extract_node('\n        import xml\n        xml.etree.portocola #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('xml.*', ))
    def test_ignored_classes_no_recursive_pattern(self):
        node = astroid.extract_node('\n        import xml\n        xml.etree.ElementTree.Test\n        ')
        message = Message('no-member',
          node=node, args=('Module', 'xml.etree.ElementTree', 'Test', ''))
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('optparse.Values', ))
    def test_ignored_classes_qualified_name(self):
        """Test that ignored-classes supports qualified name for ignoring."""
        node = astroid.extract_node('\n        import optparse\n        optparse.Values.lala\n        ')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('Values', ))
    def test_ignored_classes_only_name(self):
        """Test that ignored_classes works with the name only."""
        node = astroid.extract_node('\n        import optparse\n        optparse.Values.lala\n        ')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(suggestion_mode=False)
    @needs_c_extension
    def test_nomember_on_c_extension_error_msg(self):
        node = astroid.extract_node('\n        from coverage import tracer\n        tracer.CTracer  #@\n        ')
        message = Message('no-member',
          node=node, args=('Module', 'coverage.tracer', 'CTracer', ''))
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(suggestion_mode=True)
    @needs_c_extension
    def test_nomember_on_c_extension_info_msg(self):
        node = astroid.extract_node('\n        from coverage import tracer\n        tracer.CTracer  #@\n        ')
        message = Message('c-extension-no-member',
          node=node,
          args=('Module', 'coverage.tracer', 'CTracer', ''))
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(contextmanager_decorators=('contextlib.contextmanager', '.custom_contextmanager'))
    def test_custom_context_manager(self):
        """Test that @custom_contextmanager is recognized as configured."""
        node = astroid.extract_node('\n        from contextlib import contextmanager\n        def custom_contextmanager(f):\n            return contextmanager(f)\n        @custom_contextmanager\n        def dec():\n            yield\n        with dec():\n            pass\n        ')
        with self.assertNoMessages():
            self.checker.visit_with(node)

    def test_invalid_metaclass(self):
        module = astroid.parse('\n        import six\n\n        class InvalidAsMetaclass(object):\n            pass\n\n        @six.add_metaclass(int)\n        class FirstInvalid(object):\n            pass\n\n        @six.add_metaclass(InvalidAsMetaclass)\n        class SecondInvalid(object):\n            pass\n\n        @six.add_metaclass(2)\n        class ThirdInvalid(object):\n            pass\n        ')
        for class_obj, metaclass_name in (('ThirdInvalid', '2'), ('SecondInvalid', 'InvalidAsMetaclass'),
                                          ('FirstInvalid', 'int')):
            classdef = module[class_obj]
            message = Message('invalid-metaclass',
              node=classdef, args=(metaclass_name,))
            with self.assertAddsMessages(message):
                self.checker.visit_classdef(classdef)

    @pytest.mark.skipif((sys.version_info[0] < 3), reason='Needs Python 3.')
    def test_invalid_metaclass_function_metaclasses(self):
        module = astroid.parse('\n        def invalid_metaclass_1(name, bases, attrs):\n            return int\n        def invalid_metaclass_2(name, bases, attrs):\n            return 1\n        class Invalid(metaclass=invalid_metaclass_1):\n            pass\n        class InvalidSecond(metaclass=invalid_metaclass_2):\n            pass\n        ')
        for class_obj, metaclass_name in (('Invalid', 'int'), ('InvalidSecond', '1')):
            classdef = module[class_obj]
            message = Message('invalid-metaclass',
              node=classdef, args=(metaclass_name,))
            with self.assertAddsMessages(message):
                self.checker.visit_classdef(classdef)

    @pytest.mark.skipif((sys.version_info < (3, 5)), reason='Needs Python 3.5.')
    def test_typing_namedtuple_not_callable_issue1295(self):
        module = astroid.parse("\n        import typing\n        Named = typing.NamedTuple('Named', [('foo', int), ('bar', int)])\n        named = Named(1, 2)\n        ")
        call = module.body[(-1)].value
        callables = call.func.inferred()
        @py_assert2 = len(callables)
        @py_assert5 = 1
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_typecheck.py', lineno=264)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(callables) if 'callables' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(callables) else 'callables',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = callables[0]
        @py_assert2 = @py_assert0.callable
        @py_assert4 = @py_assert2()
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_typecheck.py', lineno=265)
        if not @py_assert4:
            @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.callable\n}()\n}' % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        with self.assertNoMessages():
            self.checker.visit_call(call)

    @pytest.mark.skipif((sys.version_info < (3, 5)), reason='Needs Python 3.5.')
    def test_typing_namedtuple_unsubscriptable_object_issue1295(self):
        module = astroid.parse('\n        import typing\n        MyType = typing.Tuple[str, str]\n        ')
        subscript = module.body[(-1)].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def test_staticmethod_multiprocessing_call(self):
        """Make sure not-callable isn't raised for descriptors

        astroid can't process descriptors correctly so
        pylint needs to ignore not-callable for them
        right now

        Test for https://github.com/PyCQA/pylint/issues/1699
        """
        call = astroid.extract_node('\n        import multiprocessing\n        multiprocessing.current_process() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(call)

    def test_not_callable_uninferable_property(self):
        """Make sure not-callable isn't raised for uninferable
        properties
        """
        call = astroid.extract_node('\n        class A:\n            @property\n            def call(self):\n                return undefined\n\n        a = A()\n        a.call() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(call)

    def test_descriptor_call(self):
        call = astroid.extract_node('\n        def func():\n            pass\n\n        class ADescriptor:\n            def __get__(self, instance, owner):\n                return func\n\n        class AggregateCls:\n            a = ADescriptor()\n\n        AggregateCls().a() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(call)

    def test_unknown_parent(self):
        """Make sure the callable check does not crash when a node's parent
        cannot be determined.
        """
        call = astroid.extract_node('\n        def get_num(n):\n            return 2 * n\n        get_num(10)()\n        ')
        with self.assertAddsMessages(Message('not-callable', node=call, args='get_num(10)')):
            self.checker.visit_call(call)