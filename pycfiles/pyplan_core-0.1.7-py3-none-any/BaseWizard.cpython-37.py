# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/wizards/BaseWizard.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 1656 bytes
import json, autopep8
from pandas import MultiIndex

class BaseWizard(object):

    def getLastDefinition(self, definition):
        newDef = definition.replace('result=', '_df =').replace('result =', '_df =')
        return newDef

    def getColumnList(self, model, params):
        res = []
        nodeId = params['nodeId']
        if model.existNode(nodeId):
            nodeResult = model.getNode(nodeId).result
            for nn, idx in enumerate(nodeResult.index.names):
                if idx is not None:
                    res.append(dict(field=idx, type='index', dtype=(self.kindToString(nodeResult.index.levels[nn].values.dtype.kind if isinstance(nodeResult.index, MultiIndex) else nodeResult.index.values.dtype.kind))))

            for nn, cols in enumerate(list(nodeResult.columns)):
                if cols is not None:
                    res.append(dict(field=cols, type='column', dtype=(self.kindToString(nodeResult.dtypes[nn].kind))))

        return res

    def kindToString(self, kind):
        """Returns the data type on human-readable string
        """
        if kind in {'U', 'S'}:
            return 'string'
        if kind in {'b'}:
            return 'boolean'
        if kind in {'f', 'i', 'u', 'c'}:
            return 'numeric'
        if kind in {'M', 'm'}:
            return 'date'
        if kind in {'O'}:
            return 'object'
        if kind in {'V'}:
            return 'void'

    def formatDefinition(self, definition):
        return autopep8.fix_code(definition)