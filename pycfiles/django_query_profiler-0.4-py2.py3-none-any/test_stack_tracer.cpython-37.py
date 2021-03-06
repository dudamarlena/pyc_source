# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/unit/test_stack_tracer.py
# Compiled at: 2020-01-07 01:26:59
# Size of source mod 2**32: 4326 bytes
from typing import Dict, Set
from unittest import TestCase
from django_query_profiler.query_profiler_storage import stack_tracer

class StackTracerTest(TestCase):
    __doc__ = '\n    Tests for validating if we are able to find the correct stack-trace - and if we are able to exclude the stack-traces\n    which we should exclude, and include the correct stack-traces\n    '

    def test_empty_params(self):
        app_stack_trace, django_stack_trace = stack_tracer.find_stack_trace((), (), 100)
        self.assertTupleEqual(django_stack_trace, ())
        app_module_names = [stack_trace.module_name for stack_trace in app_stack_trace]
        self.assertEqual(stack_tracer.find_stack_trace.__module__, app_module_names[0])
        self.assertEqual(self.__module__, app_module_names[1])
        self.assertTrue('unittest' in app_module_names[2])
        memoized_value_app_modules = stack_tracer.MEMO_APP_MODULE_NAME_DECISION[()]
        self.assertSetEqual(_keys_set_for_passed_value(memoized_value_app_modules, True), set(app_module_names))
        self.assertEqual(_keys_set_for_passed_value(memoized_value_app_modules, False), set())
        memoized_value_django_modules = stack_tracer.MEMO_DJANGO_MODULE_NAME_DECISION[()]
        self.assertEqual(_keys_set_for_passed_value(memoized_value_django_modules, False), set(app_module_names))

    def test_valid_app_params(self):
        app_stack_trace, django_stack_trace = stack_tracer.find_stack_trace((
         stack_tracer.find_stack_trace.__module__, self.__module__, 'unittest'), (), 100)
        self.assertTupleEqual(django_stack_trace, ())
        app_module_names = {stack_trace.module_name for stack_trace in app_stack_trace}
        self.assertTrue(stack_tracer.find_stack_trace.__module__ not in app_module_names)
        self.assertTrue(self.__module__ not in app_module_names)
        self.assertFalse(any((module_name.startswith('unittest') for module_name in app_module_names)))
        self.assertIsNotNone(str(app_stack_trace[0]))

    def test_invalid_app_params(self):
        app_stack_trace, django_stack_trace = stack_tracer.find_stack_trace(('random_does_not_exist', ), (), 100)
        self.assertTupleEqual(django_stack_trace, ())
        app_module_names = [stack_trace.module_name for stack_trace in app_stack_trace]
        self.assertEqual(stack_tracer.find_stack_trace.__module__, app_module_names[0])
        self.assertEqual(self.__module__, app_module_names[1])
        self.assertTrue('unittest' in app_module_names[2])
        memoized_value_app_modules = stack_tracer.MEMO_APP_MODULE_NAME_DECISION[('random_does_not_exist', )]
        self.assertSetEqual(_keys_set_for_passed_value(memoized_value_app_modules, True), set(app_module_names))
        self.assertEqual(_keys_set_for_passed_value(memoized_value_app_modules, False), set())
        memoized_value_django_modules = stack_tracer.MEMO_DJANGO_MODULE_NAME_DECISION[()]
        self.assertEqual(_keys_set_for_passed_value(memoized_value_django_modules, False), set(app_module_names))

    def test_valid_django_params(self):
        app_stack_trace, django_stack_trace = stack_tracer.find_stack_trace((), (
         stack_tracer.find_stack_trace.__module__, self.__module__, 'unittest'), 100)
        django_module_names = {stack_trace.module_name for stack_trace in django_stack_trace}
        self.assertTrue(stack_tracer.find_stack_trace.__module__ in django_module_names)
        self.assertTrue(self.__module__ in django_module_names)
        self.assertTrue(any((module_name.startswith('unittest') for module_name in django_module_names)))


def _keys_set_for_passed_value(dictionary: Dict[(str, bool)], value_condition: bool) -> Set[str]:
    """ A helper function to find all keys for which value in dictionary is value_condition """
    return {key for key, value in dictionary.items() if value is value_condition}