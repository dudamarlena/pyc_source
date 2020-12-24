# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\threadsafe_tkinter\__init__.py
# Compiled at: 2019-03-22 00:04:43
# Size of source mod 2**32: 6271 bytes
"""
This is a thread-safe version of Tkinter for Python3.
Import this where you would normally import tkinter.

Copyright (c) 2017 Devin Bobadilla

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
__author__ = 'Devin Bobadilla'
__date__ = '2019.03.21'
__version__ = (1, 0, 2)
try:
    from tkinter import *
except ImportError:
    from Tkinter import *

from queue import Queue as _Queue
from time import sleep as _sleep
from threading import currentThread as _curr_thread, _DummyThread
from types import FunctionType
TKHOOK_UNHOOKING = -1
TKHOOK_UNHOOKED = 0
TKHOOK_HOOKED = 1

class TkWrapper:
    idle_time = 15
    after_call_id = None
    _hook_status = TKHOOK_UNHOOKED

    def __init__(self, tk_widget=None):
        self.tk_widget = tk_widget
        self.request_queue = self.create_queue()
        self.tk_thread = self.get_curr_thread()
        self.after_call_id = None

    def get_curr_thread(self):
        return _curr_thread()

    def create_queue(self):
        return _Queue()

    def __getattr__--- This code section failed: ---

 L.  65         0  LOAD_DEREF               'self'
                3  LOAD_ATTR                tk_widget
                6  LOAD_CONST               None
                9  COMPARE_OP               is
               12  POP_JUMP_IF_TRUE     33  'to 33'
               15  LOAD_DEREF               'self'
               18  LOAD_ATTR                tk_widget
               21  LOAD_ATTR                _tk
               24  LOAD_CONST               None
               27  COMPARE_OP               is
             30_0  COME_FROM            12  '12'
               30  POP_JUMP_IF_FALSE    45  'to 45'

 L.  66        33  LOAD_GLOBAL              AttributeError

 L.  67        36  LOAD_STR                 'self.tk_widget is None. Not hooked into a Tk instance.'
               39  CALL_FUNCTION_1       1  '1 positional, 0 named'
               42  RAISE_VARARGS_1       1  'exception'
             45_0  COME_FROM            30  '30'

 L.  69        45  LOAD_GLOBAL              getattr
               48  LOAD_DEREF               'self'
               51  LOAD_ATTR                tk_widget
               54  LOAD_ATTR                _tk
               57  LOAD_FAST                'attr_name'
               60  CALL_FUNCTION_2       2  '2 positional, 0 named'
               63  STORE_FAST               'tk_attr'

 L.  70        66  LOAD_STR                 '_f'
               69  LOAD_FAST                'tk_attr'
               72  LOAD_CLOSURE             'self'
               75  BUILD_TUPLE_1         1 
               78  LOAD_LAMBDA              '<code_object <lambda>>'
               81  LOAD_STR                 'TkWrapper.__getattr__.<locals>.<lambda>'
               84  MAKE_CLOSURE_N1_0        '0 positional, 1 keyword only, 0 annotated'
               87  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 87

    def call_tk_attr_threadsafe(self, tk_attr, *a, **kw):
        thread = self.get_curr_thread()
        if thread == self.tk_thread or isinstance(thread, _DummyThread):
            return tk_attr(*a, **kw)
        result, raise_result = response = [
         None, None]
        self.request_queue.put(response, tk_attr, a, kw)
        while raise_result is None and self.tk_widget is not None:
            _sleep0.0001
            result, raise_result = response

        if raise_result:
            raise result
        return result

    def hook(self, tk_widget=None):
        if tk_widget is None:
            tk_widget = self.tk_widget
        if tk_widget is None or hasattr(tk_widget, '_tk'):
            return
        if self._hook_status == TKHOOK_HOOKED:
            return
        self.tk_widget = tk_widget
        tk_widget._tk = tk_widget.tk
        tk_widget.tk = self
        self._hook_status = TKHOOK_HOOKED
        self.after_call_id = tk_widget.after(0, self.process_requests)

    def unhook(self):
        if not hasattr(self.tk_widget, '_tk'):
            return
        if self._hook_status != TKHOOK_HOOKED:
            return
        if self.after_call_id is None:
            self.tk_widget.tk = self.tk_widget._tk
            self._hook_status = TKHOOK_UNHOOKED
            del self.tk_widget._tk
            self.tk_widget = None
        else:
            self._hook_status = TKHOOK_UNHOOKING

    def process_requests(self):
        cleanup = True
        while cleanup:
            cleanup = False
            while self.tk_widget is not None and self._hook_status != TKHOOK_UNHOOKED or cleanup:
                try:
                    response, func, a, kw = self.request_queue.get_nowait()
                except Exception:
                    break

                try:
                    response[:] = (
                     func(*a, **kw), False)
                except Exception as e:
                    response[:] = (
                     e, True)

            if self._hook_status == TKHOOK_UNHOOKING:
                self.tk_widget.tk = self.tk_widget._tk
                self._hook_status = TKHOOK_UNHOOKED
                del self.tk_widget._tk
                self.after_call_id = self.tk_widget = None
                cleanup = True

        if self._hook_status == TKHOOK_HOOKED and self.tk_widget is not None:
            self.after_call_id = self.tk_widget.after(self.idle_time, self.process_requests)


def _tk_init_override(self, *a, **kw):
    self._orig_init(*a, **kw)
    if not hasattr(self.tk, 'hook'):
        TkWrapper().hookself


def _tk_destroy_override(self, *a, **kw):
    self._orig_destroy(*a, **kw)
    if hasattr(self.tk, 'unhook'):
        self.tk.unhook()


if not hasattr(Tk, '_orig_init'):
    Tk._orig_init = Tk.__init__
    Tk.__init__ = _tk_init_override
if not hasattr(Tk, '_orig_destroy'):
    Tk._orig_destroy = Tk.destroy
    Tk.destroy = _tk_destroy_override