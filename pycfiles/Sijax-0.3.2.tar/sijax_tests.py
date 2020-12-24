# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tests/sijax_tests.py
# Compiled at: 2015-02-02 04:16:25
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
        data = {b'key': b'value'}
        inst.set_data(data)
        self.assertTrue(inst.get_data() == data)
        data = {b'key': b'value', b'another': b'one'}
        self.assertTrue(inst.get_data() == {b'key': b'value'})
        inst.set_data(data)
        self.assertTrue(inst.get_data() == data)

    def test_detecting_sijax_requests_works(self):
        inst = Sijax()
        cls = inst.__class__
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        inst.set_data({b'key': b'value'})
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        inst.set_data({cls.PARAM_REQUEST: b'function'})
        self.assertFalse(inst.is_sijax_request)
        self.assertEqual(inst.requested_function, b'function')
        inst.set_data({cls.PARAM_ARGS: b'[]'})
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        self.assertEqual([], inst.request_args)
        inst.set_data({cls.PARAM_ARGS: b'["invalid_json": here'})
        self.assertFalse(inst.is_sijax_request)
        self.assertTrue(inst.requested_function is None)
        self.assertEqual([], inst.request_args)
        inst.set_data({cls.PARAM_REQUEST: b'function', cls.PARAM_ARGS: b'["arg1", 5]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual(b'function', inst.requested_function)
        self.assertEqual([b'arg1', 5], inst.request_args)
        inst.set_data({cls.PARAM_REQUEST: b'func2', cls.PARAM_ARGS: b'[28, 5]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual(b'func2', inst.requested_function)
        self.assertEqual([28, 5], inst.request_args)
        return

    def test_events_have_default_handlers(self):
        inst = Sijax()
        cls = inst.__class__
        events = [ getattr(cls, attr) for attr in dir(cls) if attr.startswith(b'EVENT_') ]
        for event in events:
            self.assertTrue(inst.has_event(event), b'No handler for %s' % event)

    def test_registering_custom_events_works(self):
        inst = Sijax()
        event_name = b'my_event'
        event_callback = lambda obj_response: obj_response.alert(b'Event')
        self.assertFalse(inst.has_event(event_name), b'Custom event registered')
        inst.register_event(event_name, event_callback)
        self.assertTrue(inst.has_event(event_name), b'Failed to register event')

    def test_executing_regular_callbacks_works(self):
        calls_history = []
        call_args_history = []

        def event_before(obj_response):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            calls_history.append(b'before')
            obj_response.script(b'javascript here..')

        def event_after(obj_response):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            calls_history.append(b'after')
            obj_response.css(b'#element', b'backgroundColor', b'red')

        def callback_main(obj_response, arg1, arg2):
            self.assertTrue(isinstance(obj_response, BaseResponse))
            calls_history.append(b'main')
            call_args_history.append(arg1)
            call_args_history.append(arg2)
            obj_response.alert(b'alert from main')

        inst = Sijax()
        cls = inst.__class__
        inst.register_event(cls.EVENT_BEFORE_PROCESSING, event_before)
        inst.register_event(cls.EVENT_AFTER_PROCESSING, event_after)
        call_args = [
         b'arg1', 15]
        response = inst.execute_callback(call_args, callback=callback_main)
        self.assertEqual([b'before', b'main', b'after'], calls_history)
        self.assertEqual(call_args, call_args_history)
        self.assertTrue(isinstance(response, string_types))
        from sijax.helper import json
        try:
            commands = json.loads(response)
        except:
            self.fail(b'Invalid JSON response!')

        self.assertTrue(isinstance(commands, list))
        commands_history = []
        for cmd_params in commands:
            self.assertTrue(isinstance(cmd_params, dict))
            self.assertTrue(b'type' in cmd_params, b'Unknown command type!')
            commands_history.append(cmd_params[b'type'])

        self.assertEqual([b'script', b'alert', b'css'], commands_history)

    def test_bad_callback_objects_raise_exception(self):
        inst = Sijax()
        try:
            inst.execute_callback(callback=b'non-callable object', args=[])
            self.fail(b'SijaxError not raised when bad callback was given!')
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
        req_uri = b'http://localhost:8080/submit_here'
        json_uri = b'http://localhost:8080/json2.js'
        inst.set_request_uri(req_uri)
        js = inst.get_js()
        self.assertTrue(b'Sijax.setRequestUri("%s");' % req_uri in js)
        self.assertFalse(b'Sijax.setJsonUri' in js)
        inst.set_json_uri(json_uri)
        js = inst.get_js()
        self.assertTrue(b'Sijax.setRequestUri("%s");' % req_uri in js)
        self.assertTrue(b'Sijax.setJsonUri("%s");' % json_uri in js)

    def test_process_request_throws_exception_when_called_for_non_sijax_requests(self):
        inst = Sijax()
        try:
            inst.process_request()
            self.fail(b'Process request got executed for a non-sijax request!')
        except SijaxError:
            pass

    def test_process_request_calls_invalid_request_event_for_invalid_requests(self):
        from sijax.helper import json
        inst = Sijax()
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'["arg1", 12]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual(b'my_func', inst.requested_function)
        self.assertEqual([b'arg1', 12], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        try:
            commands = json.loads(response)
        except:
            self.fail(b'Invalid JSON generated!')
        else:
            self.assertTrue(isinstance(commands, list))
            self.assertEqual(1, len(commands))
            command_data = commands.pop(0)
            self.assertTrue(b'type' in command_data)
            self.assertEqual(b'alert', command_data[b'type'])

    def test_process_request_calls_invalid_call_event_for_invalid_calls(self):
        from types import FunctionType
        from sijax.helper import json
        call_history = []

        def my_callback(obj_response, arg1, arg2):
            call_history.append(b'call ok')

        def my_callback_with_defaults(obj_response, arg1=138, arg2=15):
            call_history.append(b'defaults ok')

        def my_callback_raising_TypeError(obj_response):
            raise TypeError(b'this should be re-raised by Sijax')

        def my_callback_raising_TypeError2(obj_response):

            def inner():
                raise TypeError(b'this should be re-raised by Sijax')

            inner()

        def invalid_call(obj_response, failed_callback):
            self.assertTrue(isinstance(failed_callback, FunctionType))
            call_history.append(b'invalid %s' % failed_callback.__name__)

        inst = Sijax()
        cls = inst.__class__
        inst.register_callback(b'my_func', my_callback)
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'["arg1", 12]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual(b'my_func', inst.requested_function)
        self.assertEqual([b'arg1', 12], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'["arg1"]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual(b'my_func', inst.requested_function)
        self.assertEqual([b'arg1'], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        try:
            commands = json.loads(response)
        except:
            self.fail(b'Invalid JSON generated!')
        else:
            self.assertTrue(isinstance(commands, list))
            self.assertEqual(1, len(commands))
            command_data = commands.pop(0)
            self.assertTrue(b'type' in command_data)
            self.assertEqual(b'alert', command_data[b'type'])

        inst.register_event(cls.EVENT_INVALID_CALL, invalid_call)
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'[]'})
        self.assertEqual(b'my_func', inst.requested_function)
        self.assertEqual([], inst.request_args)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        inst.register_callback(b'my_func', my_callback_with_defaults)
        response = inst.process_request()
        self.assertTrue(isinstance(response, string_types))
        inst.register_callback(b'my_func', my_callback_raising_TypeError)
        try:
            inst.process_request()
        except TypeError:
            call_history.append(b'TypeError')

        inst.register_callback(b'my_func', my_callback_raising_TypeError2)
        try:
            inst.process_request()
        except TypeError:
            call_history.append(b'TypeError2')

        expected = [b'call ok', b'invalid my_callback', b'defaults ok',
         b'TypeError', b'TypeError2']
        self.assertEqual(expected, call_history)

    def test_new_callbacks_override_old_during_registering(self):
        call_history = []

        def callback_one(obj_response):
            call_history.append(b'one')

        def callback_two(obj_response):
            call_history.append(b'two')

        inst = Sijax()
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.register_callback(b'my_func', callback_one)
        inst.process_request()
        inst.register_callback(b'my_func', callback_two)
        inst.process_request()
        self.assertEqual([b'one', b'two'], call_history)

    def test_mass_registering_from_a_class_works(self):
        call_history = []

        class SijaxHandler(object):

            @staticmethod
            def callback_one(obj_response):
                call_history.append(b'one')

            @staticmethod
            def callback_two(obj_response):
                call_history.append(b'two')

            @classmethod
            def callback_three(cls, obj_response):
                call_history.append(b'three')

        inst = Sijax()
        inst.register_object(SijaxHandler)
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: b'callback_one', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: b'callback_two', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: b'callback_three', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        self.assertEqual([b'one', b'two', b'three'], call_history)

    def test_mass_registering_from_an_object_works(self):
        call_history = []

        class SijaxHandler(object):

            def callback_one(self, obj_response):
                call_history.append(b'one')

            def callback_two(self, obj_response):
                call_history.append(b'two')

        inst = Sijax()
        inst.register_object(SijaxHandler())
        cls = inst.__class__
        inst.set_data({cls.PARAM_REQUEST: b'callback_one', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: b'callback_two', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        self.assertEqual([b'one', b'two'], call_history)

    def test_the_response_class_could_be_changed_during_registration(self):
        call_history = []

        class CustomResponse(BaseResponse):
            pass

        def my_callback(obj_response):
            call_history.append(b'regular')
            self.assertFalse(isinstance(obj_response, CustomResponse))
            self.assertTrue(isinstance(obj_response, BaseResponse))

        def my_custom_callback(obj_response):
            call_history.append(b'custom')
            self.assertTrue(isinstance(obj_response, CustomResponse))

        inst = Sijax()
        cls = inst.__class__
        inst.register_callback(b'my_func', my_callback)
        params_custom = {cls.PARAM_RESPONSE_CLASS: CustomResponse}
        inst.register_callback(b'my_func_custom', my_custom_callback, **params_custom)
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.set_data({cls.PARAM_REQUEST: b'my_func_custom', cls.PARAM_ARGS: b'[]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        self.assertEqual([b'regular', b'custom'], call_history)

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
        inst.register_callback(b'callback', callback, args_extra=('one', 'two'))
        inst.set_data({cls.PARAM_REQUEST: b'callback', cls.PARAM_ARGS: b'["regular"]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        inst.register_callback(b'callback', callback_basic)
        inst.set_data({cls.PARAM_REQUEST: b'callback', cls.PARAM_ARGS: b'["reg2"]'})
        self.assertTrue(inst.is_sijax_request)
        inst.process_request()
        call_history_expected = [
         b'one', b'two', b'regular', b'reg2']
        self.assertEqual(call_history_expected, call_history)

    def test_args_extra_expects_a_list_or_a_tuple(self):
        inst = Sijax()

        def try_args(args_extra, should_succeed):
            success = False
            try:
                inst.register_callback(b'name', lambda r: r, args_extra=args_extra)
                success = True
            except SijaxError:
                pass

            self.assertEqual(should_succeed, success, b'Failure for %s' % repr(args_extra))

        try_args([], True)
        try_args((), True)
        try_args(None, True)
        try_args([b'one item'], True)
        try_args(('one item', ), True)
        try_args([b'one', b'two'], True)
        try_args(('one', 'two'), True)
        try_args([{b'dictionary': b'in', b'the': b'list'}], True)
        try_args(({b'dictionary': b'in', b'the': b'tuple'},), True)
        try_args(b'string', False)
        try_args(True, False)
        try_args(False, False)
        try_args({b'dictionary': b'here'}, False)
        return

    def test_regular_functions_that_yield_are_not_allowed(self):
        inst = Sijax()

        def callback(obj_response):
            yield obj_response

        try:
            inst.execute_callback([], callback)
            self.fail(b"Yielding regular function didn't raise expected exception!")
        except SijaxError:
            pass

    def test_response_method_call_rejects_bad_args(self):
        inst = Sijax()

        def try_call(args_value, should_succeed):

            def callback(obj_response):
                obj_response.call(b'function', args_value)

            success = False
            try:
                inst.execute_callback([], callback)
                success = True
            except SijaxError:
                pass

            self.assertEqual(should_succeed, success, b'Failure for %s' % repr(args_value))

        try_call(None, True)
        try_call([], True)
        try_call([b'arg1', b'arg2', 3, 4, b'arg5'], True)
        try_call((), True)
        try_call(b'arg1', False)
        try_call(1, False)
        try_call({b'dictionary': b'here'}, False)
        return

    def test_init_static_path_helper_works(self):
        import os, sijax
        with temporary_dir() as (static_path):
            init_static_path(static_path)
            version_file = os.path.join(static_path, b'sijax_version')
            if not os.path.exists(version_file):
                self.fail(b'Version file %s does not exist' % version_file)
            with open(version_file) as (fp):
                self.assertEqual(fp.read(), sijax.__version__)
            core_js_file = os.path.join(static_path, b'sijax.js')
            with open(core_js_file, b'w') as (fp):
                fp.write(b'new stuff')
            init_static_path(static_path)
            with open(core_js_file) as (fp):
                self.assertEqual(fp.read(), b'new stuff')
            with open(version_file, b'w') as (fp):
                fp.write(b'another_version_string')
            new_file = os.path.join(static_path, b'extra-file.js')
            self.assertFalse(os.path.exists(new_file))
            with open(new_file, b'w') as (fp):
                fp.write(b'blah')
            self.assertTrue(os.path.exists(new_file))
            init_static_path(static_path)
            with open(core_js_file) as (fp):
                self.assertNotEqual(fp.read(), b'new stuff')
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
            with open(os.path.join(static_path, b'some.file'), b'w') as (fp):
                fp.write(b'blah')
            try_init(static_path, False)
        with temporary_dir() as (static_path):
            with open(os.path.join(static_path, b'some.file'), b'w') as (fp):
                fp.write(b'blah')
            with open(os.path.join(static_path, b'sijax_version'), b'w') as (fp):
                fp.write(b'version_string')
            try_init(static_path, True)

    def test_response_classes_need_to_be_callable(self):
        inst = Sijax()

        def try_response_class(response_class, should_succeed):
            success = False
            try:
                inst.register_callback(b'name', lambda r: r, response_class=response_class)
                success = True
            except SijaxError:
                pass

            self.assertEqual(should_succeed, success, b'Failure for %s' % repr(response_class))

        try_response_class(BaseResponse, True)

        class CustomResponse(BaseResponse):
            pass

        try_response_class(CustomResponse, True)

        def response_factory(*args, **kwargs):
            return CustomResponse(*args, **kwargs)

        try_response_class(response_factory, True)
        try_response_class(None, True)
        try_response_class(b'', False)
        try_response_class(14, False)
        return


class SijaxStreamingTestCase(unittest.TestCase):
    """This tests the StreamingIframeResponse functionality, which is
    used behind the Comet and Upload plugins.
    """

    def test_streaming_functions_return_generators(self):
        from types import GeneratorType
        call_history = []

        def callback_before(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'before')
            obj_response.html(b'#div', b'before html')

        def callback_after(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'after')

        def callback_yielding(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'yielding')
            obj_response.alert(b'test')
            yield obj_response
            obj_response.css(b'#div', b'color', b'red')

        def callback_normal(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'normal')
            obj_response.script(b'.. javascript here..')

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
            call_history.append(b'before_new')
            for i in range(10):
                yield obj_response

            for i in range(2):
                obj_response.alert(b'hey')
                yield obj_response

        inst.register_event(cls.EVENT_BEFORE_PROCESSING, callback_before_new)
        inst.register_event(cls.EVENT_AFTER_PROCESSING, lambda r: r.alert(b'this yields'))
        response = inst.execute_callback([], callback=callback_normal, **options)
        self.assertTrue(isinstance(response, GeneratorType))
        assert_generator_entries_length(response, 4)
        call_history_expected = [
         b'before', b'yielding', b'after',
         b'before_new', b'normal']
        self.assertEqual(call_history_expected, call_history)

    def test_invalid_call_event_works(self):
        from types import GeneratorType, FunctionType
        call_history = []

        def my_callback(obj_response, arg1, arg2):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'call ok')

        def my_callback_raising_TypeError(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            raise TypeError(b'this should be re-raised by Sijax')

        def my_callback_raising_TypeError2(obj_response):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))

            def inner():
                raise TypeError(b'this should be re-raised by Sijax')

            inner()

        def invalid_call(obj_response, failed_callback):
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            self.assertTrue(isinstance(failed_callback, FunctionType))
            call_history.append(b'invalid %s' % failed_callback.__name__)

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
        inst.register_callback(b'my_func', my_callback, **options)
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'["arg1", 12]'})
        self.assertTrue(inst.is_sijax_request)
        self.assertEqual(b'my_func', inst.requested_function)
        self.assertEqual([b'arg1', 12], inst.request_args)
        response = inst.process_request()
        exhaust_generator(response)
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'[]'})
        self.assertEqual(b'my_func', inst.requested_function)
        self.assertEqual([], inst.request_args)
        response = inst.process_request()
        exhaust_generator(response)
        inst.register_callback(b'my_func', my_callback_raising_TypeError, **options)
        try:
            response = inst.process_request()
            exhaust_generator(response)
        except TypeError:
            call_history.append(b'TypeError')

        inst.register_callback(b'my_func', my_callback_raising_TypeError2, **options)
        try:
            response = inst.process_request()
            exhaust_generator(response)
        except TypeError:
            call_history.append(b'TypeError2')

        expected = [b'call ok', b'invalid my_callback',
         b'TypeError', b'TypeError2']
        self.assertEqual(expected, call_history)


class SijaxCometTestCase(unittest.TestCase):
    """Exercises certain Comet specific things. Most of the functionality
    that Comet is based on is tested elsewhere (StreamingIframeResponse).
    """

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
            self.fail(b'Invalid call handler triggered!')

        inst = Sijax()
        cls = inst.__class__
        inst.register_event(cls.EVENT_INVALID_CALL, invalid_call)
        inst.set_data({cls.PARAM_REQUEST: b'my_func', cls.PARAM_ARGS: b'[]'})

        def my_callback(obj_response):
            self.assertTrue(isinstance(obj_response, CometResponse))
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'my_callback')
            call_history.append(type(obj_response).__name__)

        register_comet_callback(inst, b'my_func', my_callback)
        process_request(inst)
        params_custom = {cls.PARAM_RESPONSE_CLASS: CustomResponse}
        register_comet_callback(inst, b'my_func', my_callback, **params_custom)
        process_request(inst)

        class SijaxHandler(object):

            @staticmethod
            def callback_one(obj_response, arg1):
                self.assertTrue(isinstance(obj_response, CustomResponse))
                call_history.append(b'callback_one')
                call_history.append(type(obj_response).__name__)
                call_history.append(arg1)

        register_comet_object(inst, SijaxHandler, **params_custom)
        inst.set_data({cls.PARAM_REQUEST: b'callback_one', cls.PARAM_ARGS: b'[45]'})
        process_request(inst)
        call_history_expected = [
         b'my_callback', b'CometResponse',
         b'my_callback', b'CustomResponse',
         b'callback_one', b'CustomResponse', 45]
        self.assertEqual(call_history_expected, call_history)


class SijaxUploadTestCase(unittest.TestCase):
    """Exercises certain Comet specific things. Most of the functionality
    that Comet is based on is tested elsewhere (StreamingIframeResponse).
    """

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
            self.fail(b'Invalid call handler triggered!')

        inst = Sijax()
        cls = inst.__class__
        inst.register_event(cls.EVENT_INVALID_CALL, invalid_call)

        def my_callback(obj_response, files, form_values):
            self.assertTrue(isinstance(obj_response, UploadResponse))
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'my_callback')
            call_history.append(obj_response.form_id)
            call_history.append(type(obj_response).__name__)
            call_history.append(files[b'file'])
            self.assertEqual({b'form_key': b'value', b'form_key2': 15}, form_values)

        def my_callback2(obj_response, custom_arg1, custom_arg2, form_values):
            self.assertTrue(isinstance(obj_response, UploadResponse))
            self.assertTrue(isinstance(obj_response, StreamingIframeResponse))
            call_history.append(b'custom_callback')
            call_history.append(obj_response.form_id)
            call_history.append(type(obj_response).__name__)
            call_history.append(custom_arg1)
            call_history.append(custom_arg2)
            self.assertEqual({b'form_key': b'value', b'form_key2': 15}, form_values)

        form_id = b'my_form'
        public_callback_name = func_name_by_form_id(form_id)
        request_args_json = b'["%s"]' % form_id
        post = {}
        post[cls.PARAM_REQUEST] = public_callback_name
        post[cls.PARAM_ARGS] = request_args_json
        post[b'form_key'] = b'value'
        post[b'form_key2'] = 15
        inst.set_data(post)
        files = {b'file': b'object', b'passed': b'here'}
        register_upload_callback(inst, form_id, my_callback, args_extra=(files,))
        process_request(inst)
        params_custom = {cls.PARAM_RESPONSE_CLASS: CustomResponse}
        register_upload_callback(inst, form_id, my_callback2, args_extra=('custom1',
                                                                          'custom2'), **params_custom)
        process_request(inst)
        call_history_expected = [
         b'my_callback', form_id, b'UploadResponse', b'object',
         b'custom_callback', form_id, b'CustomResponse', b'custom1', b'custom2']
        self.assertEqual(call_history_expected, call_history)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SijaxMainTestCase))
    suite.addTest(unittest.makeSuite(SijaxStreamingTestCase))
    suite.addTest(unittest.makeSuite(SijaxCometTestCase))
    suite.addTest(unittest.makeSuite(SijaxUploadTestCase))
    return suite


if __name__ == b'__main__':
    unittest.main(defaultTest=b'suite')