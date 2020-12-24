# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\api\system.py
# Compiled at: 2013-03-20 09:41:35
from . import base

class CPU(base.Child):
    kwargName = 'cpu'
    expectedKwargs = {'count': (0, 1), 
       'executionCap': (0, 1), 
       'hotplug': (0, 1), 
       'pae': (0, 1)}
    defaultKwargs = {}
    count = base.pyVmProp('cpuCount')
    executionCap = base.pyVmProp('cpuExecutionCap')
    hotplug = base.pyVmProp('cpuHotplug')
    pae = base.pyVmProp('pae')


class System(base.Child):
    kwargName = 'system'
    expectedKwargs = {'cpu': (0, 1), 
       'hwVirtualisation': (0, 1), 
       'memory': (0, 1), 
       'nestedPaging': (0, 1), 
       'ioapic': (0, 1)}
    defaultKwargs = {'cpu': CPU}
    hwVirtualisation = base.pyVmProp('enableHwVirt')
    ioapic = base.pyVmProp('ioapic')
    memory = base.pyVmProp('memory')
    nestedPaging = base.pyVmProp('nestedPaging')