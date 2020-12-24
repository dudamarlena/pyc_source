# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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