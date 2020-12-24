# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/wizards/SelectRows.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 3295 bytes
import pyplan_core.classes.wizards.BaseWizard as BaseWizard
import pandas as pd, jsonpickle

class Wizard(BaseWizard):

    def __init__(self):
        self.code = 'SelectRows'

    def getValues(self, model, params):
        field = params['field']
        nodeId = params['nodeId']
        if model.existNode(nodeId):
            nodeResult = model.getNode(nodeId).result
            if field['type'] == 'index':
                pos = nodeResult.index.names.index(field['field'])
                return list(nodeResult.index.levels[pos].values)[:500]
            return list(nodeResult[field['field']].unique())[:500]

    def generateDefinition(self, model, params):
        nodeId = params['nodeId']
        if model.existNode(nodeId):
            nodeResult = model.getNode(nodeId).result
            currentDef = model.getNode(nodeId).definition
            newDef = currentDef
            conditions = ''
            for filterItem in params['filters']:
                conditions = conditions + self.generateFilter(nodeResult, filterItem) + ' & '

            if conditions != '':
                conditions = conditions[:-3]
            if conditions != '':
                newDef = self.getLastDefinition(currentDef)
                newDef = newDef + '\n' + '# applied filters'
                newDef = newDef + '\n' + '_conditions = ' + conditions
                newDef = newDef + '\n' + 'result = _df[_conditions]'
            model.getNode(nodeId).definition = self.formatDefinition(newDef)
            return 'ok'
        return ''

    def generateFilter(self, nodeResult, filterItem):
        res = ''
        field = filterItem['field']
        values = filterItem['values']
        operator = filterItem['operator']
        selector = ''
        if filterItem['type'] == 'column':
            selector = "_df['" + field.replace("'", "\\'") + "']"
        else:
            selector = "_df.index.get_level_values('" + field.replace("'", "\\'") + "')"
        if filterItem['dtype'] == 'numeric':
            if operator == 'between':
                res = '(' + selector + ' > ' + str(values[0]) + ')'
                res = res + ' & (' + selector + ' < ' + str(values[1]) + ')'
            else:
                if operator == 'outside':
                    res = '(' + selector + ' < ' + str(values[0]) + ')'
                    res = res + ' & (' + selector + ' > ' + str(values[1]) + ')'
                else:
                    if operator == 'defined':
                        res = '(~' + selector + '.isnull())'
                    else:
                        if operator == 'undefined':
                            res = '(' + selector + '.isnull())'
                        else:
                            res = '(' + selector + ' ' + operator + ' ' + str(values[0]) + ')'
        else:
            if operator == 'contains':
                res = '(' + selector + ".str.contains('" + str(values[0]).replace("'", "\\'") + "'))"
            else:
                if operator == 'notcontains':
                    res = '(~' + selector + ".str.contains('" + str(values[0]).replace("'", "\\'") + "'))"
                else:
                    res = '(' + selector + ' ' + operator + " '" + str(values[0]).replace("'", "\\'") + "')"
        return res