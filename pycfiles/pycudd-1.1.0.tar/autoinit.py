# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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