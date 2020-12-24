# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop34.py
# Compiled at: 2020-05-07 20:07:47
"""Bytecode Interpreter operations for Python 3.4
"""
from __future__ import print_function, division
import inspect, types
from xpython.byteop.byteop32 import ByteOp32
from xpython.byteop.byteop33 import ByteOp33
del ByteOp32.STORE_LOCALS

class ByteOp34(ByteOp33):

    def __init__(self, vm):
        super(ByteOp34, self).__init__(vm)

    def LOAD_CLASSDEREF(self, count):
        """
        Much like LOAD_DEREF but first checks the locals dictionary before
        consulting the cell. This is used for loading free variables in class
        bodies.
        """
        self.vm.push(self.vm.frame.cells[count].get())

    def MAKE_FUNCTION(self, argc):
        """
        Pushes a new function object on the stack. From bottom to top, the consumed stack must consist of

        * argc & 0xFF default argument objects in positional order
        * (argc >> 8) & 0xFF pairs of name and default argument, with the name just below the object on the stack, for keyword-only parameters
        * (argc >> 16) & 0x7FFF parameter annotation objects
        * a tuple listing the parameter names for the annotations (only if there are ony annotation objects)
        * the code associated with the function (at TOS1)
        * the qualified name of the function (at TOS)
        """
        rest, default_count = divmod(argc, 256)
        annotate_count, kw_default_count = divmod(rest, 256)
        name = self.vm.pop()
        code = self.vm.pop()
        if annotate_count:
            annotate_names = self.vm.pop()
            annotate_objects = self.vm.popn(annotate_count - 1)
            n = len(annotate_names)
            assert n == len(annotate_objects)
            annotations = {annotate_names[i]:annotate_objects[i] for i in range(n)}
        else:
            annotations = {}
        if kw_default_count:
            kw_default_pairs = self.vm.popn(2 * kw_default_count)
            kwdefaults = dict(kw_default_pairs[i:i + 2] for i in range(0, len(kw_default_pairs), 2))
        else:
            kwdefaults = {}
        if default_count:
            defaults = self.vm.popn(default_count)
        else:
            defaults = tuple()
        globs = self.vm.frame.f_globals
        if not inspect.iscode(code) and hasattr(code, 'to_native'):
            code = code.to_native()
        fn = types.FunctionType(code, globs, name, tuple(defaults))
        fn.__kwdefaults__ = kwdefaults
        fn.__annonations__ = annotations
        fn.version = self.version
        self.vm.push(fn)