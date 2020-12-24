# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/evaluators/PandasEvaluator.py
# Compiled at: 2020-04-30 15:43:10
# Size of source mod 2**32: 23116 bytes
import json, numpy as np, pandas as pd
import pyplan_core.classes.evaluators.BaseEvaluator as BaseEvaluator
import pyplan_core.classes.common.filterChoices as filterChoices
from pyplan_core.classes.common.indexValuesReq import IndexValuesReq
from pyplan_core.cubepy.cube import kindToString
from pyplan_core import cubepy

class PandasEvaluator(BaseEvaluator):
    PAGESIZE = 100
    MAX_COLUMS = 5000

    def evaluateNode(self, result, nodeDic, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0):
        result_structure = self.getStructure(result)
        sby = np.nansum
        if summaryBy == 'avg':
            sby = np.nanmean
        else:
            if summaryBy == 'max':
                sby = np.nanmax
            else:
                if summaryBy == 'min':
                    sby = np.nanmin
                elif not fromRow is None:
                    if int(fromRow) <= 0:
                        fromRow = 1
                    if not toRow is None:
                        if int(toRow) < 1:
                            toRow = 100
                        fromRow = int(fromRow)
                        toRow = int(toRow)
                        _filters = {}
                        _rows = []
                        _columns = []
                        theResult = self.prepareDataframeForTable(result)
                        if rows is not None:
                            for row in rows:
                                if self.hasDim(theResult, str(row['field']).split('.')[0]):
                                    _rows.append(str(row['field']).split('.')[0])
                                    self.addToFilter(row, _filters)

                        if columns is not None:
                            for column in columns:
                                if self.hasDim(theResult, str(column['field']).split('.')[0]):
                                    _columns.append(str(column['field']).split('.')[0])
                                    self.addToFilter(column, _filters)

                        if dims is not None:
                            for dim in dims:
                                if self.hasDim(theResult, str(dim['field']).split('.')[0]):
                                    self.addToFilter(dim, _filters)

                        res = None
                        pageInfo = None
                        dfResult = None
                        if len(_rows) == 0 and len(_columns) == 0:
                            dfResult = self.applyFilter(theResult, _filters)
                            if dfResult.index is not None and dfResult.index.names is not None and len(dfResult.index.names) > 0 and dfResult.index.names[0] is not None:
                                serieResult = dfResult.agg(sby)
                                dfResult = pd.DataFrame({'total': serieResult}).T
                    else:
                        needT = False
                        if len(_rows) == 0:
                            needT = True
                            aux = _rows
                            _rows = _columns
                            _columns = aux
                        _filteredDataFrame = self.applyFilter(theResult, _filters)
                        dfResult = pd.DataFrame.pivot_table(_filteredDataFrame,
                          index=_rows, columns=_columns, aggfunc=sby, margins=False, margins_name='Total')
                        if needT:
                            dfResult = dfResult.T
                            aux = _rows
                            _rows = _columns
                            _columns = aux
                    if bottomTotal:
                        if dfResult.shape[0] > 1:
                            row_total = sby((dfResult.values), axis=0)
                            new_values = np.concatenate([
                             dfResult.values, [row_total]],
                              axis=0)
                            new_index = pd.Index(np.concatenate([
                             dfResult.index.values, ['Total']]))
                            _df = pd.DataFrame(data=new_values,
                              columns=(dfResult.columns),
                              index=new_index)
                            dfResult = _df
                    if rightTotal:
                        if dfResult.shape[1] > 1:
                            row_total = sby((dfResult.values), axis=1)
                            new_values = np.concatenate([
                             dfResult.values, row_total.reshape(row_total.size, 1)],
                              axis=1)
                            new_columns = np.concatenate([dfResult.columns, ['Total']])
                            _df = pd.DataFrame(data=new_values,
                              columns=new_columns,
                              index=(dfResult.index))
                            dfResult = _df
                    if dfResult.shape[0] > self.PAGESIZE:
                        if int(toRow) > dfResult.shape[0]:
                            toRow = dfResult.shape[0]
                        pageInfo = {'fromRow':int(fromRow),  'toRow':int(toRow), 
                         'totalRows':dfResult.shape[0]}
                        _range = list(range(fromRow - 1, toRow))
                        if bottomTotal:
                            _range = _range + [len(dfResult) - 1]
                        res = dfResult.iloc[_range].to_json(orient='split',
                          date_format='iso')
                else:
                    res = dfResult[:PandasEvaluator.MAX_COLUMS].to_json(orient='split',
                      date_format='iso')
                return self.createResult(res, result_structure, resultIsJson=True, pageInfo=pageInfo, node=(nodeDic[nodeId]), onRow=(_rows[0] if len(_rows) > 0 else None), onColumn=(_columns[0] if len(_columns) > 0 else None))

    def getStructure(self, result):
        structure = dict()
        structure['type'] = str(type(result))
        structure['columns'] = list(result.columns) if isinstance(result, pd.DataFrame) else []
        structure['indexes'] = []
        if self.isIndexed(result):
            structure['indexes'] = list(result.index.names)
        return structure

    def checkStructure(self, result, resultType):
        """ Check current vs result structure. Result False for distinct structure """
        res = True
        if resultType:
            try:
                structure = json.loads(resultType)
                result_structure = self.getStructure(result)
                res = structure['type'] == result_structure['type'] and all((elem in list(result_structure['columns']) for elem in list(structure['columns']))) and all((elem in list(result_structure['indexes']) for elem in list(structure['indexes'])))
            except Exception as ex:
                try:
                    print(f"Error checking structure: {ex}")
                finally:
                    ex = None
                    del ex

        return res

    def addToFilter(self, dim, filters):
        if 'values' in dim:
            if dim['values'] is not None:
                if len(dim['values']) > 0:
                    for itemValue in dim['values']:
                        field = str(dim['field']).split('.')[0]
                        if field in filters:
                            filters[field].append(itemValue['value'])
                        else:
                            filters[field] = [
                             itemValue['value']]

    def applyFilter(self, result, filters):
        if result is not None:
            if len(filters) > 0:
                res = result
                for key in filters:
                    res = res[res.index.get_level_values(key).isin(filters[key])]

                return res
            return result

    def hasDim(self, result, dim):
        if dim in result.index.names:
            return True
        if dim in result.dtypes.index:
            return True
        if dim in result.columns:
            return True
        return False

    def isIndexed(self, result):
        if result is not None:
            result = self.prepareDataframeForTable(result)
            obj = result
            if isinstance(obj, pd.DataFrame):
                return self._isIndexedDataframe(obj)
        return False

    def getIndexes(self, node, result=None):
        res = []
        if node._result is not None:
            obj = self.prepareDataframeForTable(node._result)
            if isinstance(obj, pd.DataFrame):
                if self.isIndexed(obj):
                    res = list(obj.index.names)
                    res = [x + '.' + node.identifier for x in res]
        return res

    def getIndexesWithLevels(self, node, result=None):
        res = []
        if result is None:
            result = node._result
        if result is not None:
            result = self.prepareDataframeForTable(result)
            if self.isIndexed(result):
                for indexItem in result.index.names:
                    itemDim = indexItem.split(',')[0]
                    item = {'field':itemDim + '.' + node.identifier,  'name':itemDim, 
                     'description':'',  'levels':[]}
                    if node.model.existNode(itemDim):
                        levelNode = node.model.getNode(itemDim)
                        if levelNode.title:
                            item['name'] = levelNode.title
                            item['description'] = levelNode.description
                        if levelNode.numberFormat:
                            item['numberFormat'] = levelNode.numberFormat
                    elif 'datetime' in result.index.get_level_values(itemDim).dtype.name:
                        item['numberFormat'] = '2,DD,0,,0,0,4,0,$,5,FULL,0'
                    res.append(item)

        return res

    def getIndexValues--- This code section failed: ---

 L. 237         0  BUILD_LIST_0          0 
                2  STORE_FAST               'res'

 L. 238         4  LOAD_FAST                'data'
                6  LOAD_ATTR                node_id
                8  POP_JUMP_IF_FALSE   174  'to 174'

 L. 239        10  LOAD_FAST                'data'
               12  LOAD_ATTR                node_id
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  LOAD_FAST                'data'
               20  LOAD_ATTR                node_id
               22  LOAD_FAST                'nodeDic'
               24  COMPARE_OP               in
               26  BINARY_AND       
               28  POP_JUMP_IF_FALSE   208  'to 208'

 L. 240        30  LOAD_FAST                'nodeDic'
               32  LOAD_FAST                'data'
               34  LOAD_ATTR                node_id
               36  BINARY_SUBSCR    
               38  STORE_FAST               'node'

 L. 241        40  LOAD_FAST                'result'
               42  LOAD_CONST               None
               44  COMPARE_OP               is
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L. 242        48  LOAD_FAST                'node'
               50  LOAD_ATTR                result
               52  STORE_FAST               'result'
             54_0  COME_FROM            46  '46'

 L. 243        54  LOAD_FAST                'data'
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
               80  POP_JUMP_IF_FALSE   208  'to 208'

 L. 244        82  LOAD_FAST                'self'
               84  LOAD_METHOD              isIndexed
               86  LOAD_FAST                'result'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_JUMP_IF_FALSE   154  'to 154'

 L. 245        92  LOAD_FAST                'self'
               94  LOAD_METHOD              prepareDataframeForTable

 L. 246        96  LOAD_FAST                'node'
               98  LOAD_ATTR                result
              100  CALL_METHOD_1         1  '1 positional argument'
              102  STORE_FAST               'prepared_result'

 L. 247       104  SETUP_LOOP          172  'to 172'
              106  LOAD_FAST                'prepared_result'
              108  LOAD_ATTR                index
              110  LOAD_ATTR                levels
              112  GET_ITER         
            114_0  COME_FROM           128  '128'
              114  FOR_ITER            150  'to 150'
              116  STORE_FAST               'index'

 L. 248       118  LOAD_FAST                'index'
              120  LOAD_ATTR                name
              122  LOAD_FAST                'data'
              124  LOAD_ATTR                index_id
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   114  'to 114'

 L. 249       130  LOAD_FAST                'self'
              132  LOAD_METHOD              checkDateFormat

 L. 250       134  LOAD_FAST                'index'
              136  LOAD_ATTR                values
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_METHOD              tolist
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  STORE_FAST               'res'

 L. 251       146  BREAK_LOOP       
              148  JUMP_BACK           114  'to 114'
              150  POP_BLOCK        
              152  JUMP_ABSOLUTE       208  'to 208'
            154_0  COME_FROM            90  '90'

 L. 253       154  LOAD_FAST                'result'
              156  LOAD_FAST                'data'
              158  LOAD_ATTR                index_id
              160  BINARY_SUBSCR    
              162  LOAD_METHOD              unique
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  LOAD_METHOD              tolist
              168  CALL_METHOD_0         0  '0 positional arguments'
              170  STORE_FAST               'res'
            172_0  COME_FROM_LOOP      104  '104'
              172  JUMP_FORWARD        208  'to 208'
            174_0  COME_FROM             8  '8'

 L. 254       174  LOAD_FAST                'data'
              176  LOAD_ATTR                index_id
              178  POP_JUMP_IF_FALSE   208  'to 208'

 L. 255       180  LOAD_FAST                'result'
              182  LOAD_CONST               None
              184  COMPARE_OP               is
              186  POP_JUMP_IF_FALSE   200  'to 200'

 L. 256       188  LOAD_FAST                'nodeDic'
              190  LOAD_FAST                'data'
              192  LOAD_ATTR                index_id
              194  BINARY_SUBSCR    
              196  LOAD_ATTR                result
              198  STORE_FAST               'result'
            200_0  COME_FROM           186  '186'

 L. 257       200  LOAD_GLOBAL              list
              202  LOAD_FAST                'result'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  STORE_FAST               'res'
            208_0  COME_FROM           178  '178'
            208_1  COME_FROM           172  '172'
            208_2  COME_FROM            80  '80'
            208_3  COME_FROM            28  '28'

 L. 258       208  LOAD_FAST                'data'
              210  LOAD_ATTR                text1
          212_214  POP_JUMP_IF_FALSE   304  'to 304'

 L. 259       216  LOAD_FAST                'data'
              218  LOAD_ATTR                text1
              220  LOAD_METHOD              lower
              222  CALL_METHOD_0         0  '0 positional arguments'
              224  STORE_DEREF              'text1'

 L. 260       226  LOAD_FAST                'data'
              228  LOAD_ATTR                filter
              230  LOAD_GLOBAL              filterChoices
              232  LOAD_ATTR                CONTAINS
              234  LOAD_ATTR                value
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   266  'to 266'

 L. 261       242  LOAD_GLOBAL              list

 L. 262       244  LOAD_GLOBAL              filter
              246  LOAD_CLOSURE             'text1'
              248  BUILD_TUPLE_1         1 
              250  LOAD_LAMBDA              '<code_object <lambda>>'
              252  LOAD_STR                 'PandasEvaluator.getIndexValues.<locals>.<lambda>'
              254  MAKE_FUNCTION_8          'closure'
              256  LOAD_FAST                'res'
              258  CALL_FUNCTION_2       2  '2 positional arguments'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  STORE_FAST               'res'
              264  JUMP_FORWARD        304  'to 304'
            266_0  COME_FROM           238  '238'

 L. 263       266  LOAD_FAST                'data'
              268  LOAD_ATTR                filter
              270  LOAD_GLOBAL              filterChoices
              272  LOAD_ATTR                NOT_CONTAINS
              274  LOAD_ATTR                value
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   304  'to 304'

 L. 264       282  LOAD_GLOBAL              list

 L. 265       284  LOAD_GLOBAL              filter
              286  LOAD_CLOSURE             'text1'
              288  BUILD_TUPLE_1         1 
              290  LOAD_LAMBDA              '<code_object <lambda>>'
              292  LOAD_STR                 'PandasEvaluator.getIndexValues.<locals>.<lambda>'
              294  MAKE_FUNCTION_8          'closure'
              296  LOAD_FAST                'res'
              298  CALL_FUNCTION_2       2  '2 positional arguments'
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  STORE_FAST               'res'
            304_0  COME_FROM           278  '278'
            304_1  COME_FROM           264  '264'
            304_2  COME_FROM           212  '212'

 L. 266       304  LOAD_FAST                'res'
              306  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 172_0

    def getIndexType--- This code section failed: ---

 L. 269         0  LOAD_STR                 'int16'
                2  LOAD_STR                 'int32'
                4  LOAD_STR                 'int64'
                6  LOAD_STR                 'float16'
                8  LOAD_STR                 'float32'
               10  LOAD_STR                 'float64'
               12  BUILD_LIST_6          6 
               14  STORE_FAST               'numerics'

 L. 270        16  LOAD_STR                 'S'
               18  STORE_FAST               'res'

 L. 271        20  LOAD_FAST                'nodeId'
               22  POP_JUMP_IF_FALSE   196  'to 196'

 L. 272        24  LOAD_FAST                'nodeId'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  LOAD_FAST                'nodeId'
               32  LOAD_FAST                'nodeDic'
               34  COMPARE_OP               in
               36  BINARY_AND       
               38  POP_JUMP_IF_FALSE   196  'to 196'

 L. 273        40  LOAD_FAST                'nodeDic'
               42  LOAD_FAST                'nodeId'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'node'

 L. 274        48  LOAD_FAST                'self'
               50  LOAD_METHOD              getIndexes
               52  LOAD_FAST                'node'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  STORE_FAST               'nodeIndexes'

 L. 275        58  LOAD_FAST                'indexId'
               60  LOAD_STR                 '.'
               62  BINARY_ADD       
               64  LOAD_FAST                'nodeId'
               66  BINARY_ADD       
               68  LOAD_FAST                'nodeIndexes'
               70  COMPARE_OP               in
               72  POP_JUMP_IF_FALSE   140  'to 140'

 L. 276        74  LOAD_FAST                'self'
               76  LOAD_METHOD              isIndexed
               78  LOAD_FAST                'node'
               80  LOAD_ATTR                result
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_JUMP_IF_FALSE   134  'to 134'

 L. 277        86  LOAD_FAST                'self'
               88  LOAD_METHOD              prepareDataframeForTable

 L. 278        90  LOAD_FAST                'node'
               92  LOAD_ATTR                result
               94  CALL_METHOD_1         1  '1 positional argument'
               96  STORE_FAST               'prepared_result'

 L. 279        98  SETUP_LOOP          138  'to 138'
              100  LOAD_FAST                'prepared_result'
              102  LOAD_ATTR                index
              104  LOAD_ATTR                levels
              106  GET_ITER         
            108_0  COME_FROM           120  '120'
              108  FOR_ITER            130  'to 130'
              110  STORE_FAST               'index'

 L. 280       112  LOAD_FAST                'index'
              114  LOAD_ATTR                name
              116  LOAD_FAST                'indexId'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   108  'to 108'

 L. 281       122  LOAD_STR                 'S'
              124  STORE_FAST               'res'

 L. 282       126  BREAK_LOOP       
              128  JUMP_BACK           108  'to 108'
              130  POP_BLOCK        
              132  JUMP_ABSOLUTE       196  'to 196'
            134_0  COME_FROM            84  '84'

 L. 285       134  LOAD_STR                 'S'
              136  STORE_FAST               'res'
            138_0  COME_FROM_LOOP       98  '98'
              138  JUMP_FORWARD        196  'to 196'
            140_0  COME_FROM            72  '72'

 L. 286       140  LOAD_FAST                'indexId'
              142  LOAD_FAST                'nodeIndexes'
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   196  'to 196'
              148  LOAD_GLOBAL              isinstance
              150  LOAD_FAST                'node'
              152  LOAD_ATTR                result
              154  LOAD_GLOBAL              cubepy
              156  LOAD_ATTR                Cube
              158  CALL_FUNCTION_2       2  '2 positional arguments'
              160  POP_JUMP_IF_FALSE   196  'to 196'

 L. 287       162  LOAD_GLOBAL              str
              164  LOAD_FAST                'node'
              166  LOAD_ATTR                result
              168  LOAD_METHOD              axis
              170  LOAD_FAST                'indexId'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  LOAD_ATTR                values
              176  LOAD_ATTR                dtype
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  LOAD_FAST                'numerics'
              182  COMPARE_OP               in
              184  POP_JUMP_IF_FALSE   192  'to 192'

 L. 288       186  LOAD_STR                 'N'
              188  STORE_FAST               'res'
              190  JUMP_FORWARD        196  'to 196'
            192_0  COME_FROM           184  '184'

 L. 290       192  LOAD_STR                 'S'
              194  STORE_FAST               'res'
            196_0  COME_FROM           190  '190'
            196_1  COME_FROM           160  '160'
            196_2  COME_FROM           146  '146'
            196_3  COME_FROM           138  '138'
            196_4  COME_FROM            38  '38'
            196_5  COME_FROM            22  '22'

 L. 291       196  LOAD_FAST                'res'
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 138_0

    def getCubeMetadata(self, result, nodeDic, nodeId):
        res = None
        _result = self.prepareDataframeForPivot(result)
        if isinstance(_result, pd.DataFrame):
            res = {'dims':[],  'measures':[],  'aggregator':'sum', 
             'isEditable':False, 
             'nodeProperties':{'title':nodeDic[nodeId].title if nodeDic[nodeId].title is not None else nodeDic[nodeId].identifier, 
              'numberFormat':nodeDic[nodeId].numberFormat, 
              'resultType':json.dumps(self.getStructure(result))}}
            for dim in self.getCubeIndexes(_result, nodeDic, nodeId):
                field = dim.split('.')[0]
                itemDim = {'field':dim, 
                 'name':field}
                if field in nodeDic:
                    if nodeDic[field].numberFormat:
                        itemDim['numberFormat'] = nodeDic[field].numberFormat
                elif 'datetime' in _result.index.get_level_values(field).dtype.name:
                    itemDim['numberFormat'] = '2,DD,0,,0,0,4,0,$,5,FULL,0'
                res['dims'].append(itemDim)

            res['dims'].append({'field':'data_index', 
             'name':'Data Index'})
            numerics = [
             'int16', 'int32', 'int64',
             'float16', 'float32', 'float64']
            for col in _result.columns:
                res['measures'].append({'field':str(col), 
                 'name':str(col)})

            _result = None
        return res

    def getCubeIndexes(self, result, nodeDic, nodeId):
        res = list(result.index.names)
        res = [x + '.' + nodeDic[nodeId].identifier for x in res]
        return res

    def getCubeValues(self, result, nodeDic, nodeId, query):
        _result = self.prepareDataframeForPivot(result)
        if isinstance(_result, pd.DataFrame):
            cube_indexes = self.getCubeIndexes(_result, nodeDic, nodeId)
            _filters = {}
            if query['filters'] is not None:
                for dim in query['filters']:
                    if 'values' in dim and dim['values'] is not None and len(dim['values']) > 0:
                        for itemValue in dim['values']:
                            field = str(dim['field']).split('.')[0]
                            if field in _filters:
                                _filters[field].append(itemValue)
                            else:
                                _filters[field] = [
                                 itemValue]

            _filteredResult = self.applyFilter(_result, _filters)
            for col in query['columns']:
                if col in cube_indexes:
                    item = {'field':col,  'count':0, 
                     'values':_filteredResult.index.get_level_values(col.split('.')[0]).unique.tolist}
                    item['count'] = len(item['values'])

            _cols = [x.split('.')[0] for x in query['columns']]
            useCustomFillMeasures = False
            try:
                _aa = _result.groupMeasures
                useCustomFillMeasures = True
            except AttributeError as ex:
                try:
                    pass
                finally:
                    ex = None
                    del ex

            _measures = list(query['measures'])
            _agg = dict()
            for measure in list(_result.columns):
                _agg[measure] = 'sum'
                try:
                    if measure in _result.aggMeasures:
                        _agg[measure] = _result.aggMeasures[measure]
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

            _groupedDF = _filteredResult.agg(_agg).to_frame('Total').T if len(_cols) == 0 else _filteredResult.groupby(_cols, sort=False).agg(_agg)
            if useCustomFillMeasures:
                self._applyGroupMeasures(_groupedDF, _result.groupMeasures)
            finalDF = _groupedDF.reset_index.melt(id_vars=_cols, value_vars=(query['measures']),
              var_name='data_index',
              value_name='data_value')
            _kind = finalDF['data_value'].dtype.kind
            if _kind in {'f', 'i', 'u', 'c'}:
                if np.isinf(finalDF['data_value']).any:
                    finalDF['data_value'][np.isinf(finalDF['data_value'])] = 0
            finalDF['data_value'].fillna(0, inplace=True)
            firstCol = query['columns'] + ['data_index', 'data_value']
            sortedColumns = [x.split('.')[0] for x in query['columns']] + ['data_index', 'data_value']
            res = [firstCol] + finalDF[sortedColumns].values[:1000000].tolist
            _result = None
            return res

    def _applyGroupMeasures(self, groupedDF, groupMeasures):
        for key in groupMeasures:
            groupedDF[key] = groupMeasures[key](groupedDF)

    def getCubeDimensionValues(self, result, nodeDic, nodeId, query):
        _result = self.prepareDataframeForPivot(result)
        if isinstance(_result, pd.DataFrame):
            if len(query['columns']) > 0:
                dimension = query['columns'][(-1)]
            if dimension in nodeDic[nodeId].indexes:
                uniquelist = _result.index.get_level_values(dimension.split('.')[0]).unique
                return uniquelist.sort_values.tolist[:1000]
        return []

    def previewNode(self, nodeDic, nodeId):
        import pyplan_core.classes.Helpers as Helpers
        from sys import getsizeof
        res = {'resultType':str(type(nodeDic[nodeId].result)), 
         'dims':[],  'columns':[],  'console':nodeDic[nodeId].lastEvaluationConsole, 
         'preview':''}
        if isinstance(nodeDic[nodeId].result, pd.DataFrame):
            cube = nodeDic[nodeId].result
            if len(cube.index.names) > 1 or cube.index.names[0] is not None:
                res['dims'] = list(cube.index.names)
            for idx, col in enumerate(cube.columns.values[:500]):
                res['columns'].append(f"{col} ({cube.dtypes[idx].name})")

            res['preview'] += 'Rows: ' + str(len(cube.index))
            res['preview'] += '\nShape: ' + str(cube.shape)
            res['preview'] += '\nMemory: ' + str(round(cube.memory_usage(deep=True).sum / 1024 / 1024, 2)) + ' Mb'
            res['preview'] += '\nValues: \n' + cube.head(20).to_string
        else:
            if isinstance(nodeDic[nodeId].result, pd.Series):
                serie = nodeDic[nodeId].result
                if self.isIndexed(serie):
                    res['dims'] = list(serie.index.names)
                res['preview'] += 'Rows: ' + str(len(serie.index))
                res['preview'] += '\nMemory: ' + str(round(serie.memory_usage(deep=True) / 1024 / 1024, 2)) + ' Mb'
                res['preview'] += '\nValues: \n' + serie.head(20).to_string
            else:
                if isinstance(nodeDic[nodeId].result, pd.Index):
                    res['preview'] = str(nodeDic[nodeId].result)[:1000]
                return json.dumps(res)

    def ensureDataFrame(self, result):
        res = result
        if isinstance(res, pd.Series):
            res = pd.DataFrame({'values': res})
        return res

    def exportFlatNode(self, nodeDic, nodeId, numberFormat, columnFormat, fileName):
        if columnFormat == 'tab':
            columnFormat = '\t'
        decimalSep = '.'
        if numberFormat == 'TSPDSC':
            decimalSep = ','
        _result = self.ensureDataFrame(nodeDic[nodeId].result)
        if isinstance(_result, pd.DataFrame):
            _result.to_csv(fileName, sep=columnFormat, encoding='iso-8859-1')
            return True
        return False

    def postCalculate(self, node, result):
        """Method executed after calculate node
        """
        if node.nodeClass == 'index':
            if isinstance(result, pd.Index):
                if result.name is None:
                    result.name = node.identifier

    def copyAsValues(self, result, nodeDic, nodeId):
        """ Copy node as values """
        newDef = ''
        if isinstance(result, pd.Index):
            np.set_printoptions(threshold=(np.prod(result.values.shape)))
            values = np.array2string((result.values), separator=',', precision=20, formatter={'float_kind': lambda x:                            if np.isnan(x):
'np.nan' # Avoid dead code: repr(x)}).replace('\n', '')
            newDef = f"result = pd.Index({values})"
        else:
            return False
            nodeDic[nodeId].definition = newDef
            return True

    def _isIndexedDataframe(self, dataframe):
        """Return True if dataframe is an indexed dataframe"""
        return len(dataframe.index.names) > 1 or dataframe.index.names[0] is not None

    def prepareDataframeForTable(self, result):
        """ Prepare dataframe for use un tables and charts """
        df = result
        if isinstance(df, pd.Series):
            df = pd.DataFrame({'values': df})
        elif self._isIndexedDataframe(df):
            if df.size == 0:
                df['values'] = np.nan
            else:
                if len(df.columns) > 1:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.map(' | '.join)
                    df = df.stack
                    if isinstance(df, pd.Series):
                        df = pd.DataFrame({'values': df})
                    current_columns_name = list(df.index.names)
                    current_columns_name[len(current_columns_name) - 1] = 'Measures'
                    df.index.names = current_columns_name
        return df

    def prepareDataframeForPivot(self, result):
        """ Prepare dataframe for use in pivot cube"""
        df = result
        if isinstance(df, pd.Series):
            df = pd.DataFrame({'values': df})
        if self._isIndexedDataframe(df):
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.map(' | '.join)
            else:
                df = df.select_dtypes(include=['float64', 'int64'])
                if df.size == 0:
                    df['values'] = np.nan
                try:
                    df.groupMeasures = result.groupMeasures
                except:
                    pass

            try:
                df.aggMeasures = result.aggMeasures
            except:
                pass

        return df