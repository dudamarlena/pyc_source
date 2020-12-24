# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\gui\widgets\daskflow.py
# Compiled at: 2018-05-17 15:54:06
# Size of source mod 2**32: 3653 bytes
from pyqtgraph.flowchart import FlowchartCtrlWidget, Flowchart, Node, NodeLibrary
from xicam.core.execution.workflow import Workflow
from xicam.plugins import manager as pluginmanager

class DaskFlow(FlowchartCtrlWidget):

    def __init__(self):
        self.flowchart = Flowchart()
        super(DaskFlow, self).__init__(self.flowchart)

    def fromDask(self, workflow: Workflow):
        for process in workflow.processes:
            node = Node((process.name), terminals={'inputTerminalName':{'io': 'in'},  'outputTerminalName':{'io': 'out'}})
            self.flowchart.addNode(node, process.name)