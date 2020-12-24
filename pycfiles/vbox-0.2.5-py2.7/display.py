# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\api\display.py
# Compiled at: 2013-03-20 09:41:35
from . import base

class Display(base.Child):
    kwargName = 'display'
    expectedKwargs = {'accelerate3d': (0, 1), 
       'memory': (0, 1)}
    defaultKwargs = {'accelerate3d': None, 
       'memory': None}
    accelerate3d = base.pyVmProp('accelerate3d')
    memory = base.pyVmProp('videoMemory')