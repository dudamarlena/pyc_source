# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/dynamics/FactoryDynamic.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 951 bytes
import pyplan_core.classes.dynamics.CubepyDynamic as CubepyDynamic
import pyplan_core.classes.dynamics.XArrayDynamic as XArrayDynamic
import pyplan_core.classes.dynamics.PureXArrayDynamic as PureXArrayDynamic

class FactoryDynamic(object):

    @staticmethod
    def createInstance(circularNodes, node):
        if node is not None:
            DynamicClass = FactoryDynamic.findDynamicClass(circularNodes, node)
            return DynamicClass()

    @staticmethod
    def findDynamicClass(circularNodes, node):
        for nodeId in circularNodes:
            if node.model.existNode(nodeId):
                _def = node.model.getNode(nodeId).definition
                if 'cp.dynamic(' in _def:
                    return CubepyDynamic
                if 'pp.dynamic(' in _def:
                    return XArrayDynamic
                if 'dynamic(' in _def:
                    return PureXArrayDynamic

        return PureXArrayDynamic