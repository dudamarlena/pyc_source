# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/utils/decorators.py
# Compiled at: 2019-07-19 10:02:19
# Size of source mod 2**32: 20255 bytes
from __future__ import print_function, division, absolute_import
import os, sys, inspect, marshal, warnings
from array import array
from six.moves import builtins
from collections import OrderedDict, defaultdict
from collections import MutableMapping, Mapping
from functools import wraps, partial
from six import string_types
from six.moves import zip, zip_longest, cPickle
import types, numpy as np
__all__ = [
 'typecheck',
 'autoattr',
 'abstractstatic',
 'functionable',
 'singleton']

def _info(fname, expected, actual, flag):
    """Convenience function outputs nicely formatted error/warning msg."""

    def to_str(t):
        s = []
        for i in t:
            if not isinstance(i, (tuple, list)):
                s.append(str(i).split("'")[1])
            else:
                s.append('(' + ', '.join([str(j).split("'")[1] for j in i]) + ')')

        return ', '.join(s)

    expected, actual = to_str(expected), to_str(actual)
    ftype = 'method'
    msg = "'{}' {} ".format(fname, ftype) + ('inputs', 'outputs')[flag] + ' ({}), but '.format(expected) + ('was given',
                                                                                                            'result is')[flag] + ' ({})'.format(actual)
    return msg


def _compares_types(argtype, force_types):
    for i, j in zip(argtype, force_types):
        if isinstance(j, (tuple, list)):
            if i not in j:
                return False
        else:
            if i != j:
                return False

    return True


def typecheck(inputs=None, outputs=None, debug=2):
    """Function/Method decorator. Checks decorated function's arguments are
  of the expected types.

  Parameters
  ----------
  inputs : types
      The expected types of the inputs to the decorated function.
      Must specify type for each parameter.
  outputs : types
      The expected type of the decorated function's return value.
      Must specify type for each parameter.
  debug : int, str
      Optional specification of 'debug' level:
      0:'ignore', 1:'warn', 2:'raise'

  Examples
  --------
  >>> # Function typecheck
  >>> @typecheck(inputs=(int, str, float), outputs=(str))
  >>> def function(a, b, c):
  ...     return b
  >>> function(1, '1', 1.) # no error
  >>> function(1, '1', 1) # error, final argument must be float
  ...
  >>> # method typecheck
  >>> class ClassName(object):
  ...     @typecheck(inputs=(str, int), outputs=int)
  ...     def method(self, a, b):
  ...         return b
  >>> x = ClassName()
  >>> x.method('1', 1) # no error
  >>> x.method(1, '1') # error

  """
    if inspect.ismethod(inputs) or inspect.isfunction(inputs):
        raise ValueError('You must specify either [inputs] types or [outputs] types arguments.')
    else:
        if isinstance(debug, str):
            debug_str = debug.lower()
            if 'raise' in debug_str:
                debug = 2
            else:
                if 'warn' in debug_str:
                    debug = 1
                else:
                    debug = 0
        else:
            if debug not in (0, 1, 2):
                debug = 2
            if inputs is not None:
                if not isinstance(inputs, (tuple, list)):
                    inputs = (
                     inputs,)
            if outputs is not None:
                if not isinstance(outputs, (tuple, list)):
                    outputs = (
                     outputs,)

    def wrap_function(func):
        sign = inspect.signature(func)
        args_name = []
        args_defaults = OrderedDict()
        for n, p in sign.parameters.items():
            if p.kind in (inspect.Parameter.VAR_POSITIONAL,
             inspect.Parameter.VAR_KEYWORD):
                pass
            else:
                args_name.append(n)
                if p.default != inspect.Parameter.empty:
                    args_defaults[n] = p.default

        @wraps(func)
        def wrapper(*args, **kwargs):
            input_args = list(args)
            excluded = {i:j for i, j in zip(args_name, input_args)}
            for i, j in args_defaults.items():
                if i in excluded:
                    pass
                else:
                    if i in kwargs:
                        input_args.append(kwargs[i])
                    else:
                        input_args.append(j)

            if debug is 0:
                return func(*args, **kwargs)
            else:
                if inputs is not None:
                    length = int(min(len(input_args), len(inputs)))
                    argtypes = tuple(map(type, input_args))
                    if not _compares_types(argtypes[:length], inputs[:length]) and not _compares_types(argtypes[1:length + 1], inputs[:length]):
                        msg = _info(func.__name__, inputs, argtypes, 0)
                        if debug is 1:
                            print('TypeWarning:', msg)
                        elif debug is 2:
                            raise TypeError(msg)
                results = func(*args, **kwargs)
                if outputs is not None:
                    res_types = (type(results),) if not isinstance(results, (tuple, list)) else tuple(map(type, results))
                    length = min(len(res_types), len(outputs))
                    if len(outputs) > len(res_types) or not _compares_types(res_types[:length], outputs[:length]):
                        msg = _info(func.__name__, outputs, res_types, 1)
                        if debug is 1:
                            print('TypeWarning: ', msg)
                        elif debug is 2:
                            raise TypeError(msg)
                return results

        return wrapper

    return wrap_function


def autoattr(*args, **kwargs):
    """
  Example
  -------
  >>> class ClassName(object):
  ..... def __init__(self):
  ......... super(ClassName, self).__init__()
  ......... self.arg1 = 1
  ......... self.arg2 = False
  ...... @autoattr('arg1', arg1=lambda x: x + 1)
  ...... def test1(self):
  ......... print(self.arg1)
  ...... @autoattr('arg2')
  ...... def test2(self):
  ......... print(self.arg2)
  >>> c = ClassName()
  >>> c.test1() # arg1 = 2
  >>> c.test2() # arg2 = True

  """
    if len(args) > 0:
        if inspect.ismethod(args[0]) or inspect.isfunction(args[0]):
            raise ValueError('You must specify at least 1 *args or **kwargs, all attributes in *args will be setted to True, likewise, all attributes in **kwargs will be setted to given value.')
    attrs = {i:True for i in args}
    attrs.update(kwargs)

    def wrap_function(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            results = func(*args, **kwargs)
            if len(args) > 0:
                for i, j in attrs.items():
                    if hasattr(args[0], i):
                        if hasattr(j, '__call__'):
                            setattr(args[0], str(i), j(getattr(args[0], i)))
                        else:
                            setattr(args[0], str(i), j)

            return results

        return wrapper

    return wrap_function


class abstractstatic(staticmethod):
    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


_primitives = (
 bool, int, float, str,
 tuple, list, dict, type, types.ModuleType, types.FunctionType,
 type(None), type(type), np.ndarray)

def func_to_str(func):
    code = cPickle.dumps((array('B', marshal.dumps(func.__code__))), protocol=(cPickle.HIGHEST_PROTOCOL))
    closure = None
    if func.__closure__ is not None:
        print('[WARNING] function: %s contains closure, which cannot be serialized.' % str(func))
        closure = tuple([c.cell_contents for c in func.__closure__])
    defaults = func.__defaults__
    return (code, closure, defaults)


def str_to_func(s, sandbox=None):
    if isinstance(s, (tuple, list)):
        code, closure, defaults = s
    else:
        if isinstance(s, string_types):
            if os.path.isfile(s):
                with open(s, 'rb') as (f):
                    code, closure, defaults = cPickle.load(f)
            else:
                code, closure, defaults = cPickle.loads(s)
        else:
            raise ValueError('Unsupport str_to_func for type:%s' % type(s))
    code = marshal.loads(cPickle.loads(code).tobytes())
    func = types.FunctionType(code=code, name=(code.co_name), globals=(sandbox if isinstance(sandbox, Mapping) else globals()),
      closure=closure,
      argdefs=defaults)
    return func


def _serialize_function_sandbox(function, source):
    """environment, dictionary (e.g. globals(), locals())
  Parameters
  ----------
  source : str
      source code of the function

  Returns
  -------
  dictionary : cPickle dumps-able dictionary to store as text
  """
    import re
    sys_module = re.compile('__\\w+__')
    environment = function.__globals__
    func_module = function.__module__
    sandbox = OrderedDict()
    seen_main_function = False
    for name, val in environment.items():
        typ = None
        if sys_module.match(name) is not None:
            continue
        if builtins.any(isinstance(val, i) for i in _primitives):
            typ = type(val)
            if isinstance(val, np.ndarray):
                val = (
                 val.tostring(), val.dtype)
                typ = 'ndarray'
            else:
                if isinstance(val, types.ModuleType):
                    val = val.__name__
                    typ = 'module'
                elif isinstance(val, type) and str(val.__module__) == 'abc' and str(type(val).__module__) == 'tensorflow.contrib.distributions.python.ops.distribution':
                    val = val.__name__
                    typ = 'edward_distribution'
                else:
                    if val is types.FunctionType:
                        val = None
                        typ = 'function_type'
                    else:
                        if val is None:
                            val = None
                            typ = 'None'
                        else:
                            if isinstance(val, Mapping):
                                val = cPickle.dumps(val, protocol=(cPickle.HIGHEST_PROTOCOL))
                                typ = 'Mapping'
                            else:
                                if inspect.isfunction(val):
                                    if val == function:
                                        seen_main_function = True
                                    else:
                                        _ = '_main' if function == val else ''
                                        if val.__module__ != func_module:
                                            typ = 'imported_function'
                                            val = (val.__name__, val.__module__)
                                        else:
                                            typ = 'defined_function'
                                        val = func_to_str(val)
                                    typ += _
            if typ is not None:
                sandbox[name] = (
                 typ, val)

    if not seen_main_function:
        sandbox['random_name_1234'] = (
         'defined_function_main',
         func_to_str(function))
    return sandbox


def _deserialize_function_sandbox(sandbox):
    """
  environment : dictionary
      create by `serialize_sandbox`
  """
    import marshal
    with warnings.catch_warnings():
        warnings.filterwarnings(action='ignore', category=ImportWarning)
        import importlib
    environment = {}
    defined_function = []
    main_func = None
    for name, (typ, val) in sandbox.items():
        if isinstance(typ, string_types):
            if typ == 'None':
                val = None
            else:
                if typ == 'edward_distribution':
                    try:
                        import edward
                        val = getattr(edward.models, val)
                    except ImportError:
                        raise ImportError("Cannot import 'edward' library to deserialize the function.")

                else:
                    if typ == 'function_type':
                        val = types.FunctionType
                    else:
                        if typ == 'Mapping':
                            val = cPickle.loads(val)
                        else:
                            if typ == 'ndarray':
                                val = np.fromstring((val[0]), dtype=(val[1]))
                            else:
                                if typ == 'module':
                                    val = importlib.import_module(val)
                                else:
                                    if 'imported_function' == typ:
                                        val = getattr(importlib.import_module(val[1]), val[0])
                                        if '_main' in typ:
                                            main_func = val
                                    else:
                                        if 'defined_function' in typ:
                                            val = str_to_func(val, globals())
                                            if '_main' in typ:
                                                main_func = val
                                            defined_function.append(name)
        else:
            if builtins.any(isinstance(typ, i) for i in _primitives):
                pass
            else:
                raise ValueError('Unsupport deserializing type: {}, value: {}'.format(typ, val))
        environment[name] = val

    for name in defined_function:
        func = environment[name]
        func.__globals__.update(environment)

    return (
     main_func, environment)


class _ArgPlaceHolder_(object):
    pass


class functionable(object):
    __doc__ = ' Class handles save and load a function with its arguments\n\n  This function does perfectly for following cases:\n      - Pickling `lambda` function without external dependencies.\n      - Pickling top-level function.\n      - Pickling imported function.\n\n  Parameters\n  ----------\n  func: function\n      lambda or function\n  arg: list\n      stored arguments list for given function\n  kwargs: dict\n      stored keyword arguments for given function\n\n  Note\n  ----\n   - Please use this function with care, only primitive variables\n   are stored in pickling the function.\n   - Avoid involving closure in creating function (because closure cannot\n   be serialized with any mean), for example:\n\n  Example\n  -------\n  >>> # Wrong way:\n  >>> lambda: obj.y\n  >>> # Good way (explicitly store the obj in default arguments):\n  >>> lambda x=obj: x.y\n  '

    def __init__(self, func, *args, **kwargs):
        super(functionable, self).__init__()
        self._function = func
        self.__name__ = self._function.__name__
        try:
            self._source = inspect.getsource(self._function)
        except Exception as e:
            print('[WARNING] Cannot get source code of function:', func, '(error:%s)' % str(e))
            self._source = None

        try:
            self._sandbox = cPickle.dumps((self._function), protocol=(cPickle.HIGHEST_PROTOCOL))
        except Exception:
            self._sandbox = _serialize_function_sandbox(func, self._source)

        sign = inspect.signature(func)
        argsmap = OrderedDict()
        for i, (n, p) in enumerate(sign.parameters.items()):
            if p.kind in (inspect.Parameter.VAR_POSITIONAL,
             inspect.Parameter.VAR_KEYWORD):
                continue
            if i < len(args):
                argsmap[n] = args[i]
            else:
                if n in kwargs:
                    argsmap[n] = kwargs[n]
                else:
                    if p.default != inspect.Parameter.empty:
                        argsmap[n] = p.default
                    else:
                        argsmap[n] = _ArgPlaceHolder_()

        self._argsmap = argsmap

    def __getstate__(self):
        return (
         self._sandbox,
         self._source,
         self._argsmap)

    def __setstate__(self, states):
        self._sandbox, self._source, self._argsmap = states
        if isinstance(self._sandbox, string_types):
            self._function = cPickle.loads(self._sandbox)
        else:
            self._function, sandbox = _deserialize_function_sandbox(self._sandbox)
        if self._function is None:
            raise RuntimeError('[funtionable] Cannot find function in sandbox.')

    @property
    def function(self):
        return self._function

    @property
    def name(self):
        return self._function.__name__

    @property
    def source(self):
        return self._source

    @property
    def sandbox(self):
        return self._sandbox

    def __call__(self, *args, **kwargs):
        final_args = self._argsmap.copy()
        for i, j in zip(final_args.keys(), args):
            final_args[i] = j

        final_args.update(kwargs)
        final_args = {i:j for i, j in final_args.items() if not isinstance(j, _ArgPlaceHolder_) if not isinstance(j, _ArgPlaceHolder_)}
        return (self._function)(**final_args)

    def __str__(self):
        s = 'Name:   %s\n' % self._function.__name__
        s += 'kwargs: %s\n' % str(self._argsmap)
        if isinstance(self._sandbox, string_types):
            s += 'Sandbox: pickle-able\n'
        else:
            s += 'Sandbox:%s\n' % str(len(self._sandbox))
        s += str(self._source)
        return s[:-1]

    def __eq__(self, other):
        if self._function == other._function:
            if self._argsmap == other._argsmap:
                return True
        return False

    def __setitem__(self, key, value):
        if not isinstance(key, (str, int, float)):
            raise ValueError('Only accept string for kwargs key or int for index of args, but type(key)={}'.format(type(key)))
        if isinstance(key, str):
            if key in self._argsmap:
                self._argsmap[key] = value
        else:
            key = int(key)
        if key < len(self._argsmap):
            key = self._argsmap.keys()[key]
            self._argsmap[key] = value

    def __getitem__(self, key):
        if not isinstance(key, (str, int, float)):
            raise ValueError('Only accept string for kwargs key or int for index of args, but type(key)={}'.format(type(key)))
        if isinstance(key, str):
            return self._argsmap[key]
        else:
            return self._argsmap(int(key))


def singleton(cls):
    """ Singleton for class instance, all __init__ with same arguments return
  same instance
  @NOTE: this is copy from six.add_metaclass
  """
    if not isinstance(cls, type):
        raise Exception('singleton decorator only accept class (type).')
    orig_vars = cls.__dict__.copy()
    slots = orig_vars.get('__slots__')
    if slots is not None:
        if isinstance(slots, str):
            slots = [
             slots]
        for slots_var in slots:
            orig_vars.pop(slots_var)

    orig_vars.pop('__dict__', None)
    orig_vars.pop('__weakref__', None)
    return Singleton(cls.__name__, cls.__bases__, orig_vars)


class Singleton(type):
    _INSTANCES = defaultdict(list)

    @staticmethod
    def _dispose(self):
        clz = self.__class__
        Singleton._INSTANCES[clz] = [(args, obj) for args, obj in Singleton._INSTANCES[clz] if obj != self]

    def __new__(mcs, name, bases, class_dict):
        if '_get_id' not in class_dict:
            raise ValueError("Instance of Singleton must define classmethod '_get_id', this method takes the same arguments as __init__ and return the unique identity for an instance.")
        return super().__new__(mcs, name, bases, class_dict)

    def __call__(cls, *args, **kwargs):
        obj_id = (cls._get_id)(*args, **kwargs)
        instances_list = Singleton._INSTANCES[cls]
        for arguments, obj in instances_list:
            if arguments == obj_id:
                return obj

        obj = (super(Singleton, cls).__call__)(*args, **kwargs)
        instances_list.append((obj_id, obj))
        setattr(obj, '__del__', types.MethodType(Singleton._dispose, obj))
        return obj