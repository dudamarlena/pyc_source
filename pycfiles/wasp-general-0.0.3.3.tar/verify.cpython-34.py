# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/verify.py
# Compiled at: 2017-12-20 09:57:03
# Size of source mod 2**32: 18126 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import sys, os
from inspect import getfullargspec, isclass, isfunction, getsource
from decorator import decorator

class Verifier:
    __doc__ = " Base class for verifier implementation.\n\n\tVerifiers are classes, that generates decorators (which are later used for runtime function arguments\n\tchecking). Derived classes (such as :class:`.TypeVerifier`, :class:`SubclassVerifier` and\n\t:class:`ValueVerifier`) check arguments for type and/or value validity. But each derived class uses\n\tits own syntax for check declaration (see :meth:`.Verifier.check`).\n\n\tSame checks can be grouped into one sentence if they are used for different arguments. Each statement can\n\tbe marked by tag or tags for runtime disabling. If statement doesn't have tag then it always run checks.\n\n\tChecks can be simple (implemented by lambda-statements) or complex\n\t(implemented by standalone functions or classes). Because target function is decorated for checking it is\n\tpossible to run checks sequentially.\n\n\tExample: ::\n\n\t\t@verify_type(a=int, b=str, d=(int, None), e=float)\n\t\t@verify_subclass(c=A, args=B)\n\t\t@verify_value(a=(lambda x: x > 5, lambda x: x < 10), args=lambda x: x > 0)\n\t\t@verify_value(c=lambda x: x.a == 'foo', d=lambda x: x is None or x < 0)\n\t\tdef foo(a, b, c, d=None, *args, **kwargs):\n\t\t\tpass\n\t"
    __default_environment_var__ = 'WASP_VERIFIER_DISABLE_CHECKS'
    __tags_delimiter__ = ':'

    def __init__(self, *tags, env_var=None, silent_checks=False):
        """Construct a new :class:`.Verifier`

                :param tags: Tags to mark this checks. Now only strings are suitable.
                :param env_var: Environment variable name that is used for check bypassing. If is None, then default            value is used :attr:`.Verifier.__default_environment_var__`
                :param silent_checks: If it is not True, then debug information will be printed to stderr.
                """
        self._tags = list(tags)
        self._env_var = env_var if env_var is not None else self.__class__.__default_environment_var__
        self._silent_checks = silent_checks

    def decorate_disabled(self):
        """ Return True if this decoration must be omitted, otherwise - False.
                This class searches for tags values in environment variable
                (:attr:`.Verifier.__default_environment_var__`), Derived class can implement any logic

                :return: bool
                """
        if self._env_var not in os.environ or len(self._tags) == 0:
            return False
        env = os.environ[self._env_var].split(self.__class__.__tags_delimiter__)
        for tag in self._tags:
            if tag not in env:
                return False

        return True

    def check(self, arg_spec, arg_name, decorated_function):
        """Return callable object that takes single value - future argument. This callable must raise
                an exception if error occurs. It is recommended to return None if everything is OK

                :param arg_spec: specification that is used to describe check like types, lambda-functions,             list of types just anything (see :meth:`.Verifier.decorator`)
                :param arg_name: parameter name from decorated function
                :param decorated_function: target function (function to decorate)

                :return: None
                """
        return lambda x: None

    def _args_checks_gen(self, decorated_function, function_spec, arg_specs):
        """ Generate checks for positional argument testing

                :param decorated_function: function decorator
                :param function_spec: function inspect information
                :param arg_specs: argument specification (same as arg_specs in :meth:`.Verifier.decorate`)

                :return: internal structure, that is used by :meth:`.Verifier._args_checks_test`
                """
        inspected_args = function_spec.args
        args_check = {}
        for i in range(len(inspected_args)):
            arg_name = inspected_args[i]
            if arg_name in arg_specs.keys():
                args_check[arg_name] = self.check(arg_specs[arg_name], arg_name, decorated_function)
                continue

        return args_check

    def _args_checks_test(self, original_function, function_spec, checks, args, arg_specs):
        """ Test positional arguments by a generated checks

                :param original_function: original function, that was decorated
                :param function_spec: function inspect information
                :param checks: tests, that was generated by the :meth:`.Verifier._args_checks_gen`
                :param args: positional arguments to check (with varargs)
                :param arg_specs: argument specification (same as arg_specs in :meth:`.Verifier.decorate`)

                :return: None
                """
        inspected_args = function_spec.args
        for i in range(len(inspected_args)):
            param_name = inspected_args[i]
            if param_name in checks:
                try:
                    checks[param_name](args[i])
                except Exception as e:
                    self.help_info(e, original_function, param_name, arg_specs[param_name])
                    raise

                continue

    def _varargs_checks_gen(self, decorated_function, function_spec, arg_specs):
        """ Generate checks for positional variable argument (varargs) testing

                :param decorated_function: function decorator
                :param function_spec: function inspect information
                :param arg_specs: argument specification (same as arg_specs in :meth:`.Verifier.decorate`)

                :return: internal structure, that is used by :meth:`.Verifier._varargs_checks_test`
                """
        inspected_varargs = function_spec.varargs
        if inspected_varargs is not None and inspected_varargs in arg_specs.keys():
            return self.check(arg_specs[inspected_varargs], inspected_varargs, decorated_function)

    def _varargs_checks_test(self, original_function, function_spec, check, args, arg_specs):
        """ Test varargs by a generated check

                :param original_function: original function, that was decorated
                :param function_spec: function inspect information
                :param check: test, that was generated by the :meth:`.Verifier._varargs_checks_gen`
                :param args: positional arguments to check (all of them)
                :param arg_specs: argument specification (same as arg_specs in :meth:`.Verifier.decorate`)

                :return: None
                """
        inspected_args = function_spec.args
        inspected_varargs = function_spec.varargs
        if inspected_varargs is not None:
            if check is not None:
                for i in range(len(inspected_args), len(args)):
                    try:
                        check(args[i])
                    except Exception as e:
                        self.help_info(e, original_function, inspected_varargs, arg_specs[inspected_varargs])
                        raise

    def _kwargs_checks_gen(self, decorated_function, function_spec, arg_specs):
        """ Generate checks for keyword argument testing

                :param decorated_function: function decorator
                :param function_spec: function inspect information
                :param arg_specs: argument specification (same as arg_specs in :meth:`.Verifier.decorate`)

                :return: internal structure, that is used by :meth:`.Verifier._kwargs_checks_test`
                """
        args_names = []
        args_names.extend(function_spec.args)
        if function_spec.varargs is not None:
            args_names.append(function_spec.args)
        args_check = {}
        for arg_name in arg_specs.keys():
            if arg_name not in args_names:
                args_check[arg_name] = self.check(arg_specs[arg_name], arg_name, decorated_function)
                continue

        return args_check

    def _kwargs_checks_test(self, original_function, checks, kwargs, arg_specs):
        """ Test keyword arguments by a generated checks

                :param original_function: original function, that was decorated
                :param checks: tests, that was generated by the :meth:`.Verifier._kwargs_checks_gen`
                :param kwargs: keyword arguments to check
                :param arg_specs: argument specification (same as arg_specs in :meth:`.Verifier.decorate`)

                :return: None
                """
        for kw_key, kw_value in kwargs.items():
            if kw_key in checks.keys():
                try:
                    checks[kw_key](kw_value)
                except Exception as e:
                    self.help_info(e, original_function, kw_key, arg_specs[kw_key])
                    raise

                continue

    def decorator(self, **arg_specs):
        """ Return decorator that can decorate target function

                :param arg_specs: dictionary where keys are parameters name and values are theirs specification.                Specific specification is passed as is to :meth:`Verifier.check` method with corresponding              parameter name.

                :return: function
                """
        if self.decorate_disabled() is True:

            def empty_decorator(decorated_function):
                return decorated_function

            return empty_decorator

        def first_level_decorator(decorated_function):
            function_spec = getfullargspec(decorated_function)
            args_checks = self._args_checks_gen(decorated_function, function_spec, arg_specs)
            varargs_check = self._varargs_checks_gen(decorated_function, function_spec, arg_specs)
            kwargs_checks = self._kwargs_checks_gen(decorated_function, function_spec, arg_specs)

            def second_level_decorator(original_function, *args, **kwargs):
                self._args_checks_test(original_function, function_spec, args_checks, args, arg_specs)
                self._varargs_checks_test(original_function, function_spec, varargs_check, args, arg_specs)
                self._kwargs_checks_test(original_function, kwargs_checks, kwargs, arg_specs)
                return original_function(*args, **kwargs)

            return decorator(second_level_decorator)(decorated_function)

        return first_level_decorator

    def help_info(self, exc, decorated_function, arg_name, arg_spec):
        """ Print debug information to stderr. (Do nothing if object was constructed with silent_checks=True)

                :param exc: raised exception
                :param decorated_function: target function (function to decorate)
                :param arg_name: function parameter name
                :param arg_spec: function parameter specification

                :return: None
                """
        if self._silent_checks is not True:
            print('Exception raised:', file=sys.stderr)
            print(str(exc), file=sys.stderr)
            fn_name = Verifier.function_name(decorated_function)
            print('Decorated function: %s' % fn_name, file=sys.stderr)
            if decorated_function.__doc__ is not None:
                print('Decorated function docstrings:', file=sys.stderr)
                print(decorated_function.__doc__, file=sys.stderr)
            print('Argument "%s" specification:' % arg_name, file=sys.stderr)
            if isfunction(arg_spec):
                print(getsource(arg_spec), file=sys.stderr)
            else:
                print(str(arg_spec), file=sys.stderr)
            print('', file=sys.stderr)

    @staticmethod
    def function_name(fn):
        """ Return function name in pretty style

                :param fn: source function
                :return: str
                """
        fn_name = fn.__name__
        if hasattr(fn, '__qualname__'):
            return fn.__qualname__
        if hasattr(fn, '__self__'):
            owner = fn.__self__
            if isclass(owner) is False:
                owner = owner.__class__
            return '%s.%s' % (owner.__name__, fn_name)
        return fn_name


class TypeVerifier(Verifier):
    __doc__ = ' Verifier that is used for type verification. Checks parameter if it is instance of specified class or\n\tclasses. Specification accepts type or list/tuple/set of types\n\n\tExample: ::\n\n\t\t@verify_type(a=int, b=str, d=(int, None), e=float)\n\t\tdef foo(a, b, c, d=None, **kwargs):\n\t\t\tpass\n\t'

    def check(self, type_spec, arg_name, decorated_function):
        """ Return callable that checks function parameter for type validity. Checks parameter if it is
                instance of specified class or classes

                :param type_spec: type or list/tuple/set of types
                :param arg_name: function parameter name
                :param decorated_function: target function
                :return: function
                """

        def raise_exception(x_spec):
            exc_text = 'Argument "%s" for function "%s" has invalid type' % (
             arg_name, Verifier.function_name(decorated_function))
            exc_text += ' (%s should be %s)' % (x_spec, type_spec)
            raise TypeError(exc_text)

        if isinstance(type_spec, (tuple, list, set)):
            for single_type in type_spec:
                if single_type is not None and isclass(single_type) is False:
                    raise RuntimeError('Invalid specification. Must be type or tuple/list/set of types')
                    continue

            if None in type_spec:
                type_spec = tuple(filter(lambda x: x is not None, type_spec))
                return --- This code section failed: ---

 L. 341         0  LOAD_FAST                'x'
                3  LOAD_CONST               None
                6  COMPARE_OP               is
                9  POP_JUMP_IF_TRUE     39  'to 39'
               12  LOAD_GLOBAL              isinstance
               15  LOAD_FAST                'x'
               18  LOAD_GLOBAL              tuple
               21  LOAD_DEREF               'type_spec'
               24  CALL_FUNCTION_1       1  '1 positional, 0 named'
               27  CALL_FUNCTION_2       2  '2 positional, 0 named'
               30  LOAD_CONST               True
               33  COMPARE_OP               is
             36_0  COME_FROM             9  '9'
               36  POP_JUMP_IF_FALSE    43  'to 43'
               39  LOAD_CONST               None
               42  RETURN_END_IF_LAMBDA
             43_0  COME_FROM            36  '36'

 L. 342        43  LOAD_DEREF               'raise_exception'
               46  LOAD_GLOBAL              str
               49  LOAD_GLOBAL              type
               52  LOAD_FAST                'x'
               55  CALL_FUNCTION_1       1  '1 positional, 0 named'
               58  CALL_FUNCTION_1       1  '1 positional, 0 named'
               61  CALL_FUNCTION_1       1  '1 positional, 0 named'
               64  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            else:
                return --- This code section failed: ---

 L. 344         0  LOAD_GLOBAL              isinstance
                3  LOAD_FAST                'x'
                6  LOAD_GLOBAL              tuple
                9  LOAD_DEREF               'type_spec'
               12  CALL_FUNCTION_1       1  '1 positional, 0 named'
               15  CALL_FUNCTION_2       2  '2 positional, 0 named'
               18  LOAD_CONST               True
               21  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE    31  'to 31'
               27  LOAD_CONST               None
               30  RETURN_END_IF_LAMBDA
             31_0  COME_FROM            24  '24'

 L. 345        31  LOAD_DEREF               'raise_exception'
               34  LOAD_GLOBAL              str
               37  LOAD_GLOBAL              type
               40  LOAD_FAST                'x'
               43  CALL_FUNCTION_1       1  '1 positional, 0 named'
               46  CALL_FUNCTION_1       1  '1 positional, 0 named'
               49  CALL_FUNCTION_1       1  '1 positional, 0 named'
               52  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
        else:
            if isclass(type_spec):
                return --- This code section failed: ---

 L. 347         0  LOAD_GLOBAL              isinstance
                3  LOAD_FAST                'x'
                6  LOAD_DEREF               'type_spec'
                9  CALL_FUNCTION_2       2  '2 positional, 0 named'
               12  LOAD_CONST               True
               15  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    25  'to 25'
               21  LOAD_CONST               None
               24  RETURN_END_IF_LAMBDA
             25_0  COME_FROM            18  '18'

 L. 348        25  LOAD_DEREF               'raise_exception'
               28  LOAD_GLOBAL              str
               31  LOAD_GLOBAL              type
               34  LOAD_FAST                'x'
               37  CALL_FUNCTION_1       1  '1 positional, 0 named'
               40  CALL_FUNCTION_1       1  '1 positional, 0 named'
               43  CALL_FUNCTION_1       1  '1 positional, 0 named'
               46  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            raise RuntimeError('Invalid specification. Must be type or tuple/list/set of types')


class SubclassVerifier(Verifier):
    __doc__ = ' Verifier that is used for type verification. Checks parameter if it is class or subclass of\n\tspecified class or classes. Specification accepts type or list/tuple/set of types\n\n\tExample: ::\n\n\t\t@verify_subclass(c=A, e=(A, D))\n\t\tdef foo(a, b, c, d=None, **kwargs):\n\t\t\tpass\n\t'

    def check(self, type_spec, arg_name, decorated_function):
        """ Return callable that checks function parameter for class validity. Checks parameter if it is
                class or subclass of specified class or classes

                :param type_spec: type or list/tuple/set of types
                :param arg_name: function parameter name
                :param decorated_function: target function
                :return: function
                """

        def raise_exception(text_spec):
            exc_text = 'Argument "%s" for function "%s" has invalid type' % (
             arg_name, Verifier.function_name(decorated_function))
            exc_text += ' (%s)' % text_spec
            raise TypeError(exc_text)

        if isinstance(type_spec, (tuple, list, set)):
            for single_type in type_spec:
                if single_type is not None and isclass(single_type) is False:
                    raise RuntimeError('Invalid specification. Must be type or tuple/list/set of types')
                    continue

            if None in type_spec:
                type_spec = tuple(filter(lambda x: x is not None, type_spec))
                return --- This code section failed: ---

 L. 390         0  LOAD_FAST                'x'
                3  LOAD_CONST               None
                6  COMPARE_OP               is
                9  POP_JUMP_IF_TRUE     51  'to 51'
               12  LOAD_GLOBAL              isclass
               15  LOAD_FAST                'x'
               18  CALL_FUNCTION_1       1  '1 positional, 0 named'
               21  LOAD_CONST               True
               24  COMPARE_OP               is
               27  POP_JUMP_IF_FALSE    55  'to 55'
               30  LOAD_GLOBAL              issubclass
               33  LOAD_FAST                'x'
               36  LOAD_DEREF               'type_spec'
               39  CALL_FUNCTION_2       2  '2 positional, 0 named'
               42  LOAD_CONST               True
               45  COMPARE_OP               is
             48_0  COME_FROM            27  '27'
             48_1  COME_FROM             9  '9'
               48  POP_JUMP_IF_FALSE    55  'to 55'
               51  LOAD_CONST               None
               54  RETURN_END_IF_LAMBDA
             55_0  COME_FROM            48  '48'

 L. 391        55  LOAD_DEREF               'raise_exception'
               58  LOAD_GLOBAL              str
               61  LOAD_FAST                'x'
               64  CALL_FUNCTION_1       1  '1 positional, 0 named'
               67  CALL_FUNCTION_1       1  '1 positional, 0 named'
               70  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            else:
                return --- This code section failed: ---

 L. 393         0  LOAD_GLOBAL              isclass
                3  LOAD_FAST                'x'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  LOAD_CONST               True
               12  COMPARE_OP               is
               15  POP_JUMP_IF_FALSE    43  'to 43'
               18  LOAD_GLOBAL              issubclass
               21  LOAD_FAST                'x'
               24  LOAD_DEREF               'type_spec'
               27  CALL_FUNCTION_2       2  '2 positional, 0 named'
               30  LOAD_CONST               True
               33  COMPARE_OP               is
             36_0  COME_FROM            15  '15'
               36  POP_JUMP_IF_FALSE    43  'to 43'
               39  LOAD_CONST               None
               42  RETURN_END_IF_LAMBDA
             43_0  COME_FROM            36  '36'

 L. 394        43  LOAD_DEREF               'raise_exception'
               46  LOAD_GLOBAL              str
               49  LOAD_FAST                'x'
               52  CALL_FUNCTION_1       1  '1 positional, 0 named'
               55  CALL_FUNCTION_1       1  '1 positional, 0 named'
               58  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
        else:
            if isclass(type_spec):
                return --- This code section failed: ---

 L. 396         0  LOAD_GLOBAL              isclass
                3  LOAD_FAST                'x'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  LOAD_CONST               True
               12  COMPARE_OP               is
               15  POP_JUMP_IF_FALSE    43  'to 43'
               18  LOAD_GLOBAL              issubclass
               21  LOAD_FAST                'x'
               24  LOAD_DEREF               'type_spec'
               27  CALL_FUNCTION_2       2  '2 positional, 0 named'
               30  LOAD_CONST               True
               33  COMPARE_OP               is
             36_0  COME_FROM            15  '15'
               36  POP_JUMP_IF_FALSE    43  'to 43'
               39  LOAD_CONST               None
               42  RETURN_END_IF_LAMBDA
             43_0  COME_FROM            36  '36'

 L. 397        43  LOAD_DEREF               'raise_exception'
               46  LOAD_GLOBAL              str
               49  LOAD_FAST                'x'
               52  CALL_FUNCTION_1       1  '1 positional, 0 named'
               55  CALL_FUNCTION_1       1  '1 positional, 0 named'
               58  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
            raise RuntimeError('Invalid specification. Must be type or tuple/list/set of types')


class ValueVerifier(Verifier):
    __doc__ = " Verifier that is used for value verification. Checks parameter if its value passes specified restrictions.\n\tSpecification accepts function or list/tuple/set of functions. Each function must accept one parameter and\n\tmust return True or False if it passed restrictions or not.\n\n\tExample: ::\n\n\t\t@verify_value(a=(lambda x: x > 5, lambda x: x < 10))\n\t\t@verify_value(c=lambda x: x.a == 'foo', d=lambda x: x is None or x < 0)\n\t\tdef foo(a, b, c, d=None, **kwargs):\n\t\tpass\n\t"

    def check(self, value_spec, arg_name, decorated_function):
        """ Return callable that checks function parameter for value validity. Checks parameter if its value
                passes specified restrictions.

                :param value_spec: function or list/tuple/set of functions. Each function must accept one parameter and                 must return True or False if it passed restrictions or not.
                :param arg_name: function parameter name
                :param decorated_function: target function
                :return: function
                """

        def raise_exception(text_spec):
            exc_text = 'Argument "%s" for function "%s" has invalid value' % (
             arg_name, Verifier.function_name(decorated_function))
            exc_text += ' (%s)' % text_spec
            raise ValueError(exc_text)

        if isinstance(value_spec, (tuple, list, set)):
            for single_value in value_spec:
                if isfunction(single_value) is False:
                    raise RuntimeError('Invalid specification. Must be function or tuple/list/set of functions')
                    continue

            def check(x):
                for f in value_spec:
                    if f(x) is not True:
                        raise_exception(str(x))
                        continue

            return check
        if isfunction(value_spec):
            return --- This code section failed: ---

 L. 449         0  LOAD_DEREF               'value_spec'
                3  LOAD_FAST                'x'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  LOAD_CONST               True
               12  COMPARE_OP               is
               15  POP_JUMP_IF_FALSE    22  'to 22'
               18  LOAD_CONST               None
               21  RETURN_END_IF_LAMBDA
             22_0  COME_FROM            15  '15'
               22  LOAD_DEREF               'raise_exception'
               25  LOAD_GLOBAL              str
               28  LOAD_FAST                'x'
               31  CALL_FUNCTION_1       1  '1 positional, 0 named'
               34  CALL_FUNCTION_1       1  '1 positional, 0 named'
               37  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
        raise RuntimeError('Invalid specification. Must be function or tuple/list/set of functions')


def verify_type(*tags, **type_kwargs):
    """ Shortcut for :class:`.TypeVerifier`

        :param tags: verification tags. See :meth:`.Verifier.__init__`
        :param type_kwargs: verifier specification. See :meth:`.TypeVerifier.check`
        :return: decorator (function)
        """
    return TypeVerifier(*tags).decorator(**type_kwargs)


def verify_subclass(*tags, **type_kwargs):
    """ Shortcut for :class:`.SubclassVerifier`

        :param tags: verification tags. See :meth:`.Verifier.__init__`
        :param type_kwargs: verifier specification. See :meth:`.SubclassVerifier.check`
        :return: decorator (function)
        """
    return SubclassVerifier(*tags).decorator(**type_kwargs)


def verify_value(*tags, **type_kwargs):
    """ Shortcut for :class:`.ValueVerifier`

        :param tags: verification tags. See :meth:`.Verifier.__init__`
        :param type_kwargs: verifier specification. See :meth:`.ValueVerifier.check`
        :return: decorator (function)
        """
    return ValueVerifier(*tags).decorator(**type_kwargs)