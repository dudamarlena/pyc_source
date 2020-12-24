# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/wizards/DataframeGroupby.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 1396 bytes
import pyplan_core.classes.wizards.BaseWizard as BaseWizard
import pandas as pd, jsonpickle

class Wizard(BaseWizard):

    def __init__(self):
        self.code = 'DataframeGroupby'

    def generateDefinition(self, model, params):
        nodeId = params['nodeId']
        if model.existNode(nodeId):
            currentDef = model.getNode(nodeId).definition
            newDef = self.getLastDefinition(currentDef)
            newDef = newDef + '\n# Groupby'
            agg = params['agg']
            need_join = False
            group_by = ''
            if 'columns' in params:
                if len(params['columns']) > 0:
                    group_by = f".groupby({params['columns']})"
                    for key in agg:
                        if len(agg[key]) == 1:
                            agg[key] = str(agg[key][0])
                        else:
                            need_join = True

            newDef = newDef + f"\n_df = _df{group_by}.agg({jsonpickle.dumps(agg)})"
            if need_join:
                newDef = newDef + '\n# Format columns name'
                newDef = newDef + "\n_df.columns = _df.columns.map('_'.join)"
            newDef = newDef + '\nresult = _df'
            model.getNode(nodeId).definition = self.formatDefinition(newDef)
            return 'ok'
        return ''