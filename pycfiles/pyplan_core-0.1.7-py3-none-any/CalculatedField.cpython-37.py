# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/wizards/CalculatedField.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 1803 bytes
import pyplan_core.classes.wizards.BaseWizard as BaseWizard
import pandas as pd, jsonpickle, re

class Wizard(BaseWizard):

    def __init__(self):
        self.code = 'CalculatedField'

    def generateDefinition(self, model, params):
        nodeId = params['nodeId']
        formula = params['formula']
        name = params['name']
        if model.existNode(nodeId):
            currentDef = model.getNode(nodeId).definition
            newDef = self.getLastDefinition(currentDef)
            newDef = newDef + '\n# Generated new column'
            regex = '#(.+?)#'
            matches = re.finditer(regex, formula)
            formulaFields = []
            for matchNum, match in enumerate(matches):
                formulaFields.append(str(match.group(1)))

            dfFields = self.getColumnList(model, params)
            for field in formulaFields:
                dfField = [f for f in dfFields if f['field'] == field]
                if dfField is not None:
                    if len(dfField) == 1:
                        fieldDef = ''
                        if dfField[0]['type'] == 'column':
                            fieldDef = "_df['" + field.replace("'", "\\'") + "']"
                        else:
                            fieldDef = "_df.index.get_level_values('" + field.replace("'", "\\'") + "')"
                    key = '#' + field + '#'
                    formula = formula.replace(key, fieldDef)

            newDef = newDef + "\n_df['" + name.replace("'", '') + "'] = " + formula
            newDef = newDef + '\nresult = _df'
            model.getNode(nodeId).definition = self.formatDefinition(newDef)
            return 'ok'
        return ''