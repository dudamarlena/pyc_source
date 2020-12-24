# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/lazy/imports.py
# Compiled at: 2016-07-25 10:38:46
"""Lazy imoport - import the module upon first request"""
try:
    from mx.Misc import LazyModule
except ImportError:

    class LazyModule:

        def __init__(self, module_name, locals, globals=None):
            self.module = None
            self.module_name = module_name
            self.locals = locals
            if globals is None:
                globals = locals
            self.globals = globals
            return

        def __getattr__(self, attr):
            if self.module is None:
                self.module = module = __import__(self.module_name, self.globals, self.locals)
            else:
                module = self.module
            return getattr(module, attr)