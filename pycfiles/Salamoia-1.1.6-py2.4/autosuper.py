# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/autosuper.py
# Compiled at: 2007-12-02 16:26:55
"""Automatically determine the correct super object and use it.

This module defines a mix-in class `autosuper` which has a single property -
`super`.

The object returned by `super` can either be called or have attributes accessed.
If it is called, a base class method with the same name as the current method
will be called with the parameters passed. If an attribute is accessed a base
class attribute will be returned.

Example of usage::

    import autosuper

    class A (autosuper.autosuper):

        def __init__ (self, a, b):
            self.super()
            print 'A.__init__'
            print a, b

        def test (self, a, b):
            print 'A.test'
            print b, a

    class B (A):

        def __init__ (self):
            self.super(1, 2)
            print 'B.__init__'
            self.super.test(3, 4)

        def test (self, a, b):
            print 'B.test'
            print a, b

    B()

produces::

    A.__init__
    1 2
    B.__init__
    A.test
    4 3

We didn't need to call `self.super()` in `A.__init__` because the base class
is `object`, but we can do so.

Note that `B.test` is never called - the call in `B.__init__` to`self.super.test`
ensures that only methods of classes higher in the MRO will be searched for `test`.

Note also that it is an error to call `self.super.super` - a `TypeError` will
be raised.

**Important:** It is assumed that the code objects for each method are unique.
Breakage is likely if methods share code objects (e.g. the code object for one
method is assigned to another method).

**Note:** For performance reasons, this implementation modifies the bytecode of
functions. To disable bytecode modification, set `__super_modify_bytecode__` to
`False`."""
from __future__ import generators
import new, sys, types, __builtin__
try:
    True
except NameError:
    __builtin__.__dict__['True'] = 1
    __builtin__.__dict__['False'] = 1

__super_modify_bytecode__ = True
try:
    from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG
    LOAD_CONST = opmap['LOAD_CONST']
    LOAD_FAST = opmap['LOAD_FAST']
    LOAD_ATTR = opmap['LOAD_ATTR']
    STORE_FAST = opmap['STORE_FAST']
    CALL_FUNCTION = opmap['CALL_FUNCTION']
    STORE_GLOBAL = opmap['STORE_GLOBAL']
    JUMP_FORWARD = opmap['JUMP_FORWARD']
    JUMP_ABSOLUTE = opmap['JUMP_ABSOLUTE']
    CONTINUE_LOOP = opmap['CONTINUE_LOOP']
    ABSOLUTE_TARGET = (
     JUMP_ABSOLUTE, CONTINUE_LOOP)
    ABORT_CODES = (EXTENDED_ARG, STORE_GLOBAL)
except ImportError:
    LOAD_CONST = 100
    LOAD_FAST = 124
    LOAD_ATTR = 105
    STORE_FAST = 125
    CALL_FUNCTION = 131
    STORE_GLOBAL = 97
    JUMP_FORWARD = 110
    JUMP_ABSOLUTE = 113
    CONTINUE_LOOP = 119
    HAVE_ARGUMENT = 90
    EXTENDED_ARG = 143
    ABSOLUTE_TARGET = (
     JUMP_ABSOLUTE, CONTINUE_LOOP)
    ABORT_CODES = (EXTENDED_ARG, STORE_GLOBAL)

    def enumerate(sequence):
        return zip(range(len(sequence)), sequence)


__builtin__.__dict__['__super_modify_bytecode__'] = __super_modify_bytecode__
try:
    import _autosuper
    _autosuper.__doc__ = __doc__
    sys.modules[__name__] = _autosuper
except ImportError:

    class _super(object):
        """
        Wrapper for the super object.

        If called, a base class method of the same name as the current method
        will be called. Otherwise, attributes will be accessed.
        """
        __module__ = __name__
        __name__ = 'super'
        __slots__ = ('_super__super', '_super__method')

        def __init__(self, klass, obj, name, builtin_super=super, __setattr__=object.__setattr__):
            super = builtin_super(klass, obj)
            __setattr__(self, '_super__super', super)
            try:
                __setattr__(self, '_super__method', getattr(super, name))
            except AttributeError:
                __setattr__(self, '_super__method', name)

        def __call__(self, *p, **kw):
            """
            Calls the base class method with the passed parameters.
            """
            method = object.__getattribute__(self, '_super__method')
            try:
                return method(*p, **kw)
            except TypeError:
                if type(method) is not str:
                    raise

            super = object.__getattribute__(self, '_super__super')
            method = getattr(super, method)
            object.__setattr__(self, '_super__method', method)
            return method(*p, **kw)

        def __getattribute__(self, name, __getattribute__=object.__getattribute__):
            """
            Gets a base class attribute.
            """
            super = __getattribute__(self, '_super__super')
            try:
                return getattr(super, name)
            except (TypeError, AttributeError):
                if name == 'super':
                    raise TypeError("Cannot get 'super' object of 'super' object")
                else:
                    raise

        def __setattr__(self, name, value, __getattribute__=object.__getattribute__, __setattr__=object.__setattr__):
            """
            All we want to do here is make it look the same as if we called
            setattr() on a real `super` object.
            """
            super = __getattribute__(self, '_super__super')
            __setattr__(super, name, value)


    def _bind_autosuper(func, klass):
        """
        Modifies the bytecode of the function so that a single call to _super() is
        performed first thing in the function call, then all accesses are via
        LOAD_FAST. Once this has been done for a function the MRO will not need to
        be trawled again.

        The function should be the underlying function of a method.

        Note: If the function does not call `self.super` then the bytecode will
        be unchanged.
        """
        try:
            func.__super_original_bytecode__
            return func
        except AttributeError:
            pass

        func.__super_original_bytecode__ = func.func_code
        name = func.func_name
        co = func.func_code
        newcode = map(ord, co.co_code)
        codelen = len(newcode)
        newconsts = list(co.co_consts)
        sl_pos = len(co.co_varnames)
        newvarnames = co.co_varnames + (co.co_varnames[0] + '.super',)
        (s_pos, k_pos, n_pos) = (-1, -1, -1)
        for (pos, v) in enumerate(newconsts):
            if v is _super:
                s_pos = pos
            elif v is klass:
                k_pos = pos
            elif v == name:
                n_pos = pos

        if s_pos == -1:
            s_pos = len(newconsts)
            newconsts.append(_super)
        if k_pos == -1:
            k_pos = len(newconsts)
            newconsts.append(klass)
        if n_pos == -1:
            n_pos = len(newconsts)
            newconsts.append(name)
        setup_code = [
         LOAD_CONST, s_pos & 255, s_pos >> 8, LOAD_CONST, k_pos & 255, k_pos >> 8, LOAD_FAST, 0, 0, LOAD_CONST, n_pos & 255, n_pos >> 8, CALL_FUNCTION, 3, 0, STORE_FAST, sl_pos & 255, sl_pos >> 8]
        need_setup = False
        i = 0
        while i < codelen:
            opcode = newcode[i]
            if opcode in ABORT_CODES:
                return func
            elif opcode == LOAD_FAST:
                oparg = newcode[(i + 1)] + (newcode[(i + 2)] << 8)
                if oparg == 0:
                    i += 3
                    opcode = newcode[i]
                    if opcode == LOAD_ATTR:
                        oparg = newcode[(i + 1)] + (newcode[(i + 2)] << 8)
                        attrname = co.co_names[oparg]
                        if attrname == 'super':
                            need_setup = True
                            newcode[(i - 3):i] = [LOAD_FAST, sl_pos & 255, sl_pos >> 8]
                            newcode[i:(i + 3)] = [JUMP_FORWARD, 0 & 255, 0 >> 8]
            elif opcode in ABSOLUTE_TARGET:
                oparg = newcode[(i + 1)] + (newcode[(i + 2)] << 8) + len(setup_code)
                newcode[i + 1] = oparg & 255
                newcode[i + 2] = oparg >> 8
            i += 1
            if opcode >= HAVE_ARGUMENT:
                i += 2

        if not need_setup:
            return func
        co_stacksize = max(4, co.co_stacksize)
        co_lnotab = map(ord, co.co_lnotab)
        if co_lnotab:
            co_lnotab[0] += len(setup_code)
        co_lnotab = ('').join(map(chr, co_lnotab))
        codestr = ('').join(map(chr, setup_code + newcode))
        codeobj = new.code(co.co_argcount, len(newvarnames), co_stacksize, co.co_flags, codestr, tuple(newconsts), co.co_names, newvarnames, co.co_filename, co.co_name, co.co_firstlineno, co_lnotab, co.co_freevars, co.co_cellvars)
        func.func_code = codeobj
        return func


    def _do_bind_autosuper_class(klass, attrs):
        """
        Modifies the bytecode of every method on the class that invokes `self.super`.
        """
        for a in attrs.values():
            if type(a) is types.FunctionType:
                try:
                    a.__super_original_bytecode__
                except AttributeError:
                    _bind_autosuper(a, klass)

        try:
            setattr(klass, '_%s__super_bound' % klass.__name__, True)
        except (TypeError, AttributeError):
            pass


    def _bind_autosuper_class(klass):
        """
        Modifies the bytecode of every method on the class and base classes that
        invokes `self.super`.
        """
        for k in klass.__mro__:
            if k is autosuper or not issubclass(k, autosuper):
                continue
            attrs = vars(k)
            try:
                bound = attrs[('_%s__super_bound' % k.__name__)]
            except KeyError:
                bound = False

            if not bound:
                _do_bind_autosuper_class(k, attrs)


    def _getSuper(self, getframe=sys._getframe, _bind_autosuper=_bind_autosuper):
        """
        Gets the super object for the current function. If `autosuper.__init__` is
        executed this method will never be called.
        """
        frame = getframe().f_back
        code = frame.f_code
        name = code.co_name
        cur_class = None
        m = None
        for c in type(self).__mro__:
            last_method = m
            try:
                m = getattr(c, name)
                func_code = m.func_code
            except AttributeError:
                func_code = None

            match_code = func_code is code
            if not match_code:
                try:
                    match_code = m.__super_original_bytecode__ is code
                except AttributeError:
                    pass

            if match_code:
                cur_class = c
            elif cur_class is not None:
                break

        if cur_class is None:
            raise TypeError, "Can only call 'super' in a bound method"
        if __super_modify_bytecode__:
            _bind_autosuper(last_method.im_func, cur_class)
        return _super(cur_class, self, name)


    class autosuper(object):
        """
        Automatically determine the correct super object and use it.
        """
        __module__ = __name__
        __slots__ = ()

        def __init__(self, *p, **kw):
            """
            Modify the bytecode of the methods to improve performance.
            """
            if __super_modify_bytecode__:
                klass = type(self)
                attrs = vars(klass)
                try:
                    bound = attrs[('_%s__super_bound' % klass.__name__)]
                except KeyError:
                    bound = False
                else:
                    if not bound:
                        _bind_autosuper_class(klass)
            super(autosuper, self).__init__(*p, **kw)

        super = property(fget=_getSuper, doc='Gets a `super` object for the class of the currently-executing method.')


    try:
        import bind_constants
        bind_constants.bind_all(sys.modules[__name__])
    except ImportError:
        pass

from salamoia.tests import *
runDocTests()