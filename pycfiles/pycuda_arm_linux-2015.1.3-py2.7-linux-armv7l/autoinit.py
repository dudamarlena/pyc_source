# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/pycuda/gl/autoinit.py
# Compiled at: 2015-06-16 13:16:13
from __future__ import absolute_import
import pycuda.driver as cuda, pycuda.gl as cudagl
cuda.init()
assert cuda.Device.count() >= 1
from pycuda.tools import make_default_context
context = make_default_context(lambda dev: cudagl.make_context(dev))
device = context.get_device()
import atexit
atexit.register(context.pop)