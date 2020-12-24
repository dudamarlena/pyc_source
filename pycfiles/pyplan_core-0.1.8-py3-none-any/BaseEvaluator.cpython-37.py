# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/evaluators/BaseEvaluator.py
# Compiled at: 2020-04-30 15:43:10
# Size of source mod 2**32: 9160 bytes
import json, numpy as np, pandas as pd, inspect, jsonpickle
from pyplan_core import cubepy
import pyplan_core.classes.common.filterChoices as filterChoices
from pyplan_core.classes.common.indexValuesReq import IndexValuesReq

class BaseEvaluator(object):
    __doc__ = '\n    Base Class to manage node evaluators\n    '

    def createResult(self, result, structure, resultIsJson=False, onRow=None, onColumn=None, node=None, pageInfo=None):
        if resultIsJson:
            res = {'resultType':json.dumps(structure), 
             'result':json.loads(result)}
            if onRow is not None:
                res['onRow'] = onRow
            if onColumn is not None:
                res['onColumn'] = onColumn
            if pageInfo is not None:
                res['pageInfo'] = pageInfo
        else:
            if node is not None:
                if node.numberFormat:
                    res['numberFormat'] = node.numberFormat
            return json.dumps(res)
            res = {'resultType':json.dumps(structure), 
             'result':result, 
             'onRow':onRow, 
             'onColumn':onColumn}
            if pageInfo is not None:
                res['pageInfo'] = pageInfo
            if node is not None:
                if node.model.isNodeInScenario(node.identifier):
                    res['scenario'] = True
                if node.numberFormat:
                    res['numberFormat'] = node.numberFormat
        return json.dumps(res)

    def getStructure(self, result):
        structure = dict()
        structure['type'] = str(type(result))
        return structure

    def checkStructure(self, result, resultType):
        """ Check current vs result structure. Result False for distinct structure """
        res = True
        if resultType:
            try:
                structure = json.loads(resultType)
                result_structure = self.getStructure(result)
                if structure['type'] != result_structure['type']:
                    res = False
            except Exception as ex:
                try:
                    print(f"Error checking structure: {ex}")
                finally:
                    ex = None
                    del ex

        return res

    def evaluateNode(self, result, nodeDic, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0):
        result_structure = self.getStructure(result)
        if isinstance(result, np.ndarray):
            return self.createResult((result.tolist()), result_structure, node=(nodeDic[nodeId]))
        if callable(result):
            aux = {'params': inspect.getargspec(result)[0]}
            return self.createResult((jsonpickle.encode(aux)), result_structure, node=(nodeDic[nodeId]))
        try:
            return self.createResult(result, result_structure, node=(nodeDic[nodeId]))
        except:
            return self.createResult((str(result)), result_structure, node=(nodeDic[nodeId]))

    def getCubeValues(self, result, nodeDic, nodeId, query):
        raise NotImplementedError

    def getCubeDimensionValues(self, result, nodeDic, nodeId, query):
        raise NotImplementedError

    def getCubeMetadata(self, result, nodeDic, nodeId):
        raise NotImplementedError

    def generateEmptyPreviewResponse(self, nodeDic, nodeId):
        msg = 'This node does not return any value'
        if nodeDic[nodeId].nodeClass == 'button':
            msg = 'Successfully executed'
        res = {'resultType':'',  'dims':[],  'console':nodeDic[nodeId].lastEvaluationConsole, 
         'preview':msg}
        return json.dumps(res)

    def previewNode(self, nodeDic, nodeId):
        if nodeDic[nodeId].result is not None:
            res = {'resultType':str(type(nodeDic[nodeId].result)),  'dims':[],  'console':nodeDic[nodeId].lastEvaluationConsole, 
             'preview':str(nodeDic[nodeId].result)[:1000]}
            if callable(nodeDic[nodeId].result):
                try:
                    res['preview'] += '\nparams: ' + str(inspect.getargspec(nodeDic[nodeId].result)[0])
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

            return json.dumps(res)
        return self.generateEmptyPreviewResponse(nodeDic, nodeId)

    def setNodeValueChanges(self, nodeDic, nodeId, changes):
        value = None
        if changes is not None:
            if len(changes['changes']) == 1:
                if len(changes['changes'][0]['filterList']) == 0:
                    value = changes['changes'][0]['definition']
                    value = nodeDic[nodeId].sanitizeDefinition(value)
        if value is not None:
            nodeDic[nodeId].definition = value

    def isTable(self, node):
        return '0'

    def isIndexed(self, result):
        return False

    def getIndexes(self, node, result=None):
        return []

    def getIndexesWithLevels(self, node, result=None):
        return []

    def getIndexValues--- This code section failed: ---

 L. 152         0  BUILD_LIST_0          0 
                2  STORE_FAST               'res'

 L. 153         4  LOAD_FAST                'data'
                6  LOAD_ATTR                node_id
                8  POP_JUMP_IF_FALSE   156  'to 156'

 L. 154        10  LOAD_FAST                'data'
               12  LOAD_ATTR                node_id
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  LOAD_FAST                'data'
               20  LOAD_ATTR                node_id
               22  LOAD_FAST                'nodeDic'
               24  COMPARE_OP               in
               26  BINARY_AND       
               28  POP_JUMP_IF_FALSE   254  'to 254'

 L. 155        30  LOAD_FAST                'nodeDic'
               32  LOAD_FAST                'data'
               34  LOAD_ATTR                node_id
               36  BINARY_SUBSCR    
               38  STORE_FAST               'node'

 L. 156        40  LOAD_FAST                'result'
               42  LOAD_CONST               None
               44  COMPARE_OP               is
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L. 157        48  LOAD_FAST                'node'
               50  LOAD_ATTR                result
               52  STORE_FAST               'result'
             54_0  COME_FROM            46  '46'

 L. 159        54  LOAD_FAST                'data'
               56  LOAD_ATTR                index_id
               58  FORMAT_VALUE          0  ''
               60  LOAD_STR                 '.'
               62  LOAD_FAST                'data'
               64  LOAD_ATTR                node_id
               66  FORMAT_VALUE          0  ''
               68  BUILD_STRING_3        3 
               70  LOAD_FAST                'self'
               72  LOAD_METHOD              getIndexes
               74  LOAD_FAST                'node'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  COMPARE_OP               in
               80  POP_JUMP_IF_FALSE   254  'to 254'

 L. 160        82  LOAD_FAST                'self'
               84  LOAD_METHOD              isIndexed
               86  LOAD_FAST                'result'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_JUMP_IF_FALSE   136  'to 136'

 L. 161        92  SETUP_LOOP          154  'to 154'
               94  LOAD_FAST                'result'
               96  LOAD_ATTR                index
               98  LOAD_ATTR                levels
              100  GET_ITER         
            102_0  COME_FROM           116  '116'
              102  FOR_ITER            132  'to 132'
              104  STORE_FAST               'index'

 L. 162       106  LOAD_FAST                'index'
              108  LOAD_ATTR                name
              110  LOAD_FAST                'data'
              112  LOAD_ATTR                index_id
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   102  'to 102'

 L. 163       118  LOAD_FAST                'index'
              120  LOAD_ATTR                values
              122  LOAD_METHOD              tolist
              124  CALL_METHOD_0         0  '0 positional arguments'
              126  STORE_FAST               'res'

 L. 164       128  BREAK_LOOP       
              130  JUMP_BACK           102  'to 102'
              132  POP_BLOCK        
              134  JUMP_ABSOLUTE       254  'to 254'
            136_0  COME_FROM            90  '90'

 L. 166       136  LOAD_FAST                'result'
              138  LOAD_FAST                'data'
              140  LOAD_ATTR                index_id
              142  BINARY_SUBSCR    
              144  LOAD_METHOD              unique
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  LOAD_METHOD              tolist
              150  CALL_METHOD_0         0  '0 positional arguments'
              152  STORE_FAST               'res'
            154_0  COME_FROM_LOOP       92  '92'
              154  JUMP_FORWARD        254  'to 254'
            156_0  COME_FROM             8  '8'

 L. 168       156  LOAD_FAST                'data'
              158  LOAD_ATTR                index_id
              160  LOAD_CONST               None
              162  COMPARE_OP               is-not
              164  LOAD_FAST                'data'
              166  LOAD_ATTR                index_id
              168  LOAD_FAST                'nodeDic'
              170  COMPARE_OP               in
              172  BINARY_AND       
              174  POP_JUMP_IF_FALSE   254  'to 254'

 L. 169       176  LOAD_FAST                'nodeDic'
              178  LOAD_FAST                'data'
              180  LOAD_ATTR                index_id
              182  BINARY_SUBSCR    
              184  STORE_FAST               'node'

 L. 170       186  LOAD_FAST                'result'
              188  LOAD_CONST               None
              190  COMPARE_OP               is
              192  POP_JUMP_IF_FALSE   200  'to 200'

 L. 171       194  LOAD_FAST                'node'
              196  LOAD_ATTR                result
              198  STORE_FAST               'result'
            200_0  COME_FROM           192  '192'

 L. 172       200  LOAD_GLOBAL              isinstance
              202  LOAD_FAST                'result'
              204  LOAD_GLOBAL              cubepy
              206  LOAD_ATTR                Index
              208  CALL_FUNCTION_2       2  '2 positional arguments'
              210  POP_JUMP_IF_FALSE   224  'to 224'

 L. 173       212  LOAD_FAST                'result'
              214  LOAD_ATTR                values
              216  LOAD_METHOD              tolist
              218  CALL_METHOD_0         0  '0 positional arguments'
              220  STORE_FAST               'res'
              222  JUMP_FORWARD        254  'to 254'
            224_0  COME_FROM           210  '210'

 L. 174       224  LOAD_GLOBAL              isinstance
              226  LOAD_FAST                'result'
              228  LOAD_GLOBAL              np
              230  LOAD_ATTR                ndarray
              232  CALL_FUNCTION_2       2  '2 positional arguments'
              234  POP_JUMP_IF_FALSE   246  'to 246'

 L. 175       236  LOAD_FAST                'result'
              238  LOAD_METHOD              tolist
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  STORE_FAST               'res'
              244  JUMP_FORWARD        254  'to 254'
            246_0  COME_FROM           234  '234'

 L. 177       246  LOAD_GLOBAL              list
              248  LOAD_FAST                'result'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  STORE_FAST               'res'
            254_0  COME_FROM           244  '244'
            254_1  COME_FROM           222  '222'
            254_2  COME_FROM           174  '174'
            254_3  COME_FROM           154  '154'
            254_4  COME_FROM            80  '80'
            254_5  COME_FROM            28  '28'

 L. 178       254  LOAD_FAST                'data'
              256  LOAD_ATTR                text1
          258_260  POP_JUMP_IF_FALSE   350  'to 350'

 L. 179       262  LOAD_FAST                'data'
              264  LOAD_ATTR                text1
              266  LOAD_METHOD              lower
              268  CALL_METHOD_0         0  '0 positional arguments'
              270  STORE_DEREF              'text1'

 L. 180       272  LOAD_FAST                'data'
              274  LOAD_ATTR                filter
              276  LOAD_GLOBAL              filterChoices
              278  LOAD_ATTR                CONTAINS
              280  LOAD_ATTR                value
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   312  'to 312'

 L. 181       288  LOAD_GLOBAL              list

 L. 182       290  LOAD_GLOBAL              filter
              292  LOAD_CLOSURE             'text1'
              294  BUILD_TUPLE_1         1 
              296  LOAD_LAMBDA              '<code_object <lambda>>'
              298  LOAD_STR                 'BaseEvaluator.getIndexValues.<locals>.<lambda>'
              300  MAKE_FUNCTION_8          'closure'
              302  LOAD_FAST                'res'
              304  CALL_FUNCTION_2       2  '2 positional arguments'
              306  CALL_FUNCTION_1       1  '1 positional argument'
              308  STORE_FAST               'res'
              310  JUMP_FORWARD        350  'to 350'
            312_0  COME_FROM           284  '284'

 L. 183       312  LOAD_FAST                'data'
              314  LOAD_ATTR                filter
              316  LOAD_GLOBAL              filterChoices
              318  LOAD_ATTR                NOT_CONTAINS
              320  LOAD_ATTR                value
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   350  'to 350'

 L. 184       328  LOAD_GLOBAL              list

 L. 185       330  LOAD_GLOBAL              filter
              332  LOAD_CLOSURE             'text1'
              334  BUILD_TUPLE_1         1 
              336  LOAD_LAMBDA              '<code_object <lambda>>'
              338  LOAD_STR                 'BaseEvaluator.getIndexValues.<locals>.<lambda>'
              340  MAKE_FUNCTION_8          'closure'
              342  LOAD_FAST                'res'
              344  CALL_FUNCTION_2       2  '2 positional arguments'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  STORE_FAST               'res'
            350_0  COME_FROM           324  '324'
            350_1  COME_FROM           310  '310'
            350_2  COME_FROM           258  '258'

 L. 186       350  LOAD_FAST                'res'
              352  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 154_0

    def getIndexType(self, nodeDic, nodeId, indexId):
        return 'S'

    def exportFlatNode(self, nodeDic, nodeId, numberFormat, columnFormat, fileName):
        if columnFormat == 'tab':
            columnFormat = '\t'
        decimalSep = '.'
        if numberFormat == 'TSPDSC':
            decimalSep = ','
        query = {'columns':self.getIndexes(nodeDic[nodeId]), 
         'filters':None}
        data = self.getCubeValues(nodeDic[nodeId].result, nodeDic, nodeId, query)
        realIndexes = [x['field'] for x in data['dims']]
        realIndexes = realIndexes + ['data_value']
        dimValues = [x['values'] for x in data['dims']]
        import itertools
        allCombinations = (itertools.product)(*dimValues)
        with open(fileName, 'w') as (f):
            f.write(columnFormat.join(realIndexes) + '\n')
            nn = 0
            for item in allCombinations:
                aa = 0
                f.write(columnFormat.join((str(e) for e in item)) + columnFormat)
                f.write(str(data['values'][nn]).replace('.', decimalSep) + '\n')
                nn += 1

            f.close()
        return True

    def dumpNodeToFile(self, nodeDic, nodeId, fileName):
        definition = nodeDic[nodeId].definition
        with open(fileName, 'w') as (f):
            f.write(definition)
            f.close()

    def geoUnclusterData(self, result, nodeDic, nodeId, rowIndex, attIndex, latField='latitude', lngField='longitude', geoField='geoField', labelField='labelField', sizeField='sizeField', colorField='colorField', iconField='iconField'):
        raise NotImplementedError

    def postCalculate(self, node, result):
        """Method executed after calculate node
        """
        pass

    def copyAsValues(self, result, nodeDic, nodeId):
        """ Copy node as values """
        raise NotImplementedError

    def checkDateFormat(self, np_array):
        if 'date' in np_array.dtype.name:

            def _cut(x):
                return x[:19]

            vfunc = np.vectorize(_cut)
            return vfunc(np_array.astype(str))
        return np_array