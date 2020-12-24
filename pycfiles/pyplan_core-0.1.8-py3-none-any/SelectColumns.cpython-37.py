# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/wizards/SelectColumns.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 674 bytes
import pyplan_core.classes.wizards.BaseWizard as BaseWizard
import pandas as pd, jsonpickle

class Wizard(BaseWizard):

    def __init__(self):
        self.code = 'SelectColumns'

    def generateDefinition(self, model, params):
        nodeId = params['nodeId']
        if model.existNode(nodeId):
            currentDef = model.getNode(nodeId).definition
            newDef = self.getLastDefinition(currentDef)
            newDef = newDef + '\n# Selected columns'
            newDef = newDef + '\nresult = _df[' + str(params['columns']) + ']'
            model.getNode(nodeId).definition = self.formatDefinition(newDef)
            return 'ok'
        return ''