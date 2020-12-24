# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/pyobj.py
# Compiled at: 2020-05-07 16:38:47
"""Implementations of Python fundamental objects for xpython."""
from __future__ import print_function
import collections, inspect, linecache, types
from sys import stderr
from xdis.util import CO_GENERATOR
from xdis import PYTHON3, PYTHON_VERSION, iscode
import six
PY2 = not PYTHON3

def make_cell(value):
    fn = (lambda x: lambda : x)(value)
    if PYTHON3:
        return fn.__closure__[0]
    else:
        return fn.func_closure[0]


Traceback = collections.namedtuple('_Traceback', 'tb_frame tb_lasti tb_lineno tb_next')
try:
    _Traceback.tb_frame.__doc__ = 'frame object at this level'
    _Traceback.tb_lasti.__doc__ = 'index of last attempted instruction in bytecode'
    _Traceback.tb_lineno.__doc__ = 'current line number in Python source code'
    _Traceback.tb_next.__doc__ = 'next inner traceback object (called by this level)'
except:
    pass

class Function(object):
    """Function(name, code, globals, argdefs, closure, vm,  kwdefaults={}, annotations={})

    Create a function object in vm from a code object and a dictionary.
    The name string overrides the name from the code object.
    The optional argdefs tuple specifies the default argument values.
    The optional closure tuple supplies the bindings for free variables.

    In contrast to `types.Function`, parameters appear in the order
    the CPython generates them; also there is an additional parameter
    `vm` which appears last.

    As a convenience, in contrast to types.FunctionType we allow
    setting `kwdefaults` and `annotations`.
    """
    __slots__ = [
     'func_code',
     'func_name',
     'func_defaults',
     'func_closure',
     '__code__',
     '__name__',
     '__defaults__',
     '__kwdefaults__',
     '__closure__',
     'func_globals',
     'func_locals',
     'func_dict',
     '__dict__',
     '_vm',
     '_func']

    def __init__(self, name, code, globs, argdefs, closure=None, vm=None, kwdefaults={}, annotations={}):
        self._vm = vm
        self.version = vm.version
        if name is not None and not isinstance(name, str):
            raise TypeError('Function() argument 1 (name) must None or string, not %s' % type(name))
        if not iscode(code):
            raise TypeError('Function() argument 2 (code) must be code, not %s' % type(code))
        if not isinstance(globs, dict):
            raise TypeError('Function() argument 3 (argdefs) must be dict, not %s' % type(globs))
        if closure is not None and not isinstance(closure, tuple):
            raise TypeError('Function() argument 5 (closure) must None or tuple, not %s' % type(closure))
        if not vm:
            raise TypeError('Function() argument 6 (vm) must be passed')
        self.func_code = self.__code__ = code
        self.func_name = self.__name__ = name or code.co_name
        self.func_defaults = self.__defaults__ = tuple(argdefs)
        self.func_closure = self.__closure__ = closure
        self.func_globals = globs
        self.func_locals = self._vm.frame.f_locals
        self.__dict__ = {}
        self.__doc__ = code.co_consts[0] if hasattr(code, 'co_consts') and code.co_consts else None
        self.__kwdefaults__ = kwdefaults
        self.__annotations = annotations
        self.has_dot_zero = False
        kw = {'argdefs': self.func_defaults}
        if closure:
            kw['closure'] = tuple(make_cell(0) for _ in closure)
        if not isinstance(code, types.CodeType) and hasattr(code, 'to_native'):
            try:
                code = code.to_native()
            except:
                pass

        if isinstance(code, types.CodeType):
            self._func = types.FunctionType(code, globs, **kw)
            self._func.__kwdefaults__ = kwdefaults
            self._func.__annotations__ = annotations
        else:
            self._func = self
        return

    def __repr__(self):
        return '<Function %s at 0x%08x>' % (self.func_name, id(self))

    def __get__(self, instance, owner):
        if instance is not None:
            return Method(instance, owner, self)
        else:
            version = self.version if hasattr(self, 'version') else PYTHON_VERSION
            if version < 3.0:
                return Method(None, owner, self)
            return self
            return

    def __call__(self, *args, **kwargs):
        if self.has_dot_zero:
            assert len(args) == 1 and not kwargs, 'Surprising comprehension!'
            callargs = {'.0': args[0]}
        else:
            callargs = inspect.getcallargs(self._func, *args, **kwargs)
        frame = self._vm.make_frame(self.func_code, callargs, self.func_globals, {})
        if self.func_code.co_flags & CO_GENERATOR:
            gen = Generator(frame, self._vm)
            frame.generator = gen
            retval = gen
        else:
            retval = self._vm.run_frame(frame)
        return retval


class Method(object):
    """Create a bound instance method object."""

    def __init__(self, obj, _class, func):
        self.im_self = obj
        self.im_class = _class
        self.im_func = func

    def __repr__(self):
        name = '%s.%s' % (self.im_class.__name__, self.im_func.func_name)
        if self.im_self is not None:
            return '<Bound Method %s of %s>' % (name, self.im_self)
        else:
            return '<Unbound Method %s>' % (name,)
            return

    def __call__(self, *args, **kwargs):
        if self.im_self is not None:
            return self.im_func(self.im_self, *args, **kwargs)
        else:
            return self.im_func(*args, **kwargs)
            return


class Cell(object):
    """A fake cell for closures.

    Closures keep names in scope by storing them not in a frame, but in a
    separate object called a cell.  Frames share references to cells, and
    the LOAD_DEREF and STORE_DEREF opcodes get and set the value from cells.

    This class acts as a cell, though it has to jump through two hoops to make
    the simulation complete:

        1. In order to create actual FunctionType functions, we have to have
           actual cell objects, which are difficult to make. See the twisty
           double-lambda in __init__.

        2. Actual cell objects can't be modified, so to implement STORE_DEREF,
           we store a one-element list in our cell, and then use [0] as the
           actual value.

    """

    def __init__(self, value):
        self.contents = value

    def get(self):
        return self.contents

    def set(self, value):
        self.contents = value


Block = collections.namedtuple('Block', 'type, handler, level')

class Frame(object):

    def __init__(self, f_code, f_globals, f_locals, f_back, version=PYTHON_VERSION):
        self.f_code = f_code
        self.f_globals = f_globals
        self.f_locals = f_locals
        self.f_back = f_back
        self.stack = []
        self.f_trace = None
        self.version = PYTHON_VERSION
        if f_back and f_back.f_globals is f_globals:
            self.f_builtins = f_back.f_builtins
        else:
            try:
                self.f_builtins = f_globals['__builtins__']
                if hasattr(self.f_builtins, '__dict__'):
                    self.f_builtins = self.f_builtins.__dict__
            except KeyError:
                self.f_builtins = {'None': None}

        self.f_lineno = f_code.co_firstlineno
        self.f_lasti = 0
        if f_code.co_cellvars:
            self.cells = {}
            if not f_back.cells:
                f_back.cells = {}
            for var in f_code.co_cellvars:
                cell = Cell(self.f_locals.get(var))
                f_back.cells[var] = self.cells[var] = cell

        else:
            self.cells = None
        if f_code.co_freevars:
            if not self.cells:
                self.cells = {}
            for var in f_code.co_freevars:
                assert self.cells is not None
                assert f_back.cells, 'f_back.cells: %r' % (f_back.cells,)
                self.cells[var] = f_back.cells[var]

        self.block_stack = []
        self.generator = None
        return

    def __repr__(self):
        return '<Frame at 0x%08x: %r @ %d>' % (
         id(self),
         self.f_code.co_filename,
         self.f_lineno)

    def line_number(self):
        """Get the current line number the frame is executing."""
        lnotab = self.f_code.co_lnotab
        byte_increments = six.iterbytes(lnotab[0::2])
        line_increments = six.iterbytes(lnotab[1::2])
        byte_num = 0
        line_num = self.f_code.co_firstlineno
        for byte_incr, line_incr in zip(byte_increments, line_increments):
            if isinstance(byte_incr, str):
                return ord(byte_incr)
            byte_num += byte_incr
            if byte_num > self.f_lasti:
                break
            line_num += line_incr

        return line_num


class Traceback(object):

    def __init__(self, frame):
        self.tb_next = frame.f_back
        self.tb_lasti = frame.f_lasti
        self.tb_lineno = frame.f_lineno
        self.tb_frame = frame

    def print_tb(self, limit=None, file=stderr):
        """Like traceback.tb, but is a method."""
        tb = self
        while tb:
            f = tb.tb_frame
            filename = f.f_code.co_filename
            lineno = f.line_number()
            print('  File "%s", line %d, in %s' % (filename, lineno, f.f_code.co_name), file=file)
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            if line:
                print('    ' + line.strip(), file=file)
            tb = tb.tb_next


def traceback_from_frame(frame):
    tb = None
    while frame:
        next_tb = Traceback(frame)
        next_tb.tb_next = tb
        tb = next_tb
        frame = frame.f_back

    return tb


class Generator(object):

    def __init__(self, g_frame, vm):
        self.gi_frame = g_frame
        self.vm = vm
        self.started = False
        self.finished = False

    def __iter__(self):
        return self

    def next(self):
        return self.send(None)

    def send(self, value=None):
        if not self.started and value is not None:
            raise TypeError("Can't send non-None value to a just-started generator")
        self.gi_frame.stack.append(value)
        self.started = True
        val = self.vm.resume_frame(self.gi_frame)
        if self.finished:
            raise StopIteration(val)
        return val

    __next__ = next