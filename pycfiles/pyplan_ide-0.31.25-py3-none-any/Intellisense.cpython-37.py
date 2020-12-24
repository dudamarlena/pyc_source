# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/Intellisense.py
# Compiled at: 2020-05-07 09:45:20
# Size of source mod 2**32: 15666 bytes
import inspect, os
from sys import exc_info
import numpy as np, numpydoc, pandas as pd
from pyplan_core import cubepy
import pyplan_core.classes.BaseNode as BaseNode
import pyplan_core.classes.PyplanFunctions as PyplanFunctions
from pyplan_core.classes.common.indexValuesReq import IndexValuesReq

class Intellisense(object):
    """Intellisense"""

    def __init__(self):
        self._operatorsDic = {'.':self.searchDot, 
         '[':self.searchBrackeys, 
         '==':self.searchOperators, 
         '>=':self.searchOperators, 
         '<=':self.searchOperators, 
         '!=':self.searchOperators, 
         '>':self.searchOperators, 
         '<':self.searchOperators}
        self._finalIndex = -1
        self._preIndex = -1
        self._operator = None
        self._prefix = None
        self._searchText = ''
        self._extraText = ''

    @property
    def operatorsDic(self):
        return self._operatorsDic

    def clearValues(self):
        self._finalIndex = -1
        self._preIndex = -1
        self._operator = None
        self._prefix = None
        self._searchText = ''
        self._extraText = ''

    def search(self, model, filterOptions):
        res = []
        self.clearValues()
        if filterOptions is not None:
            onlyClass = None
            if filterOptions['nodeClass'] is not None:
                if str(filterOptions['nodeClass']).lower() != 'all':
                    onlyClass = []
                    onlyClass.append(str(filterOptions['nodeClass']).lower())
            if 'extraClasses' in filterOptions:
                if isinstance(filterOptions['extraClasses'], list):
                    if len(filterOptions['extraClasses']) > 0:
                        if onlyClass is None:
                            onlyClass = []
                        onlyClass.extend((str(extraClass).lower() for extraClass in filterOptions['extraClasses']))
            moduleId = None
            if filterOptions['moduleId'] is not None:
                moduleId = str(filterOptions['moduleId']).lower()
            searchText = None
            index = None
            if filterOptions['text'] is not None:
                if filterOptions['text'] != '':
                    searchText = str(filterOptions['text']).lower()
                    for operator in self._operatorsDic:
                        index = searchText.rfind(operator)
                        if index > self._finalIndex:
                            self._operator = operator
                            self._finalIndex = index

                    if self._finalIndex != -1:
                        self._prefix = searchText[:self._finalIndex]
                        index = -1
                        for operator in self._operatorsDic:
                            index = searchText[:self._finalIndex].rfind(operator)
                            if index > self._preIndex:
                                self._preIndex = index
                                if self._preIndex != -1:
                                    if len(operator) == 1:
                                        self._prefix = searchText[self._preIndex + 1:self._finalIndex]
                                        self._extraText = searchText[:self._preIndex + 1]
                                    else:
                                        self._prefix = searchText[self._preIndex + 2:self._finalIndex]
                                        self._extraText = searchText[:self._preIndex + 2]
                                if len(filterOptions['text']) > self._finalIndex + 1:
                                    if len(self._operator) == 1:
                                        self._searchText = str(filterOptions['text'][self._finalIndex + 1:]).lower()
                                if len(filterOptions['text']) > self._finalIndex + 2 and len(self._operator) == 2:
                                    self._searchText = str(filterOptions['text'][self._finalIndex + 2:]).lower()

                        res = self._operatorsDic[self._operator](model, filterOptions, onlyClass, moduleId, self._searchText, self._prefix, self._extraText, self._operator)
                    else:
                        self._searchText = str(filterOptions['text']).lower()
                        res = self.searchDefault(model, filterOptions, onlyClass, moduleId, self._searchText, self._prefix, self._extraText)
        return res

    def searchDefault(self, model, filterOptions, onlyClass, moduleId, searchText, prefix, extraText):
        res = []
        for _, node in model.nodeDic.items():
            if not searchText is not None and node is not None or node.identifier.lower().find(searchText) >= 0 or node.title is not None and node.title.lower().find(searchText) >= 0:
                if onlyClass is None or node.nodeClass in onlyClass:
                    if moduleId is None or node.moduleId == moduleId:
                        toAppend = node.system or node.toObj(properties=[
                         'identifier', 'nodeClass', 'moduleId', 'title', 'description'])
                        toAppend['completeText'] = extraText + node.identifier
                        if filterOptions['fillDetail'] and node.nodeClass == 'function':
                            try:
                                _fn = node.result
                                toAppend['params'] = str(inspect.signature(_fn))
                                toAppend['description'] = str(inspect.getdoc(_fn))
                            except:
                                params = node.definition[node.definition.find('(') + 1:node.definition.find(')')]
                                toAppend['params'] = params

                    res.append(toAppend)

        return res

    def searchDot(self, model, filterOptions, onlyClass, moduleId, searchText, prefix, extraText, operator):
        res = []
        node = None
        if model.existNode(prefix):
            node = model.getNode(prefix)
            if node.isCalc:
                if filterOptions['fillDetail']:
                    res = self.describe(searchText, prefix, extraText, operator, type(node.result))
        else:
            localRes = {'pp': PyplanFunctions(model)}
            customImports = model.getCustomImports()
            if customImports:
                for keyParam in customImports:
                    localRes[keyParam] = customImports[keyParam]

            toExec = 'result =' + prefix
            try:
                try:
                    exec(compile(toExec, '<string>', 'exec'), globals(), localRes)
                    if filterOptions['fillDetail']:
                        res = self.describe(searchText, prefix, extraText, operator, localRes['result'])
                except:
                    print('Error al intentar compilar el prefijo ' + prefix + ' antes del .')
                    e = exc_info()[0]
                    print('<p>Error: %s</p>' % e)

            finally:
                localRes['pp'].release()
                del localRes['pp']

        return res

    def searchBrackeys(self, model, filterOptions, onlyClass, moduleId, searchText, prefix, extraText, operator):
        res = []
        if prefix is not None:
            if prefix != '':
                node = None
                indexes = None
                if model.existNode(prefix):
                    node = model.getNode(prefix)
                    if node.isCalc:
                        if isinstance(node.result, cubepy.Cube):
                            if filterOptions['fillDetail']:
                                indexes = model.getIndexes(node.identifier)
                                if indexes:
                                    for index in indexes:
                                        res.append({'identifier':index, 
                                         'nodeClass':'cube axis', 
                                         'moduleId':'', 
                                         'title':index, 
                                         'description':'se ha buscado un cubo', 
                                         'params':index, 
                                         'completeText':extraText + prefix + operator})

                        elif isinstance(node.result, pd.DataFrame) and filterOptions['fillDetail']:
                            for column in list(node.result.columns):
                                res.append({'identifier':column, 
                                 'nodeClass':'dataframe column', 
                                 'moduleId':'', 
                                 'title':column, 
                                 'description':'dataframe column', 
                                 'params':'"' + column + '"', 
                                 'completeText':extraText + prefix + operator})

        return res

    def searchOperators(self, model, filterOptions, onlyClass, moduleId, searchText, prefix, extraText, operator):
        res = []
        if prefix is not None:
            if prefix != '':
                node = None
                indexValues = None
                if model.existNode(prefix):
                    node = model.getNode(prefix)
                    if node.isCalc:
                        if node.nodeClass == 'index':
                            if filterOptions['fillDetail']:
                                indexValues = model.getIndexValues(None, IndexValuesReq(node_id=(node.identifier)))
                                if indexValues:
                                    for value in indexValues:
                                        finalValue = str(value)
                                        finalParam = value
                                        if isinstance(value, str):
                                            finalValue = "'" + value + "'"
                                            finalParam = finalValue
                                        res.append({'identifier':finalValue, 
                                         'nodeClass':'index value', 
                                         'moduleId':'', 
                                         'title':finalValue, 
                                         'description':'se ha buscado un indice', 
                                         'params':finalParam, 
                                         'completeText':extraText + prefix + operator})

        return res

    @staticmethod
    def describe(text, prefix, extraText, operator, objectType=None):
        res = []
        _prefix = prefix + operator
        if text == _prefix:
            text = ''
            _prefix = ''
        _members = inspect.getmembers(objectType)
        for _member in _members:
            if '__' not in str(_member[0]) and not text is None:
                if text in str(_member[0]).lower():
                    if inspect.isfunction(_member[1]) or inspect.isclass(_member[1]):
                        _doc = inspect.getdoc(_member[1])
                        if _doc is not None:
                            _params = ''
                            try:
                                _params = str(inspect.signature(_member[1]))
                                _params = _params.replace('self,', '')
                            except:
                                _params = ''

                            res.append({'identifier':_prefix + _member[0], 
                             'nodeClass':'helper' if prefix == 'cp' else 'function' if inspect.isfunction(_member[1]) else 'class', 
                             'moduleId':'', 
                             'title':_prefix + _member[0], 
                             'description':_doc, 
                             'params':_params, 
                             'completeText':extraText + _prefix + _member[0]})
                    elif inspect.isroutine(_member[1]):
                        _doc = inspect.getdoc(_member[1])
                        try:
                            _params = ''
                            try:
                                _params = str(inspect.signature(_member[1]))
                                _params = _params.replace('self,', '')
                            except:
                                _params = ''

                            res.append({'identifier':_prefix + _member[0], 
                             'nodeClass':'method', 
                             'moduleId':'', 
                             'title':_prefix + _member[0], 
                             'description':_doc, 
                             'params':_params, 
                             'completeText':extraText + _prefix + _member[0]})
                        except:
                            _dot = str(objectType).find('.')
                            if _dot != -1 and str(objectType)[_dot - 5:_dot] == 'numpy':
                                info = numpydoc.docscrape.FunctionDoc(_member[1])
                                info['Signature'] = info['Signature'][info['Signature'].find('('):]
                                res.append({'identifier':_prefix + _member[0], 
                                 'nodeClass':'method', 
                                 'moduleId':'', 
                                 'title':_prefix + _member[0], 
                                 'description':_doc, 
                                 'params':info['Signature'], 
                                 'completeText':extraText + _prefix + _member[0]})
                            else:
                                print('Error al intentar obtener la signature del tipo de dato')
                                e = exc_info()[0]
                                print('<p>Error: %s</p>' % e)

                    else:
                        _doc = inspect.getdoc(_member[1])
                        try:
                            res.append({'identifier':_prefix + _member[0], 
                             'nodeClass':'other', 
                             'moduleId':'', 
                             'title':_prefix + _member[0], 
                             'description':_doc, 
                             'params':'', 
                             'completeText':extraText + _prefix + _member[0]})
                        except:
                            pass

        return res