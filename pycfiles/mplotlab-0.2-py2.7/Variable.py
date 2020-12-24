# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\models\Variable.py
# Compiled at: 2016-02-07 09:44:32
from AbcModel import AbcModel, MODELS, STRING
from Source import Source
from numpy import *

class Variable(AbcModel):
    attributeInfos = list(AbcModel.attributeInfos)
    attributeInfos.extend([
     (
      'source', (Source, Source, Source(), 'data')),
     (
      'formula',
      (str, STRING, '',
       'formula to compose with other variable data ' + "(ex: 'sin(T)' with 'T' a source name)" + 'It uses numpy expressions'))])

    def getVariableData(self):
        sourceValues = self.get_source().getSourceData()
        values = self.applyFormula(sourceValues)
        return values

    def applyFormula(self, sourceValues):
        """
        @param sourceValues : np.array
        @param sources : dict
            ex : {'T':<numpyarray>}
        """
        formula = self.get_formula()
        values = sourceValues
        if formula != '':
            container = self.get_container()
            if container is None:
                raise Exception('variable not registered. Cannot perform formula evaluation')
            sources = self.get_container().getSources()
            values = eval(formula, globals(), {s.get_name():s.getSourceData() for s in sources})
        return values