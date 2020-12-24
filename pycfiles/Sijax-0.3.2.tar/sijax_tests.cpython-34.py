# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tests/sijax_tests.py
# Compiled at: 2015-02-02 04:16:25
# Size of source mod 2**32: 37803 bytes
from __future__ import absolute_import, unicode_literals
import sys, os, unittest, tempfile, shutil
from contextlib import contextmanager
from builtins import range, next, open
from six import string_types
sijax_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(sijax_path)
from sijax import Sijax
from sijax.response import BaseResponse, StreamingIframeResponse
from sijax.exception import SijaxError
from sijax.plugin.comet import register_comet_callback, register_comet_object, CometResponse
from sijax.plugin.upload import register_upload_callback, UploadResponse
from sijax.helper import init_static_path

@contextmanager
def temporary_dir(*args, **kwargs):
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


class SijaxMainTestCase(unittest.TestCase):

    def test_changing_incoming_data_works(self):
        inst = Sijax()
        self.assertTrue(inst.get_data() == {})
        data = {'key': 'value'}
        inst.set_data(data)
        self.assertTrue(inst.get_data() == data)
        data = {'key': 'value',  'another': 'one'}
        self.assertTrue(inst.get_data() == {'key': 'value'})
        inst.set_data(data)
        self.assertTrue(inst.get_data() == data)

    def test_detecting_sijax_requests_works(self):
        inst = Sijax()
        cls = inst.__class__
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        inst.set_data({'key': 'value'})
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        inst.set_data({cls.PARAM_REQUEST: 'function'})
        self.assertFalse(inst.is_sijax_request)
        self.assertEqual(inst.requested_function, 'function')
        inst.set_data({cls.PARAM_ARGS: '[]'})
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        self.assertEqual([], inst.request_args)
        inst.set_data({cls.PARAM_ARGS: '["invalid_json": here'})
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        self.assertEqual([], inst.request_args)
        inst.set_data({cls.PARAM_REQUEST: 'function',  cls.PARAM_ARGS: '["arg1", 5]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual('function', inst.requested_function)
        self.assertEqual(['arg1', 5], inst.request_args)
        inst.set_data({cls.PARAM_REQUEST: 'func2',  cls.PARAM_ARGS: '[28, 5]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual('func2', inst.requested_function)
        self.assertEqual([28, 5], inst.request_args)

    def test_events_have_default_handlers(self):
        inst = Sijax()
        cls = inst.__class__
        events = [getattr(cls, attr) for attr in dir(cls) if attr.startswith('EVENT_')]
        for event in events:
            self.assertTrue(inst.has_event(event), 'No handler for %s' % event)

    def test_registering_custom_events_works(self):
        inst = Sijax()
        event_name = 'my_event'
        event_callback = lambda obj_response: obj_response.alert('Event')
        self.assertFalse(inst.has_event(event_name), 'Custom event registered')
        inst.register_event(event_name, event_callback)
        self.assertTrue(inst.has_event(event_name), 'Failed to register event')

    def test_executing_regular_callbacks_works(self):
        calls_history = []
        call_args_history = []

        def event_before(obj_response):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            calls_history.append('before')
            obj_response.script('javascript here..')

        def event_after(obj_response):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            calls_history.append('after')
            obj_response.css('#element', 'backgroundColor', 'red')

        def callback_main(obj_response, arg1, arg2):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            calls_history.append('main')
            call_args_history.append(arg1)
            call_args_history.append(arg2)
            obj_response.alert('alert from main')

        inst = Sijax()
        cls = inst.__class__
        inst.register_event(cls.EVENT_BEFORE_PROCESSING, event_before)
        inst.register_event(cls.EVENT_AFTER_PROCESSING, event_after)
        call_args = [
         'arg1', 15]
        response = inst.execute_callback(call_args, callback=callback_main)
        self.assertEqual(['before', 'main', 'after'], calls_history)
        self.assertEqual(call_args, call_args_history)
        self.assertTrue(isinstance(response, string_types))
        from sijax.helper import json
        try:
            commands = json.loads(response)
        except:
            self.fail('Invalid JSON response!')
        else:
            self.assertTrue(isinstance(commands, list))
            commands_history = []
            for cmd_params in commands:
                self.assertTrue(isinstance(cmd_params, dict))
                self.assertTrue('type' in cmd_params, 'Unknown command type!')
                commands_history.append(cmd_params['type'])

        self.assertEqual(['script', 'alert', 'css'], commands_history)

    def test_bad_callback_objects_raise_exception(self):
        inst = Sijax()
        try:
            inst.execute_callback(callback='non-callable object', args=[])
            self.fail('SijaxError not raised when bad callback was given!')
        except SijaxError:
            pass

    def test_get_js_fails_with_missing_request_uri(self):
        inst = Sijax()
        try:
            inst.get_js()
            self.fail()
        except SijaxError:
            pass

    def test_changing_uris_results_in_a_differnt_js_output(self):
        inst = Sijax()
        req_uri = 'http://localhost:8080/submit_here'
        json_uri = 'http://localhost:8080/json2.js'
        inst.set_request_uri(req_uri)
        js = inst.get_js()
        self.assertTrue('Sijax.setRequestUri("%s");' % req_uri in js)
        self.assertFalse('Sijax.setJsonUri' in js)
        inst.set_json_uri(json_uri)
        js = inst.get_js()
        self.assertTrue('Sijax.setRequestUri("%s");' % req_uri in js)
        self.assertTrue('Sijax.setJsonUri("%s");' % json_uri in js)

    def test_process_request_throws_exception_when_called_for_non_sijax_requests(self):
        inst = Sijax()
        try:
            inst.process_request()
            self.fail('Process request got executed for a non-sijax request!')
        except SijaxError:
            pass

    def test_process_request_calls_invalid_request_event_for_invalid_requests(self):
        from sijax.helper import json
        inst = Sijax()
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '["arg1", 12]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual('my_func', inst.requested_function)
        self.assertEqual(['arg1', 12], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        try:
            commands = json.loads(response)
        except:
            self.fail('Invalid JSON generated!')
        else:
            self.assertTrue(isinstance(commands, list))
            self.assertEqual(1, len(commands))
            command_data = commands.pop(0)
            self.assertTrue('type' in command_data)
            self.assertEqual('alert', command_data['type'])

    def test_process_request_calls_invalid_call_event_for_invalid_calls(self):
        from types import FunctionType
        from sijax.helper import json
        call_history = []

        def my_callback(obj_response, arg1, arg2):
            call_history.append('call ok')

        def my_callback_with_defaults(obj_response, arg1=138, arg2=15):
            call_history.append('defaults ok')

        def my_callback_raising_TypeError(obj_response):
            raise TypeError('this should be re-raised by Sijax')

        def my_callback_raising_TypeError2(obj_response):

            def inner():
                raise TypeError('this should be re-raised by Sijax')

            inner()

        def invalid_call(obj_response, failed_callback):
            self.assertTrue(isinstance(failed_callback, FunctionType))
            call_history.append('invalid %s' % failed_callback.__name__)

        inst = Sijax()
        cls = inst.__class__
        inst.register_callback('my_func', my_callback)
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '["arg1", 12]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual('my_func', inst.requested_function)
        self.assertEqual(['arg1', 12], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '["arg1"]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual('my_func', inst.requested_function)
        self.assertEqual(['arg1'], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        try:
            commands = json.loads(response)
        except:
            self.fail('Invalid JSON generated!')
        else:
            self.assertTrue(isinstance(commands, list))
            self.assertEqual(1, len(commands))
            command_data = commands.pop(0)
            self.assertTrue('type' in command_data)
            self.assertEqual('alert', command_data['type'])
        inst.register_event(cls.EVENT_INVALID_CALL, invalid_call)
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '[]'})
        self.assertEqual('my_func', inst.requested_function)
        self.assertEqual([], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        inst.register_callback('my_func', my_callback_with_defaults)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        inst.register_callback('my_func', my_callback_raising_TypeError)
        try:
            inst.process_request()
        except TypeError:
            call_history.append('TypeError')

        inst.register_callback('my_func', my_callback_raising_TypeError2)
        try:
            inst.process_request()
        except TypeError:
            call_history.append('TypeError2')

        expected = ['call ok', 'invalid my_callback', 'defaults ok',
         'TypeError', 'TypeError2']
        self.assertEqual(expected, call_history)

    def test_new_callbacks_override_old_during_registering(self):
        call_history = []

        def callback_one(obj_response):
            call_history.append('one')

        def callback_two(obj_response):
            call_history.append('two')

        inst = Sijax()
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.register_callback('my_func', callback_one)
        inst.process_request()
        inst.register_callback('my_func', callback_two)
        inst.process_request()
        self.assertEqual(['one', 'two'], call_history)

    def test_mass_registering_from_a_class_works(self):
        call_history = []

        class SijaxHandler(object):

            @staticmethod
            def callback_one(obj_response):
                call_history.append('one')

            @staticmethod
            def callback_two(obj_response):
                call_history.append('two')

            @classmethod
            def callback_three(cls, obj_response):
                call_history.append('three')

        inst = Sijax()
        inst.register_object(SijaxHandler)
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: 'callback_one',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: 'callback_two',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: 'callback_three',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        self.assertEqual(['one', 'two', 'three'], call_history)

    def test_mass_registering_from_an_object_works(self):
        call_history = []

        class SijaxHandler(object):

            def callback_one(self, obj_response):
                call_history.append('one')

            def callback_two(self, obj_response):
                call_history.append('two')

        inst = Sijax()
        inst.register_object(SijaxHandler())
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: 'callback_one',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: 'callback_two',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        self.assertEqual(['one', 'two'], call_history)

    def test_the_response_class_could_be_changed_during_registration(self):
        call_history = []

        class CustomResponse(BaseResponse):
            pass

        def my_callback(obj_response):
            call_history.append('regular')
            self.assertFalse(isinstance(obj_response, CustomResponse))
            self.assertTrue(isinstance(obj_response, BaseResponse))

        def my_custom_callback(obj_response):
            call_history.append('custom')
            self.assertTrue(isinstance(obj_response, CustomResponse))

        inst = Sijax()
        cls = inst.__class__
        inst.register_callback('my_func', my_callback)
        params_custom = {cls.PARAM_RESPONSE_CLASS: CustomResponse}
        inst.register_callback('my_func_custom', my_custom_callback, **params_custom)
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: 'my_func_custom',  cls.PARAM_ARGS: '[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        self.assertEqual(['regular', 'custom'], call_history)

    def test_args_extra_works_properly(self):
        call_history = []

        def callback(obj_response, arg1_custom, arg2_custom, arg_regular):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            call_history.append(arg1_custom)
            call_history.append(arg2_custom)
            call_history.append(arg_regular)

        def callback_basic(obj_response, arg_regular):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            call_history.append(arg_regular)

        inst = Sijax()
        cls = inst.__class__
        inst.register_callback('callback', callback, args_extra=('one', 'two'))
        inst.set_data({cls.PARAM_REQUEST: 'callback',  cls.PARAM_ARGS: '["regular"]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.register_callback('callback', callback_basic)
        inst.set_data({cls.PARAM_REQUEST: 'callback',  cls.PARAM_ARGS: '["reg2"]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        call_history_expected = [
         'one', 'two', 'regular', 'reg2']
        self.assertEqual(call_history_expected, call_history)

    def test_args_extra_expects_a_list_or_a_tuple(self):
        inst = Sijax()

        def try_args(args_extra, should_succeed):
            success = False
            try:
                inst.register_callback('name', lambda r: r, args_extra=args_extra)
                success = True
            except SijaxError:
                pass

            self.assertEqual(should_succeed, success, 'Failure for %s' % repr(args_extra))

        try_args([], True)
        try_args((), True)
        try_args(None, True)
        try_args(['one item'], True)
        try_args(('one item', ), True)
        try_args(['one', 'two'], True)
        try_args(('one', 'two'), True)
        try_args([{'dictionary': 'in',  'the': 'list'}], True)
        try_args(({'dictionary': 'in',  'the': 'tuple'},), True)
        try_args('string', False)
        try_args(True, False)
        try_args(False, False)
        try_args({'dictionary': 'here'}, False)

    def test_regular_functions_that_yield_are_not_allowed(self):
        inst = Sijax()

        def callback(obj_response):
            yield obj_response

        try:
            inst.execute_callback([], callback)
            self.fail("Yielding regular function didn't raise expected exception!")
        except SijaxError:
            pass

    def test_response_method_call_rejects_bad_args(self):
        inst = Sijax()

        def try_call(args_value, should_succeed):

            def callback(obj_response):
                obj_response.call('function', args_value)

            success = False
            try:
                inst.execute_callback([], callback)
                success = True
            except SijaxError:
                pass

            self.assertEqual(should_succeed, success, 'Failure for %s' % repr(args_value))

        try_call(None, True)
        try_call([], True)
        try_call(['arg1', 'arg2', 3, 4, 'arg5'], True)
        try_call((), True)
        try_call('arg1', False)
        try_call(1, False)
        try_call({'dictionary': 'here'}, False)

    def test_init_static_path_helper_works(self):
        import os, sijax
        with temporary_dir() as (static_path):
            init_static_path(static_path)
            version_file = os.path.join(static_path, 'sijax_version')
            if not os.path.exists(version_file):
                self.fail('Version file %s does not exist' % version_file)
            with open(version_file) as (fp):
                self.assertEqual(fp.read(), sijax.__version__)
            core_js_file = os.path.join(static_path, 'sijax.js')
            with open(core_js_file, 'w') as (fp):
                fp.write('new stuff')
            init_static_path(static_path)
            with open(core_js_file) as (fp):
                self.assertEqual(fp.read(), 'new stuff')
            with open(version_file, 'w') as (fp):
                fp.write('another_version_string')
            new_file = os.path.join(static_path, 'extra-file.js')
            self.assertFalse(os.path.exists(new_file))
            with open(new_file, 'w') as (fp):
                fp.write('blah')
            self.assertTrue(os.path.exists(new_file))
            init_static_path(static_path)
            with open(core_js_file) as (fp):
                self.assertNotEqual(fp.read(), 'new stuff')
            with open(version_file) as (fp):
                self.assertEqual(fp.read(), sijax.__version__)
            self.assertFalse(os.path.exists(new_file))

    def test_static_path_helper_refuses_to_write_to_non_empty_paths(self):
        import os

        def try_init(path, should_succeed):
            success = False
            try:
                init_static_path(path)
                success = True
            except SijaxError:
                pass

            self.assertEqual(should_succeed, success)

        with temporary_dir() as (static_path):
            try_init(static_path, True)
        with temporary_dir() as (static_path):
            with open(os.path.join(static_path, 'some.file'), 'w') as (fp):
                fp.write('blah')
            try_init(static_path, False)
        with temporary_dir() as (static_path):
            with open(os.path.join(static_path, 'some.file'), 'w') as (fp):
                fp.write('blah')
            with open(os.path.join(static_path, 'sijax_version'), 'w') as (fp):
                fp.write('version_string')
            try_init(static_path, True)

    def test_response_classes_need_to_be_callable(self):
        inst = Sijax()

        def try_response_class(response_class, should_succeed):
            success = False
            try:
                inst.register_callback('name', lambda r: r, response_class=response_class)
                success = True
            except SijaxError:
                pass

            self.assertEqual(should_succeed, success, 'Failure for %s' % repr(response_class))

        try_response_class(BaseResponse, True)

        class CustomResponse(BaseResponse):
            pass

        try_response_class(CustomResponse, True)

        def response_factory(*args, **kwargs):
            return CustomResponse(*args, **kwargs)

        try_response_class(response_factory, True)
        try_response_class(None, True)
        try_response_class('', False)
        try_response_class(14, False)


class SijaxStreamingTestCase(unittest.TestCase):
    __doc__ = 'This tests the StreamingIframeResponse functionality, which is\n    used behind the Comet and Upload plugins.\n    '

    def test_streaming_functions_return_generators(self):
        from types import GeneratorType
        call_history = []

        def callback_before(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('before')
            obj_response.html('#div', 'before html')

        def callback_after(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('after')

        def callback_yielding(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('yielding')
            obj_response.alert('test')
            yield obj_response
            obj_response.css('#div', 'color', 'red')

        def callback_normal(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('normal')
            obj_response.script('.. javascript here..')

        def assert_generator_entries_length(generator, length):
            items = []
            try:
                while True:
                    items.append(next(generator))

            except StopIteration:
                pass

            self.assertEqual(length, len(items))

        inst = Sijax()
        cls = inst.__class__
        inst.register_event(cls.EVENT_BEFORE_PROCESSING, callback_before)
        inst.register_event(cls.EVENT_AFTER_PROCESSING, callback_after)
        options = {cls.PARAM_RESPONSE_CLASS: StreamingIframeResponse}
        response = inst.execute_callback([], callback=callback_yielding, **options)
        self.assertTrue(isinstance(response, GeneratorType))
        assert_generator_entries_length(response, 3)

        def callback_before_new(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('before_new')
            for i in range(10):
                yield obj_response

            for i in range(2):
                obj_response.alert('hey')
                yield obj_response

        inst.register_event(cls.EVENT_BEFORE_PROCESSING, callback_before_new)
        inst.register_event(cls.EVENT_AFTER_PROCESSING, lambda r: r.alert('this yields'))
        response = inst.execute_callback([], callback=callback_normal, **options)
        self.assertTrue(isinstance(response, GeneratorType))
        assert_generator_entries_length(response, 4)
        call_history_expected = [
         'before', 'yielding', 'after',
         'before_new', 'normal']
        self.assertEqual(call_history_expected, call_history)

    def test_invalid_call_event_works(self):
        from types import GeneratorType, FunctionType
        call_history = []

        def my_callback(obj_response, arg1, arg2):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('call ok')

        def my_callback_raising_TypeError(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            raise TypeError('this should be re-raised by Sijax')

        def my_callback_raising_TypeError2(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))

            def inner():
                raise TypeError('this should be re-raised by Sijax')

            inner()

        def invalid_call(obj_response, failed_callback):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            self.assertTrue(isinstance(failed_callback, FunctionType))
            call_history.append('invalid %s' % failed_callback.__name__)

        def exhaust_generator(gen):
            self.assertTrue(isinstance(gen, GeneratorType))
            try:
                while True:
                    next(gen)

            except StopIteration:
                pass

        inst = Sijax()
        cls = inst.__class__
        options = {cls.PARAM_RESPONSE_CLASS: StreamingIframeResponse}
        inst.register_event(cls.EVENT_INVALID_CALL, invalid_call)
        inst.register_callback('my_func', my_callback, **options)
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '["arg1", 12]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual('my_func', inst.requested_function)
        self.assertEqual(['arg1', 12], inst.request_args)
        response = inst.process_request()
        exhaust_generator(response)
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '[]'})
        self.assertEqual('my_func', inst.requested_function)
        self.assertEqual([], inst.request_args)
        response = inst.process_request()
        exhaust_generator(response)
        inst.register_callback('my_func', my_callback_raising_TypeError, **options)
        try:
            response = inst.process_request()
            exhaust_generator(response)
        except TypeError:
            call_history.append('TypeError')

        inst.register_callback('my_func', my_callback_raising_TypeError2, **options)
        try:
            response = inst.process_request()
            exhaust_generator(response)
        except TypeError:
            call_history.append('TypeError2')

        expected = ['call ok', 'invalid my_callback',
         'TypeError', 'TypeError2']
        self.assertEqual(expected, call_history)


class SijaxCometTestCase(unittest.TestCase):
    __doc__ = 'Exercises certain Comet specific things. Most of the functionality\n    that Comet is based on is tested elsewhere (StreamingIframeResponse).\n    '

    def test_registering_helper_works(self):
        from types import GeneratorType

        class CustomResponse(CometResponse):
            pass

        def process_request(inst):
            self.assertTrue(inst.is_sijax_request)
            response = inst.process_request()
            self.assertTrue(isinstance(response, GeneratorType))
            for string in response:
                pass

        call_history = []

        def invalid_call(obj_response, callback):
            self.fail('Invalid call handler triggered!')

        inst = Sijax()
        cls = inst.__class__
        inst.register_event(cls.EVENT_INVALID_CALL, invalid_call)
        inst.set_data({cls.PARAM_REQUEST: 'my_func',  cls.PARAM_ARGS: '[]'})

        def my_callback(obj_response):
            self.assertTrue(isinstance(obj_response, CometResponse))
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('my_callback')
            call_history.append(type(obj_response).__name__)

        register_comet_callback(inst, 'my_func', my_callback)
        process_request(inst)
        params_custom = {cls.PARAM_RESPONSE_CLASS: CustomResponse}
        register_comet_callback(inst, 'my_func', my_callback, **params_custom)
        process_request(inst)

        class SijaxHandler(object):

            @staticmethod
            def callback_one(obj_response, arg1):
                self.assertTrue(isinstance(obj_response, CustomResponse))
                call_history.append('callback_one')
                call_history.append(type(obj_response).__name__)
                call_history.append(arg1)

        register_comet_object(inst, SijaxHandler, **params_custom)
        inst.set_data({cls.PARAM_REQUEST: 'callback_one',  cls.PARAM_ARGS: '[45]'})
        process_request(inst)
        call_history_expected = [
         'my_callback', 'CometResponse',
         'my_callback', 'CustomResponse',
         'callback_one', 'CustomResponse', 45]
        self.assertEqual(call_history_expected, call_history)


class SijaxUploadTestCase(unittest.TestCase):
    __doc__ = 'Exercises certain Comet specific things. Most of the functionality\n    that Comet is based on is tested elsewhere (StreamingIframeResponse).\n    '

    def test_registering_helper_works(self):
        from types import GeneratorType
        from sijax.plugin.upload import func_name_by_form_id

        class CustomResponse(UploadResponse):
            pass

        def process_request(inst):
            self.assertTrue(inst.is_sijax_request)
            response = inst.process_request()
            self.assertTrue(isinstance(response, GeneratorType))
            for string in response:
                pass

        call_history = []

        def invalid_call(obj_response, callback):
            self.fail('Invalid call handler triggered!')

        inst = Sijax()
        cls = inst.__class__
        inst.register_event(cls.EVENT_INVALID_CALL, invalid_call)

        def my_callback(obj_response, files, form_values):
            self.assertTrue(isinstance(obj_response, UploadResponse))
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('my_callback')
            call_history.append(obj_response.form_id)
            call_history.append(type(obj_response).__name__)
            call_history.append(files['file'])
            self.assertEqual({'form_key': 'value',  'form_key2': 15}, form_values)

        def my_callback2(obj_response, custom_arg1, custom_arg2, form_values):
            self.assertTrue(isinstance(obj_response, UploadResponse))
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append('custom_callback')
            call_history.append(obj_response.form_id)
            call_history.append(type(obj_response).__name__)
            call_history.append(custom_arg1)
            call_history.append(custom_arg2)
            self.assertEqual({'form_key': 'value',  'form_key2': 15}, form_values)

        form_id = 'my_form'
        public_callback_name = func_name_by_form_id(form_id)
        request_args_json = '["%s"]' % form_id
        post = {}
        post[cls.PARAM_REQUEST] = public_callback_name
        post[cls.PARAM_ARGS] = request_args_json
        post['form_key'] = 'value'
        post['form_key2'] = 15
        inst.set_data(post)
        files = {'file': 'object',  'passed': 'here'}
        register_upload_callback(inst, form_id, my_callback, args_extra=(files,))
        process_request(inst)
        params_custom = {cls.PARAM_RESPONSE_CLASS: CustomResponse}
        register_upload_callback(inst, form_id, my_callback2, args_extra=('custom1',
                                                                          'custom2'), **params_custom)
        process_request(inst)
        call_history_expected = [
         'my_callback', form_id, 'UploadResponse', 'object',
         'custom_callback', form_id, 'CustomResponse', 'custom1', 'custom2']
        self.assertEqual(call_history_expected, call_history)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SijaxMainTestCase))
    suite.addTest(unittest.makeSuite(SijaxStreamingTestCase))
    suite.addTest(unittest.makeSuite(SijaxCometTestCase))
    suite.addTest(unittest.makeSuite(SijaxUploadTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')