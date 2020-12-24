# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/wizards/sourcecsv.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 3571 bytes
import pyplan_core.classes.wizards.BaseWizard as BaseWizard
import pandas as pd, jsonpickle

class Wizard(BaseWizard):

    def __init__(self):
        self.code = 'sourcecsv'

    def getColumns(self, model, params):
        res = []
        current_path = model.getNode('current_path').result
        params['rows'] = 5000
        _df = self._openFile(params, current_path)
        totalReg = _df.shape[0]
        for nn, cols in enumerate(list(_df.columns)):
            if cols is not None:
                item = dict(field=cols, type='column', dtype=(self.kindToString(_df.dtypes[nn].kind)))
                if item['dtype'] != 'numeric':
                    uniqueCount = len(_df[cols].unique())
                    if uniqueCount / totalReg < 0.8:
                        item['type'] = 'index'
                res.append(item)

        return res

    def readFile(self, model, params):
        current_path = model.getNode('current_path').result
        _df = self._openFile(params, current_path)
        res = {'params':params, 
         'result':jsonpickle.decode(_df.to_json(orient='table'))}
        return res

    def generateDefinition(self, model, params):
        nodeId = params['nodeId']
        charcode = None if params['encoding'] == 'auto' else params['encoding']
        sep = None if params['sep'] == 'auto' else params['sep']
        index_col = None
        if 'indexes' in params:
            if len(params['indexes']) > 0:
                index_col = params['indexes']
        else:
            newDef = "result = pd.read_csv(current_path + '{}'".format(params['filename'])
            if params['filename'].lower().startswith('http'):
                newDef = "result = pd.read_csv('{}'".format(params['filename'])
            if charcode is not None:
                newDef = newDef + ", encoding='{}'".format(charcode)
            if sep is None:
                newDef = newDef + ', sep=None'
            else:
                newDef = newDef + ", sep='{}'".format(sep)
        if index_col is not None:
            newDef = newDef + ', index_col={}'.format(index_col)
        newDef = newDef + ')'
        model.getNode(nodeId).definition = self.formatDefinition(newDef)
        return 'ok'

    def _openFile(self, params, current_path):
        filename = current_path + params['filename']
        if params['filename'].lower().startswith('http'):
            filename = params['filename']
        sample = 5000
        charcode = None if params['encoding'] == 'auto' else params['encoding']
        sep = None if params['sep'] == 'auto' else params['sep']
        index_col = None
        if 'indexes' in params:
            if len(params['indexes']) > 0:
                index_col = params['indexes']
        codecs = [
         charcode, 'utf-8', 'cp850', 'cp852',
         'cp1250', 'cp1252', 'latin_1', 'ascii']
        nChance = 0
        while nChance < len(codecs):
            try:
                tryCharcode = codecs[nChance]
                _df = pd.read_csv(filename, encoding=tryCharcode, sep=sep,
                  nrows=sample,
                  index_col=index_col)
                if charcode is None:
                    if tryCharcode is not None:
                        params['encoding'] = tryCharcode
                return _df.head(int(params['rows']))
            except Exception as ex:
                try:
                    if "codec can't decode byte" in str(ex) and nChance + 1 < len(codecs):
                        nChance += 1
                    else:
                        raise ex
                finally:
                    ex = None
                    del ex