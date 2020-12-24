# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/IOEngine.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 2458 bytes


class IOEngine(object):

    def __init__(self, node):
        self.node = node
        self.inputs = []
        self.outputs = []

    def release(self):
        self.inputs = None
        self.outputs = None
        self.node = None

    def updateInputs(self, names):
        for inputNode in self.inputs:
            if inputNode not in names and self.node.model.existNode(inputNode):
                self.node.model.getNode(inputNode).ioEngine.removeOutput(self.node.identifier)

        newInputs = []
        for nodeId in names:
            if self.node.model.existNode(nodeId):
                newInputs.append(nodeId)
                if nodeId not in self.inputs:
                    self.node.model.getNode(nodeId).ioEngine.addOutput(self.node.identifier)

        self.inputs = newInputs

    def removeOutput(self, nodeId):
        if nodeId in self.outputs:
            self.outputs.remove(nodeId)

    def removeInput(self, nodeId):
        if nodeId in self.inputs:
            self.inputs.remove(nodeId)

    def addOutput(self, nodeId):
        self.outputs.append(nodeId)

    def updateNodeId(self, oldId, newId):
        for inputNode in self.inputs:
            if self.node.model.existNode(inputNode):
                self.node.model.getNode(inputNode).ioEngine.updateOutputId(oldId, newId)

        for outputNode in self.outputs:
            if self.node.model.existNode(outputNode):
                self.node.model.getNode(outputNode).ioEngine.updateInputId(oldId, newId)

    def updateOnDeleteNode(self):
        for inputNode in self.inputs:
            if self.node.model.existNode(inputNode):
                self.node.model.getNode(inputNode).ioEngine.removeOutput(self.node.identifier)

        for outputNode in self.outputs:
            if self.node.model.existNode(outputNode):
                self.node.model.getNode(outputNode).ioEngine.removeInput(self.node.identifier)

    def updateOutputId(self, oldId, newId):
        if oldId in self.outputs:
            self.outputs.remove(oldId)
        self.outputs.append(newId)

    def updateInputId(self, oldId, newId):
        if oldId in self.inputs:
            self.inputs.remove(oldId)
        self.inputs.append(newId)
        self.node.updateDefinitionForChangeId(oldId, newId)