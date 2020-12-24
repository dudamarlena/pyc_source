# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/standalone/utils/cloudpickle.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 37249 bytes
"""
This class is defined to override standard pickle functionality
The goals of it follow:
-Serialize lambdas and nested functions to compiled byte code
-Deal with main module correctly
-Deal with other non-serializable objects
It does not include an unpickler, as standard python unpickling suffices.
This module was extracted from the `cloud` package, developed by `PiCloud, Inc.
<https://web.archive.org/web/20140626004012/http://www.picloud.com/>`_.
Copyright (c) 2012, Regents of the University of California.
Copyright (c) 2009 `PiCloud, Inc. <https://web.archive.org/web/20140626004012/http://www.picloud.com/>`_.
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the University of California, Berkeley nor the
      names of its contributors may be used to endorse or promote
      products derived from this software without specific prior written
      permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from __future__ import print_function
import dis
from functools import partial
import imp, io, itertools, logging, opcode, operator, pickle, struct, sys, traceback, types, weakref
DEFAULT_PROTOCOL = pickle.HIGHEST_PROTOCOL
if sys.version < '3':
    from pickle import Pickler
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    PY3 = False
else:
    types.ClassType = type
    from pickle import _Pickler as Pickler
    from io import BytesIO as StringIO
    PY3 = True

def _make_cell_set_template_code():
    """Get the Python compiler to emit LOAD_FAST(arg); STORE_DEREF
    Notes
    -----
    In Python 3, we could use an easier function:
    .. code-block:: python
       def f():
           cell = None
           def _stub(value):
               nonlocal cell
               cell = value
           return _stub
        _cell_set_template_code = f()
    This function is _only_ a LOAD_FAST(arg); STORE_DEREF, but that is
    invalid syntax on Python 2. If we use this function we also don't need
    to do the weird freevars/cellvars swap below
    """

    def inner(value):
        lambda : cell
        cell = value

    co = inner.__code__
    if not PY3:
        return types.CodeType(co.co_argcount, co.co_nlocals, co.co_stacksize, co.co_flags, co.co_code, co.co_consts, co.co_names, co.co_varnames, co.co_filename, co.co_name, co.co_firstlineno, co.co_lnotab, co.co_cellvars, ())
    return types.CodeType(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals, co.co_stacksize, co.co_flags, co.co_code, co.co_consts, co.co_names, co.co_varnames, co.co_filename, co.co_name, co.co_firstlineno, co.co_lnotab, co.co_cellvars, ())


_cell_set_template_code = _make_cell_set_template_code()

def cell_set(cell, value):
    """Set the value of a closure cell.
    """
    return types.FunctionType(_cell_set_template_code, {}, '_cell_set_inner', (), (
     cell,))(value)


STORE_GLOBAL = opcode.opmap['STORE_GLOBAL']
DELETE_GLOBAL = opcode.opmap['DELETE_GLOBAL']
LOAD_GLOBAL = opcode.opmap['LOAD_GLOBAL']
GLOBAL_OPS = (STORE_GLOBAL, DELETE_GLOBAL, LOAD_GLOBAL)
HAVE_ARGUMENT = dis.HAVE_ARGUMENT
EXTENDED_ARG = dis.EXTENDED_ARG

def islambda(func):
    return getattr(func, '__name__') == '<lambda>'


_BUILTIN_TYPE_NAMES = {}
for k, v in types.__dict__.items():
    if type(v) is type:
        _BUILTIN_TYPE_NAMES[v] = k

def _builtin_type(name):
    return getattr(types, name)


def _make__new__factory(type_):

    def _factory():
        return type_.__new__

    return _factory


_get_dict_new = _make__new__factory(dict)
_get_frozenset_new = _make__new__factory(frozenset)
_get_list_new = _make__new__factory(list)
_get_set_new = _make__new__factory(set)
_get_tuple_new = _make__new__factory(tuple)
_get_object_new = _make__new__factory(object)
_BUILTIN_TYPE_CONSTRUCTORS = {dict.__new__: _get_dict_new, 
 frozenset.__new__: _get_frozenset_new, 
 set.__new__: _get_set_new, 
 list.__new__: _get_list_new, 
 tuple.__new__: _get_tuple_new, 
 object.__new__: _get_object_new}
if sys.version_info < (3, 4):

    def _walk_global_ops(code):
        """
        Yield (opcode, argument number) tuples for all
        global-referencing instructions in *code*.
        """
        code = getattr(code, 'co_code', '')
        if not PY3:
            code = map(ord, code)
        n = len(code)
        i = 0
        extended_arg = 0
        while i < n:
            op = code[i]
            i += 1
            if op >= HAVE_ARGUMENT:
                oparg = code[i] + code[(i + 1)] * 256 + extended_arg
                extended_arg = 0
                i += 2
                if op == EXTENDED_ARG:
                    extended_arg = oparg * 65536
                if op in GLOBAL_OPS:
                    yield (
                     op, oparg)


else:

    def _walk_global_ops(code):
        """
        Yield (opcode, argument number) tuples for all
        global-referencing instructions in *code*.
        """
        for instr in dis.get_instructions(code):
            op = instr.opcode
            if op in GLOBAL_OPS:
                yield (
                 op, instr.arg)


class CloudPickler(Pickler):
    dispatch = Pickler.dispatch.copy()

    def __init__(self, file, protocol=None):
        if protocol is None:
            protocol = DEFAULT_PROTOCOL
        Pickler.__init__(self, file, protocol=protocol)
        self.modules = set()
        self.globals_ref = {}

    def dump(self, obj):
        self.inject_addons()
        try:
            return Pickler.dump(self, obj)
        except RuntimeError as e:
            try:
                if 'recursion' in e.args[0]:
                    msg = 'Could not pickle object as excessively deep recursion required.'
                    raise pickle.PicklingError(msg)
            finally:
                e = None
                del e

    def save_memoryview(self, obj):
        self.save(obj.tobytes())

    dispatch[memoryview] = save_memoryview
    if not PY3:

        def save_buffer(self, obj):
            self.save(str(obj))

        dispatch[buffer] = save_buffer
    else:

        def save_unsupported(self, obj):
            raise pickle.PicklingError('Cannot pickle objects of type %s' % type(obj))

        dispatch[types.GeneratorType] = save_unsupported
        for v in itertools.__dict__.values():
            if type(v) is type:
                dispatch[v] = save_unsupported

        def save_module(self, obj):
            """
        Save a module as an import
        """
            mod_name = obj.__name__
            if hasattr(obj, '__file__'):
                is_dynamic = False
            else:
                try:
                    _find_module(mod_name)
                    is_dynamic = False
                except ImportError:
                    is_dynamic = True

                self.modules.add(obj)
                if is_dynamic:
                    self.save_reduce(dynamic_subimport, (obj.__name__, vars(obj)), obj=obj)
                else:
                    self.save_reduce(subimport, (obj.__name__,), obj=obj)

        dispatch[types.ModuleType] = save_module

        def save_codeobject(self, obj):
            """
        Save a code object
        """
            if PY3:
                args = (obj.co_argcount, obj.co_kwonlyargcount, obj.co_nlocals, obj.co_stacksize,
                 obj.co_flags, obj.co_code, obj.co_consts, obj.co_names, obj.co_varnames,
                 obj.co_filename, obj.co_name, obj.co_firstlineno, obj.co_lnotab, obj.co_freevars,
                 obj.co_cellvars)
            else:
                args = (obj.co_argcount, obj.co_nlocals, obj.co_stacksize, obj.co_flags, obj.co_code,
                 obj.co_consts, obj.co_names, obj.co_varnames, obj.co_filename, obj.co_name,
                 obj.co_firstlineno, obj.co_lnotab, obj.co_freevars, obj.co_cellvars)
            self.save_reduce((types.CodeType), args, obj=obj)

        dispatch[types.CodeType] = save_codeobject

        def save_function(self, obj, name=None):
            """ Registered with the dispatch to handle all function types.
        Determines what kind of function obj is (e.g. lambda, defined at
        interactive prompt, etc) and handles the pickling appropriately.
        """
            if obj in _BUILTIN_TYPE_CONSTRUCTORS:
                return self.save_reduce((_BUILTIN_TYPE_CONSTRUCTORS[obj]), (), obj=obj)
                write = self.write
                if name is None:
                    name = obj.__name__
                try:
                    modname = pickle.whichmodule(obj, name)
                except Exception:
                    modname = None

                try:
                    themodule = sys.modules[modname]
                except KeyError:
                    modname = '__main__'

                if modname == '__main__':
                    themodule = None
                try:
                    lookedup_by_name = getattr(themodule, name, None)
                except Exception:
                    lookedup_by_name = None

                if themodule:
                    self.modules.add(themodule)
                    if lookedup_by_name is obj:
                        return self.save_global(obj, name)
                if not hasattr(obj, '__code__'):
                    if PY3:
                        rv = obj.__reduce_ex__(self.proto)
                    else:
                        if hasattr(obj, '__self__'):
                            rv = (
                             getattr, (obj.__self__, name))
                        else:
                            raise pickle.PicklingError("Can't pickle %r" % obj)
                    return (self.save_reduce)(*rv, **{'obj': obj})
                if islambda(obj) or getattr(obj.__code__, 'co_filename', None) == '<stdin>' or themodule is None:
                    self.save_function_tuple(obj)
                    return
                if lookedup_by_name is None or lookedup_by_name is not obj:
                    self.save_function_tuple(obj)
                    return
                if obj.__dict__:
                    self.save(_restore_attr)
                    write(pickle.MARK + pickle.GLOBAL + modname + '\n' + name + '\n')
                    self.memoize(obj)
                    self.save(obj.__dict__)
                    write(pickle.TUPLE + pickle.REDUCE)
            else:
                write(pickle.GLOBAL + modname + '\n' + name + '\n')
                self.memoize(obj)

        dispatch[types.FunctionType] = save_function

        def _save_subimports(self, code, top_level_dependencies):
            """
        Ensure de-pickler imports any package child-modules that
        are needed by the function
        """
            for x in top_level_dependencies:
                if isinstance(x, types.ModuleType) and hasattr(x, '__package__') and x.__package__:
                    prefix = x.__name__ + '.'
                    for name, module in sys.modules.items():
                        if name is not None and name.startswith(prefix):
                            tokens = set(name[len(prefix):].split('.'))
                            tokens - set(code.co_names) or self.save(module)
                            self.write(pickle.POP)

        def save_dynamic_class(self, obj):
            """
        Save a class that can't be stored as module global.
        This method is used to serialize classes that are defined inside
        functions, or that otherwise can't be serialized as attribute lookups
        from global modules.
        """
            clsdict = dict(obj.__dict__)
            clsdict.pop('__weakref__', None)
            type_kwargs = {'__doc__': clsdict.pop('__doc__', None)}
            __dict__ = clsdict.pop('__dict__', None)
            if isinstance(__dict__, property):
                type_kwargs['__dict__'] = __dict__
            save = self.save
            write = self.write
            save(_rehydrate_skeleton_class)
            write(pickle.MARK)
            tp = type(obj)
            self.save_reduce(tp, (obj.__name__, obj.__bases__, type_kwargs), obj=obj)
            save(clsdict)
            write(pickle.TUPLE)
            write(pickle.REDUCE)

        def save_function_tuple(self, func):
            """  Pickles an actual func object.
        A func comprises: code, globals, defaults, closure, and dict.  We
        extract and save these, injecting reducing functions at certain points
        to recreate the func object.  Keep in mind that some of these pieces
        can contain a ref to the func itself.  Thus, a naive save on these
        pieces could trigger an infinite loop of save's.  To get around that,
        we first create a skeleton func object using just the code (this is
        safe, since this won't contain a ref to the func), and memoize it as
        soon as it's created.  The other stuff can then be filled in later.
        """
            if is_tornado_coroutine(func):
                self.save_reduce(_rebuild_tornado_coroutine, (func.__wrapped__,), obj=func)
                return
            save = self.save
            write = self.write
            code, f_globals, defaults, closure_values, dct, base_globals = self.extract_func_data(func)
            save(_fill_function)
            write(pickle.MARK)
            self._save_subimports(code, itertools.chain(f_globals.values(), closure_values or ()))
            save(_make_skel_func)
            save((
             code,
             len(closure_values) if closure_values is not None else -1,
             base_globals))
            write(pickle.REDUCE)
            self.memoize(func)
            state = {'globals':f_globals, 
             'defaults':defaults, 
             'dict':dct, 
             'module':func.__module__, 
             'closure_values':closure_values}
            if hasattr(func, '__qualname__'):
                state['qualname'] = func.__qualname__
            save(state)
            write(pickle.TUPLE)
            write(pickle.REDUCE)

        _extract_code_globals_cache = weakref.WeakKeyDictionary() if not hasattr(sys, 'pypy_version_info') else {}

        @classmethod
        def extract_code_globals(cls, co):
            """
        Find all globals names read or written to by codeblock co
        """
            out_names = cls._extract_code_globals_cache.get(co)
            if out_names is None:
                try:
                    names = co.co_names
                except AttributeError:
                    out_names = set()
                else:
                    out_names = set((names[oparg] for op, oparg in _walk_global_ops(co)))
                    if co.co_consts:
                        for const in co.co_consts:
                            if type(const) is types.CodeType:
                                out_names |= cls.extract_code_globals(const)

                cls._extract_code_globals_cache[co] = out_names
            return out_names

        def extract_func_data(self, func):
            """
        Turn the function into a tuple of data necessary to recreate it:
            code, globals, defaults, closure_values, dict
        """
            code = func.__code__
            func_global_refs = self.extract_code_globals(code)
            f_globals = {}
            for var in func_global_refs:
                if var in func.__globals__:
                    f_globals[var] = func.__globals__[var]

            defaults = func.__defaults__
            closure = list(map(_get_cell_contents, func.__closure__)) if func.__closure__ is not None else None
            dct = func.__dict__
            base_globals = self.globals_ref.get(id(func.__globals__), {})
            self.globals_ref[id(func.__globals__)] = base_globals
            return (
             code, f_globals, defaults, closure, dct, base_globals)

        def save_builtin_function(self, obj):
            if obj.__module__ == '__builtin__':
                return self.save_global(obj)
            return self.save_function(obj)

        dispatch[types.BuiltinFunctionType] = save_builtin_function

        def save_global(self, obj, name=None, pack=struct.pack):
            """
        Save a "global".
        The name of this method is somewhat misleading: all types get
        dispatched here.
        """
            if obj.__module__ == '__main__':
                return self.save_dynamic_class(obj)
            try:
                return Pickler.save_global(self, obj, name=name)
            except Exception:
                if obj.__module__ == '__builtin__' or obj.__module__ == 'builtins':
                    if obj in _BUILTIN_TYPE_NAMES:
                        return self.save_reduce(_builtin_type,
                          (_BUILTIN_TYPE_NAMES[obj],), obj=obj)
                typ = type(obj)
                if typ is not obj:
                    if isinstance(obj, (type, types.ClassType)):
                        return self.save_dynamic_class(obj)
                raise

        dispatch[type] = save_global
        dispatch[types.ClassType] = save_global

        def save_instancemethod(self, obj):
            if obj.__self__ is None:
                self.save_reduce(getattr, (obj.im_class, obj.__name__))
            else:
                if PY3:
                    self.save_reduce((types.MethodType), (obj.__func__, obj.__self__), obj=obj)
                else:
                    self.save_reduce((types.MethodType), (obj.__func__, obj.__self__, obj.__self__.__class__), obj=obj)

        dispatch[types.MethodType] = save_instancemethod

        def save_inst(self, obj):
            """Inner logic to save instance. Based off pickle.save_inst"""
            cls = obj.__class__
            f = self.dispatch.get(cls)
            if f:
                f(self, obj)
                return
            else:
                memo = self.memo
                write = self.write
                save = self.save
                if hasattr(obj, '__getinitargs__'):
                    args = obj.__getinitargs__()
                    len(args)
                    pickle._keep_alive(args, memo)
                else:
                    args = ()
            write(pickle.MARK)
            if self.bin:
                save(cls)
                for arg in args:
                    save(arg)

                write(pickle.OBJ)
            else:
                for arg in args:
                    save(arg)

                write(pickle.INST + cls.__module__ + '\n' + cls.__name__ + '\n')
            self.memoize(obj)
            try:
                getstate = obj.__getstate__
            except AttributeError:
                stuff = obj.__dict__
            else:
                stuff = getstate()
                pickle._keep_alive(stuff, memo)
            save(stuff)
            write(pickle.BUILD)

        if not PY3:
            dispatch[types.InstanceType] = save_inst

        def save_property(self, obj):
            self.save_reduce(property, (obj.fget, obj.fset, obj.fdel, obj.__doc__), obj=obj)

        dispatch[property] = save_property

        def save_classmethod(self, obj):
            orig_func = obj.__func__
            self.save_reduce((type(obj)), (orig_func,), obj=obj)

        dispatch[classmethod] = save_classmethod
        dispatch[staticmethod] = save_classmethod

        def save_itemgetter(self, obj):
            """itemgetter serializer (needed for namedtuple support)"""

            class Dummy:

                def __getitem__(self, item):
                    return item

            items = obj(Dummy())
            if not isinstance(items, tuple):
                items = (
                 items,)
            return self.save_reduce(operator.itemgetter, items)

        if type(operator.itemgetter) is type:
            dispatch[operator.itemgetter] = save_itemgetter

        def save_attrgetter(self, obj):
            """attrgetter serializer"""

            class Dummy(object):

                def __init__(self, attrs, index=None):
                    self.attrs = attrs
                    self.index = index

                def __getattribute__(self, item):
                    attrs = object.__getattribute__(self, 'attrs')
                    index = object.__getattribute__(self, 'index')
                    if index is None:
                        index = len(attrs)
                        attrs.append(item)
                    else:
                        attrs[index] = '.'.join([attrs[index], item])
                    return type(self)(attrs, index)

            attrs = []
            obj(Dummy(attrs))
            return self.save_reduce(operator.attrgetter, tuple(attrs))

        if type(operator.attrgetter) is type:
            dispatch[operator.attrgetter] = save_attrgetter

        def save_file(self, obj):
            """Save a file"""
            try:
                import StringIO as pystringIO
            except ImportError:
                import io as pystringIO

            if not (hasattr(obj, 'name') and hasattr(obj, 'mode')):
                raise pickle.PicklingError('Cannot pickle files that do not map to an actual file')
            if obj is sys.stdout:
                return self.save_reduce(getattr, (sys, 'stdout'), obj=obj)
            if obj is sys.stderr:
                return self.save_reduce(getattr, (sys, 'stderr'), obj=obj)
            if obj is sys.stdin:
                raise pickle.PicklingError('Cannot pickle standard input')
            if obj.closed:
                raise pickle.PicklingError('Cannot pickle closed files')
            if hasattr(obj, 'isatty'):
                if obj.isatty():
                    raise pickle.PicklingError('Cannot pickle files that map to tty objects')
            if 'r' not in obj.mode:
                if '+' not in obj.mode:
                    raise pickle.PicklingError('Cannot pickle files that are not opened for reading: %s' % obj.mode)
            name = obj.name
            retval = pystringIO.StringIO()
            try:
                curloc = obj.tell()
                obj.seek(0)
                contents = obj.read()
                obj.seek(curloc)
            except IOError:
                raise pickle.PicklingError('Cannot pickle file %s as it cannot be read' % name)

            retval.write(contents)
            retval.seek(curloc)
            retval.name = name
            self.save(retval)
            self.memoize(obj)

        def save_ellipsis(self, obj):
            self.save_reduce(_gen_ellipsis, ())

        def save_not_implemented(self, obj):
            self.save_reduce(_gen_not_implemented, ())

        if PY3:
            dispatch[io.TextIOWrapper] = save_file
        else:
            dispatch[file] = save_file
    dispatch[type(Ellipsis)] = save_ellipsis
    dispatch[type(NotImplemented)] = save_not_implemented

    def save_weakset(self, obj):
        self.save_reduce(weakref.WeakSet, (list(obj),))

    dispatch[weakref.WeakSet] = save_weakset

    def save_logger(self, obj):
        self.save_reduce((logging.getLogger), (obj.name,), obj=obj)

    dispatch[logging.Logger] = save_logger

    def inject_addons(self):
        """Plug in system. Register additional pickling functions if modules already loaded"""
        pass


def is_tornado_coroutine(func):
    """
    Return whether *func* is a Tornado coroutine function.
    Running coroutines are not supported.
    """
    if 'tornado.gen' not in sys.modules:
        return False
    else:
        gen = sys.modules['tornado.gen']
        return hasattr(gen, 'is_coroutine_function') or False
    return gen.is_coroutine_function(func)


def _rebuild_tornado_coroutine(func):
    from tornado import gen
    return gen.coroutine(func)


def dump(obj, file, protocol=None):
    """Serialize obj as bytes streamed into file
    protocol defaults to cloudpickle.DEFAULT_PROTOCOL which is an alias to
    pickle.HIGHEST_PROTOCOL. This setting favors maximum communication speed
    between processes running the same Python version.
    Set protocol=pickle.DEFAULT_PROTOCOL instead if you need to ensure
    compatibility with older versions of Python.
    """
    CloudPickler(file, protocol=protocol).dump(obj)


def dumps(obj, protocol=None):
    """Serialize obj as a string of bytes allocated in memory
    protocol defaults to cloudpickle.DEFAULT_PROTOCOL which is an alias to
    pickle.HIGHEST_PROTOCOL. This setting favors maximum communication speed
    between processes running the same Python version.
    Set protocol=pickle.DEFAULT_PROTOCOL instead if you need to ensure
    compatibility with older versions of Python.
    """
    file = StringIO()
    try:
        cp = CloudPickler(file, protocol=protocol)
        cp.dump(obj)
        return file.getvalue()
    finally:
        file.close()


load = pickle.load
loads = pickle.loads

def subimport(name):
    __import__(name)
    return sys.modules[name]


def dynamic_subimport(name, vars):
    mod = imp.new_module(name)
    mod.__dict__.update(vars)
    sys.modules[name] = mod
    return mod


def _restore_attr(obj, attr):
    for key, val in attr.items():
        setattr(obj, key, val)

    return obj


def _get_module_builtins():
    return pickle.__builtins__


def print_exec(stream):
    ei = sys.exc_info()
    traceback.print_exception(ei[0], ei[1], ei[2], None, stream)


def _modules_to_main(modList):
    """Force every module in modList to be placed into main"""
    if not modList:
        return
    main = sys.modules['__main__']
    for modname in modList:
        if type(modname) is str:
            try:
                mod = __import__(modname)
            except Exception as e:
                try:
                    sys.stderr.write('warning: could not import %s\n.  Your function may unexpectedly error due to this import failing;A version mismatch is likely.  Specific error was:\n' % modname)
                    print_exec(sys.stderr)
                finally:
                    e = None
                    del e

            else:
                setattr(main, mod.__name__, mod)


def _genpartial(func, args, kwds):
    if not args:
        args = ()
    if not kwds:
        kwds = {}
    return partial(func, *args, **kwds)


def _gen_ellipsis():
    return Ellipsis


def _gen_not_implemented():
    return NotImplemented


def _get_cell_contents(cell):
    try:
        return cell.cell_contents
    except ValueError:
        return _empty_cell_value


def instance(cls):
    """Create a new instance of a class.
    Parameters
    ----------
    cls : type
        The class to create an instance of.
    Returns
    -------
    instance : cls
        A new instance of ``cls``.
    """
    return cls()


@instance
class _empty_cell_value(object):
    __doc__ = 'sentinel for empty closures\n    '

    @classmethod
    def __reduce__(cls):
        return cls.__name__


def _fill_function(*args):
    """Fills in the rest of function data into the skeleton function object
    The skeleton itself is create by _make_skel_func().
    """
    if len(args) == 2:
        func = args[0]
        state = args[1]
    else:
        if len(args) == 5:
            func = args[0]
            keys = ['globals', 'defaults', 'dict', 'closure_values']
            state = dict(zip(keys, args[1:]))
        else:
            if len(args) == 6:
                func = args[0]
                keys = ['globals', 'defaults', 'dict', 'module', 'closure_values']
                state = dict(zip(keys, args[1:]))
            else:
                raise ValueError('Unexpected _fill_value arguments: %r' % (args,))
    func.__globals__.update(state['globals'])
    func.__defaults__ = state['defaults']
    func.__dict__ = state['dict']
    if 'module' in state:
        func.__module__ = state['module']
    if 'qualname' in state:
        func.__qualname__ = state['qualname']
    cells = func.__closure__
    if cells is not None:
        for cell, value in zip(cells, state['closure_values']):
            if value is not _empty_cell_value:
                cell_set(cell, value)

    return func


def _make_empty_cell():
    return (lambda : cell).__closure__[0]


def _make_skel_func(code, cell_count, base_globals=None):
    """ Creates a skeleton function object that contains just the provided
        code and the correct number of cells in func_closure.  All other
        func attributes (e.g. func_globals) are empty.
    """
    if base_globals is None:
        base_globals = {}
    base_globals['__builtins__'] = __builtins__
    closure = tuple((_make_empty_cell() for _ in range(cell_count))) if cell_count >= 0 else None
    return types.FunctionType(code, base_globals, None, None, closure)


def _rehydrate_skeleton_class(skeleton_class, class_dict):
    """Put attributes from `class_dict` back on `skeleton_class`.
    See CloudPickler.save_dynamic_class for more info.
    """
    for attrname, attr in class_dict.items():
        setattr(skeleton_class, attrname, attr)

    return skeleton_class


def _find_module(mod_name):
    """
    Iterate over each part instead of calling imp.find_module directly.
    This function is able to find submodules (e.g. sickit.tree)
    """
    path = None
    for part in mod_name.split('.'):
        if path is not None:
            path = [
             path]
        file, path, description = imp.find_module(part, path)
        if file is not None:
            file.close()

    return (
     path, description)


def _getobject(modname, attribute):
    mod = __import__(modname, fromlist=[attribute])
    return mod.__dict__[attribute]


if sys.version_info < (3, 4):
    method_descriptor = type(str.upper)

    def _reduce_method_descriptor(obj):
        return (
         getattr, (obj.__objclass__, obj.__name__))


    try:
        import copy_reg as copyreg
    except ImportError:
        import copyreg

    copyreg.pickle(method_descriptor, _reduce_method_descriptor)