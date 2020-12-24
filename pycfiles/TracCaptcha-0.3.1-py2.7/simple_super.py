# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/lib/simple_super.py
# Compiled at: 2010-06-12 08:49:15
__all__ = [
 'SuperProxy']
import inspect, re, sys, traceback, warnings
try:
    reversed
except NameError:

    def reversed(an_iterable):
        copied_iterable = list(an_iterable)
        copied_iterable.reverse()
        return copied_iterable


class SmartMethodCall(object):

    def __init__(self, method, *vargs, **kwargs):
        self._method = method
        self._vargs, self._kwargs = self._arguments_for_call(vargs, kwargs)

    def call_with_correct_parameters(self):
        return self._method(*self._vargs, **self._kwargs)

    def _arguments_for_call(self, vargs, kwargs):
        if self._did_specify_arguments_explicitely(vargs, kwargs):
            return (vargs, kwargs)
        return self._arguments_for_super_method()

    def _did_specify_arguments_explicitely--- This code section failed: ---

 L.  84         0  LOAD_FAST             1  'vargs'
                3  POP_JUMP_IF_TRUE     12  'to 12'
                6  LOAD_FAST             2  'kwargs'
              9_0  COME_FROM             3  '3'
                9  POP_JUMP_IF_FALSE    16  'to 16'

 L.  85        12  LOAD_GLOBAL           0  'True'
               15  RETURN_VALUE     
             16_0  COME_FROM             9  '9'

 L.  89        16  LOAD_GLOBAL           1  'inspect'
               19  LOAD_ATTR             2  'getframeinfo'
               22  LOAD_GLOBAL           3  'sys'
               25  LOAD_ATTR             4  '_getframe'
               28  LOAD_CONST               4
               31  CALL_FUNCTION_1       1  None
               34  CALL_FUNCTION_1       1  None
               37  STORE_FAST            3  'frame_info'

 L.  90        40  LOAD_FAST             3  'frame_info'
               43  LOAD_CONST               3
               46  BINARY_SUBSCR    
               47  STORE_FAST            4  'caller_source_lines'

 L.  91        50  LOAD_FAST             4  'caller_source_lines'
               53  LOAD_CONST               None
               56  COMPARE_OP            8  is
               59  POP_JUMP_IF_FALSE    87  'to 87'

 L.  92        62  LOAD_GLOBAL           6  'warnings'
               65  LOAD_ATTR             7  'warn'
               68  LOAD_CONST               'No source found for '
               71  LOAD_FAST             3  'frame_info'
               74  LOAD_CONST               0
               77  BINARY_SUBSCR    
               78  BINARY_ADD       
               79  CALL_FUNCTION_1       1  None
               82  POP_TOP          

 L.  93        83  LOAD_GLOBAL           8  'False'
               86  RETURN_END_IF    
             87_0  COME_FROM            59  '59'

 L.  94        87  LOAD_FAST             4  'caller_source_lines'
               90  LOAD_CONST               0
               93  BINARY_SUBSCR    
               94  STORE_FAST            5  'caller_source_code'

 L.  95        97  LOAD_GLOBAL           9  're'
              100  LOAD_ATTR            10  'search'
              103  LOAD_CONST               'self.super\\((.*?)\\)'
              106  LOAD_FAST             5  'caller_source_code'
              109  CALL_FUNCTION_2       2  None
              112  STORE_FAST            6  'match'

 L.  96       115  LOAD_FAST             6  'match'
              118  LOAD_CONST               None
              121  COMPARE_OP            9  is-not
              124  POP_JUMP_IF_TRUE    142  'to 142'
              127  LOAD_ASSERT              AssertionError
              130  LOAD_GLOBAL          12  'repr'
              133  LOAD_FAST             5  'caller_source_code'
              136  CALL_FUNCTION_1       1  None
              139  RAISE_VARARGS_2       2  None

 L.  97       142  LOAD_GLOBAL           9  're'
              145  LOAD_ATTR            10  'search'
              148  LOAD_CONST               '\\S'
              151  LOAD_FAST             6  'match'
              154  LOAD_ATTR            13  'group'
              157  LOAD_CONST               1
              160  CALL_FUNCTION_1       1  None
              163  CALL_FUNCTION_2       2  None
              166  POP_JUMP_IF_FALSE   173  'to 173'

 L.  98       169  LOAD_GLOBAL           0  'True'
              172  RETURN_END_IF    
            173_0  COME_FROM           166  '166'

 L.  99       173  LOAD_GLOBAL           8  'False'
              176  RETURN_VALUE     

Parse error at or near `LOAD_GLOBAL' instruction at offset 173

    def _arguments_for_super_method(self):
        if not inspect.isroutine(self._method):
            return ([], {})
        else:
            args, varargs, varkw, defaults = inspect.getargspec(self._method)
            if len(args) == 1 and varargs is None:
                return ([], {})
            return self._find_arguments_for_called_method()

    def _find_arguments_for_called_method(self):
        caller_frame = sys._getframe(5)
        caller_arg_names, caller_varg_name, caller_kwarg_name, caller_arg_values = inspect.getargvalues(caller_frame)
        callee_arg_names, callee_varargs, callee_kwarg_name, callee_defaults = inspect.getargspec(self._method)
        vargs = []
        kwargs = {}
        if len(caller_arg_names) > len(callee_arg_names):
            for name in caller_arg_names[len(callee_arg_names):]:
                kwargs[name] = caller_arg_values[name]

        for name in caller_arg_names[1:len(callee_arg_names)]:
            vargs.append(caller_arg_values[name])

        if caller_varg_name:
            vargs.extend(caller_arg_values[caller_varg_name])
        if caller_kwarg_name:
            kwargs.update(caller_arg_values[caller_kwarg_name])
        return (vargs, kwargs)


class SuperFinder(object):

    def super_method(self, method_name=None):
        caller_self = self._find_caller_self()
        code = sys._getframe(2).f_code
        if method_name is None:
            method_name = code.co_name
        super_class = self._find_class(caller_self, code)
        return getattr(super(super_class, caller_self), method_name)

    def _find_caller_self(self):
        arg_names, varg_name, kwarg_name, arg_values = inspect.getargvalues(sys._getframe(3))
        return arg_values[arg_names[0]]

    def _points_to_this_function(self, code, func):
        is_python2x = 2 == sys.version_info[0]
        if is_python2x:
            return self._points_to_this_function_py2x(code, func)
        return self._points_to_this_function_py3k(code, func)

    def _points_to_this_function_py2x(self, code, func):
        if hasattr(func, 'im_func'):
            other_code = func.im_func.func_code
            if id(code) == id(other_code):
                return True
        return False

    def _points_to_this_function_py3k(self, code, func):
        other_code = inspect.getmembers(func)[4][1]
        return id(code) == id(other_code)

    def _find_class(self, instance, code):
        method_name = code.co_name
        for klass in reversed(inspect.getmro(instance.__class__)):
            if hasattr(klass, method_name):
                func = getattr(klass, method_name)
                if self._points_to_this_function(code, func):
                    return klass


class SuperProxy(object):
    """This has as few methods as possible, to serve as an ideal proxy."""

    def __call__(self, *vargs, **kwargs):
        method = SuperFinder().super_method()
        return SmartMethodCall(method, *vargs, **kwargs).call_with_correct_parameters()

    def __getattr__(self, method_name):
        return SuperFinder().super_method(method_name=method_name)


import unittest

class Super(object):
    super = SuperProxy()

    def __init__(self):
        self.did_call_super = False

    def method(self, *vargs, **kwargs):
        self.did_call_super = True
        return self

    def verify(self):
        assert self.did_call_super


class SuperTests(unittest.TestCase):

    def test_no_arguments(self):

        class Upper(Super):

            def method(self):
                return self.super()

        class Lower(Upper):

            def method(self):
                return self.super()

        Lower().method().verify()

    def test_positional_argument(self):

        class Upper(Super):

            def method(self, arg, *vargs):
                assert 'fnord' == arg
                assert (23, 42) == vargs
                return self.super()

        class Lower(Upper):

            def method(self, arg, *vargs):
                self.super(arg, *vargs)
                return self.super()

        Lower().method('fnord', 23, 42).verify()

    def test_test_keyword_argument(self):

        class Upper(Super):

            def method(self, arg1, arg2, **kwargs):
                assert 'fnord' == arg1
                assert 23 == arg2
                assert {'foo': 'bar'}
                return self.super()

        class Lower(Upper):

            def method(self, arg1, arg2, **kwargs):
                self.super(arg1=arg1, arg2=arg2, **kwargs)
                return self.super()

        Lower().method(arg1='fnord', arg2=23, foo='bar').verify()

    def test_positional_variable_and_keyword_arguments(self):

        class Upper(Super):

            def method(self, arg, *vargs, **kwargs):
                assert 'fnord' == arg
                assert (23, 42) == vargs
                assert {'foo': 'bar'} == kwargs
                return self.super()

        class Lower(Upper):

            def method(self, arg, *vargs, **kwargs):
                self.super(arg, *vargs, **kwargs)
                return self.super()

        Lower().method('fnord', 23, 42, foo='bar').verify()

    def test_default_arguments(self):

        class Upper(Super):

            def method(self, arg):
                assert 'fnord' == arg
                return self.super()

        class Lower(Upper):

            def method(self, arg='fnord'):
                self.super(arg)
                return self.super()

        Lower().method().verify()

    def test_can_change_arguments_to_super(self):

        class Upper(Super):

            def method(self, arg):
                assert 'fnord' == arg
                return self.super()

        class Lower(Upper):

            def method(self, arg):
                return self.super('fnord')

        Lower().method('foobar').verify()

    def test_super_has_fewer_arguments(self):

        class Upper(Super):

            def method(self, arg):
                assert 23 == arg
                return self.super()

        class Lower(Upper):

            def method(self, arg1, arg2):
                return self.super(arg1)

        Lower().method(23, 42).verify()

    def test_can_call_arbitrary_method_on_super(self):

        class Upper(Super):

            def foo(self):
                return self.super.method()

        class Lower(Upper):

            def bar(self):
                return self.super.foo()

        Lower().bar().verify()

    def test_can_use_super_in_init(self):

        class Upper(object):
            super = SuperProxy()

            def __init__(self):
                self.super()
                self.did_call_super = True

        class Lower(Upper):

            def __init__(self):
                return self.super()

        self.assertEqual(True, Lower().did_call_super)

    def test_do_not_pass_arguments_by_default_if_lower_doesnt_have_any(self):

        class Upper(Super):

            def foo(self):
                return self.super.method()

        class Lower(Upper):

            def foo(self, default=None, *args, **kwargs):
                return self.super()

        Lower().foo().verify()

    def test_use_correct_default_arguments_for_super_method(self):

        class Upper(Super):

            def foo--- This code section failed: ---

 L. 337         0  LOAD_FAST             1  'important_key'
                3  LOAD_CONST               'fnord'
                6  COMPARE_OP            2  ==
                9  POP_JUMP_IF_TRUE     27  'to 27'
               12  LOAD_ASSERT              AssertionError
               15  LOAD_GLOBAL           1  'repr'
               18  LOAD_FAST             1  'important_key'
               21  CALL_FUNCTION_1       1  None
               24  RAISE_VARARGS_2       2  None

 L. 338        27  LOAD_FAST             0  'self'
               30  LOAD_ATTR             2  'super'
               33  LOAD_ATTR             3  'method'
               36  CALL_FUNCTION_0       0  None
               39  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 39

        class Lower(Upper):

            def foo(self, some_paramter=None, *args, **kwargs):
                return self.super(*args, **kwargs)

        Lower().foo().verify()

    def test_add_arguments_to_kwargs_if_upper_has_less_named_arguments_than_lower(self):

        class Upper(Super):

            def foo(self, some_parameter, **kwargs):
                assert 'another_parameter' in kwargs
                assert kwargs['another_parameter'] == 'fnord'
                return self.super.method()

        class Lower(Upper):

            def foo(self, some_parameter, another_parameter='fnord', **kwargs):
                return self.super()

        Lower().foo(None).verify()
        return


if __name__ == '__main__':
    unittest.main()