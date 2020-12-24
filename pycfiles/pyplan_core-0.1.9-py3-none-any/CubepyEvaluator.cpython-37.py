# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/evaluators/CubepyEvaluator.py
# Compiled at: 2020-04-30 15:43:10
# Size of source mod 2**32: 26912 bytes
import json, numpy as np, pandas as pd, xarray as xr
from pyplan_core import cubepy
import pyplan_core.classes.evaluators.BaseEvaluator as BaseEvaluator
import pyplan_core.classes.common.filterChoices as filterChoices
from pyplan_core.classes.common.indexValuesReq import IndexValuesReq
from pyplan_core.cubepy.cube import kindToString, safemax, safemean, safemin, safesum

class CubepyEvaluator(BaseEvaluator):
    PAGESIZE = 100
    MAX_COLUMS = 5000

    def evaluateNode(self, result, nodeDic, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0):
        if isinstance(result, cubepy.Cube):
            return self.cubeEvaluate(result, nodeDic, nodeId, dims, rows, columns, summaryBy, bottomTotal, rightTotal, fromRow, toRow)
        if isinstance(result, cubepy.Index):
            return self.indexEvaluate(result, nodeDic, nodeId, dims, rows, columns, summaryBy, bottomTotal, rightTotal, fromRow, toRow)

    def cubeEvaluate(self, result, nodeDic, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0):
        result_structure = self.getStructure(result)
        sby = safesum
        if summaryBy == 'avg':
            sby = safemean
        else:
            if summaryBy == 'max':
                sby = safemax
            else:
                if summaryBy == 'min':
                    sby = safemin
                elif not fromRow is None:
                    if int(fromRow) <= 0:
                        fromRow = 1
                    if toRow is None or int(toRow) < 1:
                        toRow = 100
                    fromRow = int(fromRow)
                    toRow = int(toRow)
                    result = self.applyHierarchy(result, nodeDic, nodeId, dims, rows, columns, sby)
                    _filters = []
                    _rows = []
                    _columns = []
                    if rows is not None:
                        for row in rows:
                            if self.hasDim(result, str(row['field'])):
                                _rows.append(str(row['field']))
                                self.addToFilter(nodeDic, row, _filters)

                    if columns is not None:
                        for column in columns:
                            if self.hasDim(result, str(column['field'])):
                                _columns.append(str(column['field']))
                                self.addToFilter(nodeDic, column, _filters)

                    if dims is not None:
                        for dim in dims:
                            if self.hasDim(result, str(dim['field'])):
                                self.addToFilter(nodeDic, dim, _filters)

                    tmp = None
                    if len(_rows) == 0:
                        if len(_columns) == 0 and result.ndim > 0:
                            tmp = cubepy.Cube([], result.filter(_filters).reduce(sby))
                        else:
                            tmp = result.filter(_filters).reduce(sby, keep=(_rows + _columns)).transpose(_rows + _columns)
                        finalValues = tmp.values
                        finalIndexes = []
                        if tmp.ndim > 0:
                            finalIndexes = tmp.axes[0].values
                        finalColumns = [
                         'Total']
                        if tmp.ndim == 2:
                            finalColumns = tmp.axes[1].values
                        _totalRow = None
                        if bottomTotal and len(_rows) > 0:
                            if tmp.ndim == 1:
                                _totalRow = finalValues.sum(axis=0).reshape(1)
                    else:
                        _totalRow = finalValues.sum(axis=0).reshape(1, len(finalValues[0]))
                    _totalRow = _totalRow[0]
                    if rightTotal:
                        _totalRow = np.append(_totalRow, finalValues.sum())
                    if rightTotal:
                        if len(_columns) > 0:
                            if tmp.ndim == 1:
                                finalIndexes = np.append(finalIndexes, 'Total')
                                finalValues = np.append(finalValues,
                                  (finalValues.sum(axis=0).reshape(1)), axis=0)
                            else:
                                finalColumns = np.append(finalColumns, 'Total')
                                finalValues = np.append(finalValues, (finalValues.sum(axis=1).reshape(len(finalValues), 1)),
                                  axis=1)
                else:
                    if kindToString(finalValues.dtype.kind) == 'numeric':
                        if np.isinf(finalValues).any():
                            finalValues[np.isinf(finalValues)] = None
                    if pd.isnull(finalValues).any():
                        try:
                            finalValues = np.where(np.isnan(finalValues), None, finalValues)
                        except:
                            finalValues[pd.isnull(finalValues)] = None

                res = {}
                pageInfo = None
                onRow = None
                onColumn = None
        if len(_rows) == 0 and len(_columns) == 0:
            res = {'columns':[],  'index':[
              'Total'], 
             'data':[
              [
               finalValues.tolist()]]}
        else:
            if len(_rows) == 0:
                onColumn = _columns[0]
                res = {'columns':finalIndexes[:CubepyEvaluator.MAX_COLUMS].tolist(), 
                 'index':finalColumns, 
                 'data':[
                  finalValues[:CubepyEvaluator.MAX_COLUMS].tolist()]}
            else:
                if len(_columns) == 0:
                    if len(finalIndexes) > self.PAGESIZE:
                        pageInfo = {'fromRow':int(fromRow),  'toRow':int(toRow), 
                         'totalRows':len(finalIndexes)}
                    onRow = _rows[0]
                    res = {'columns':finalColumns, 
                     'index':finalIndexes[fromRow - 1:toRow].tolist(), 
                     'data':[[x] for x in finalValues[fromRow - 1:toRow].tolist()]}
                    if _totalRow is not None:
                        res['index'].append('Total')
                        res['data'].append(_totalRow.tolist())
                else:
                    onColumn = _columns[0]
                    onRow = _rows[0]
                    if len(finalIndexes) > self.PAGESIZE:
                        pageInfo = {'fromRow':int(fromRow),  'toRow':int(toRow), 
                         'totalRows':len(finalIndexes)}
                    res = {'columns':finalColumns[:CubepyEvaluator.MAX_COLUMS].tolist(), 
                     'index':finalIndexes[fromRow - 1:toRow].tolist(), 
                     'data':finalValues[fromRow - 1:toRow, :CubepyEvaluator.MAX_COLUMS].tolist()}
                    if _totalRow is not None:
                        res['index'].append('Total')
                        res['data'].append(_totalRow[:CubepyEvaluator.MAX_COLUMS].tolist())
                return self.createResult(res, result_structure, onRow=onRow, onColumn=onColumn, node=(nodeDic[nodeId]), pageInfo=pageInfo)

    def applyHierarchy(self, result, nodeDic, nodeId, dims, rows, columns, sby):

        def hierarchize(cube, levels, maps):
            mapArray = nodeDic[maps[0]].result
            coordValues = mapArray.values.copy()
            targetIndexId = nodeDic[levels[1]].result.name
            for pos, level in enumerate(levels):
                if pos > 0 and maps[pos] is not None:
                    mapArrayLevel = nodeDic[maps[pos]].result
                    for ii in range(len(coordValues)):
                        if coordValues[ii] is not None:
                            try:
                                newVal = mapArrayLevel.filter(mapArrayLevel.dims[0], coordValues[ii]).values.item(0)
                                coordValues[ii] = newVal
                            except Exception as ex:
                                try:
                                    coordValues[ii] = None
                                finally:
                                    ex = None
                                    del ex

            _coords = []
            for _axis in cube.axes:
                _coord = pd.Index((_axis.values), name=(_axis.name))
                _coords.append(_coord)

            dataArray = xr.DataArray(cube.values, _coords)
            dataArray.coords[levels[0]].values = coordValues
            _df = dataArray.to_series()
            _df = _df.groupby((list(dataArray.dims)), sort=False).agg(sby)
            _da = _df.to_xarray()
            reindex_dic = dict()
            for dimension in _da.dims:
                if dimension == levels[0]:
                    reindex_dic[dimension] = nodeDic[levels[-1:][0]].result.values

            _db = _da.reindex(reindex_dic)
            _indexes = []
            for _dim in _db.dims:
                _index = cubepy.Index(_dim, _db.coords[_dim].values)
                _indexes.append(_index)

            _cube = cubepy.Cube(_indexes, _db.values)
            return _cube

        allDims = (dims or []) + (rows or []) + (columns or [])
        for dim in allDims:
            if dim and dim['currentLevel'] and dim['currentLevel'] != str(dim['field']).split('.')[0]:

                def findPath(indexNode, level, levels, maps):
                    if indexNode.identifier == level:
                        levels.append(indexNode.identifier)
                        maps.append(None)
                        return True
                        parents = indexNode.hierarchy_parents
                        if parents is None:
                            return False
                    else:
                        if not isinstance(parents, list):
                            parents = [
                             parents]
                        mapArrays = indexNode.hierarchy_maps
                        mapArrays = isinstance(mapArrays, list) or [
                         mapArrays]
                    mapPos = 0
                    for parentId in parents:
                        parent = nodeDic[parentId]
                        if findPath(parent, level, levels, maps):
                            levels.append(indexNode.identifier)
                            maps.append(mapArrays[mapPos])
                            return True
                        mapPos += 1

                    return False

                field = str(dim['field']).split('.')[0]
                currentLevel = dim['currentLevel']
                indexNode = nodeDic[field]
                levels = []
                maps = []
                findPath(indexNode, currentLevel, levels, maps)
                levels.reverse()
                maps.reverse()
                result = hierarchize(cubepy.cube.Cube(result._axes, result._values), levels, maps)

        return result

    def indexEvaluate(self, result, nodeDic, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0):
        res = result.values[:100].tolist()
        return self.createResult(res, (self.getStructure(res)), node=(nodeDic[nodeId]))

    def addToFilter(self, nodeDic, dim, filters):
        if 'values' in dim:
            if dim['values'] is not None:
                if len(dim['values']) > 0:
                    field = str(dim['field'])
                    nodeId = None
                    indexType = None
                    if '.' in field:
                        if field.startswith('Axis'):
                            indexType = 'N'
                        else:
                            indexType = self.getIndexType(nodeDic, nodeId, field)
                    elif indexType == 'S':
                        filters.append(cubepy.Index(field, [str(v['value']) for v in dim['values']]))
                    else:
                        filters.append(cubepy.Index(field, [int(v['value']) for v in dim['values']]))

    def getCubeValues(self, result, nodeDic, nodeId, query):
        if isinstance(result, cubepy.Cube):
            res = {'dims':[],  'values':[]}
            _filters = []
            if query['filters'] is not None:
                for dimFilter in query['filters']:
                    field = str(dimFilter['field'])
                    if self.hasDim(result, field):
                        indexType = None
                        if '.' in field:
                            if field.startswith('Axis'):
                                indexType = 'N'
                            else:
                                indexType = self.getIndexType(nodeDic, nodeId, field)
                            if indexType == 'S':
                                _filters.append(cubepy.Index(field, [str(v) for v in dimFilter['values']]))
                        else:
                            _filters.append(cubepy.Index(field, [int(v) for v in dimFilter['values']]))

            else:
                _filteredResult = result.filter(_filters)
                for col in query['columns']:
                    if col in self.getIndexes(nodeDic[nodeId], result):
                        item = {'field':col,  'count':0, 
                         'values':[str(v) for v in _filteredResult.axis(col).values.tolist()]}
                        item['count'] = len(item['values'])
                        res['dims'].append(item)

                resultValues = _filteredResult.sum(keep=(query['columns']))
                if isinstance(resultValues, cubepy.Cube):
                    res['values'] = resultValues.transpose(query['columns']).values.reshape(resultValues.size).tolist()
                else:
                    if isinstance(resultValues, str):
                        res['values'] = [
                         resultValues]
                    else:
                        res['values'] = resultValues
            return res

    def getCubeDimensionValues(self, result, nodeDic, nodeId, query):
        if isinstance(result, cubepy.Cube):
            if len(query['columns']) > 0:
                dimension = query['columns'][(-1)]
            if dimension in self.getIndexes(nodeDic[nodeId], result):
                finalList = [str(v) for v in result.axis(dimension).values.tolist()[:1000]]
                finalList.sort()
                return finalList
        return []

    def getCubeMetadata(self, result, nodeDic, nodeId):
        res = None
        if isinstance(result, cubepy.Cube):
            res = {'dims':[],  'measures':[],  'aggregator':'sum', 
             'isEditable':True if self.isTable(nodeDic[nodeId]) == '1' else False, 
             'nodeProperties':{'title':nodeDic[nodeId].title if nodeDic[nodeId].title is not None else nodeDic[nodeId].identifier, 
              'numberFormat':nodeDic[nodeId].numberFormat}}
            if nodeDic[nodeId].model.isNodeInScenario(nodeDic[nodeId].identifier):
                res['nodeProperties']['scenario'] = True
            for dim in result.dims:
                itemDim = {'field':dim,  'name':str(dim).split('.')[0]}
                if dim in nodeDic:
                    if nodeDic[dim].title is not None:
                        itemDim['name'] = nodeDic[dim].title
                res['dims'].append(itemDim)

            res['measures'].append({'field':'datavalue', 
             'name':'datavalue'})
        return res

    def setNodeValueChanges(self, nodeDic, nodeId, nodeChanges):
        if isinstance(nodeDic[nodeId].result, cubepy.Cube):
            for change in nodeChanges['changes']:
                newValue = change['definition']
                filters = []
                for filterItem in change['filterList']:
                    aux = {'field':filterItem['Key'],  'values':[
                      {'value': filterItem['Value']}]}
                    self.addToFilter(nodeDic, aux, filters)

                nodeDic[nodeId].result.set_data(filters, newValue)
                newDeff = nodeDic[nodeId].result.generateDefinition()
                nodeDic[nodeId].definition = newDeff

            return 'ok'

    def isTable--- This code section failed: ---

 L. 431         0  LOAD_STR                 '0'
                2  STORE_FAST               'res'

 L. 432         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'node'
                8  LOAD_ATTR                result
               10  LOAD_GLOBAL              cubepy
               12  LOAD_ATTR                Cube
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE   182  'to 182'

 L. 433        18  LOAD_FAST                'node'
               20  LOAD_ATTR                definition
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE   180  'to 180'
               28  LOAD_FAST                'node'
               30  LOAD_ATTR                definition
               32  LOAD_STR                 ''
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE   180  'to 180'

 L. 434        38  LOAD_CONST               0
               40  LOAD_CONST               None
               42  IMPORT_NAME              re
               44  STORE_FAST               're'

 L. 435        46  LOAD_FAST                're'
               48  LOAD_METHOD              sub

 L. 436        50  LOAD_STR                 '[\\s+]'
               52  LOAD_STR                 ''
               54  LOAD_GLOBAL              str
               56  LOAD_FAST                'node'
               58  LOAD_ATTR                definition
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  LOAD_METHOD              strip
               64  LOAD_STR                 ' \t\n\r'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  CALL_METHOD_3         3  '3 positional arguments'
               70  LOAD_METHOD              lower
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  STORE_FAST               'deff'

 L. 437        76  LOAD_FAST                'deff'
               78  LOAD_METHOD              startswith
               80  LOAD_STR                 'this=cubepy.cube('
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_JUMP_IF_TRUE    176  'to 176'
               86  LOAD_FAST                'deff'
               88  LOAD_METHOD              startswith
               90  LOAD_STR                 'result=cubepy.cube('
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_JUMP_IF_TRUE    176  'to 176'

 L. 438        96  LOAD_FAST                'deff'
               98  LOAD_METHOD              startswith
              100  LOAD_STR                 'this=cp.cube('
              102  CALL_METHOD_1         1  '1 positional argument'
              104  POP_JUMP_IF_TRUE    176  'to 176'
              106  LOAD_FAST                'deff'
              108  LOAD_METHOD              startswith
              110  LOAD_STR                 'result=cp.cube('
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_JUMP_IF_TRUE    176  'to 176'

 L. 439       116  LOAD_FAST                'deff'
              118  LOAD_METHOD              startswith
              120  LOAD_STR                 'this=cubepy.cube.zeros('
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_JUMP_IF_TRUE    176  'to 176'
              126  LOAD_FAST                'deff'
              128  LOAD_METHOD              startswith
              130  LOAD_STR                 'result=cubepy.cube.zeros('
              132  CALL_METHOD_1         1  '1 positional argument'
              134  POP_JUMP_IF_TRUE    176  'to 176'

 L. 440       136  LOAD_FAST                'deff'
              138  LOAD_METHOD              startswith
              140  LOAD_STR                 'this=cubepy.cube.ones('
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_JUMP_IF_TRUE    176  'to 176'
              146  LOAD_FAST                'deff'
              148  LOAD_METHOD              startswith
              150  LOAD_STR                 'result=cubepy.cube.ones('
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_JUMP_IF_TRUE    176  'to 176'

 L. 441       156  LOAD_FAST                'deff'
              158  LOAD_METHOD              startswith
              160  LOAD_STR                 'this=cubepy.cube.full('
              162  CALL_METHOD_1         1  '1 positional argument'
              164  POP_JUMP_IF_TRUE    176  'to 176'
              166  LOAD_FAST                'deff'
              168  LOAD_METHOD              startswith
              170  LOAD_STR                 'result=cubepy.cube.full('
              172  CALL_METHOD_1         1  '1 positional argument'
              174  POP_JUMP_IF_FALSE   180  'to 180'
            176_0  COME_FROM           164  '164'
            176_1  COME_FROM           154  '154'
            176_2  COME_FROM           144  '144'
            176_3  COME_FROM           134  '134'
            176_4  COME_FROM           124  '124'
            176_5  COME_FROM           114  '114'
            176_6  COME_FROM           104  '104'
            176_7  COME_FROM            94  '94'
            176_8  COME_FROM            84  '84'

 L. 442       176  LOAD_STR                 '1'
              178  STORE_FAST               'res'
            180_0  COME_FROM           174  '174'
            180_1  COME_FROM            36  '36'
            180_2  COME_FROM            26  '26'
              180  JUMP_FORWARD        276  'to 276'
            182_0  COME_FROM            16  '16'

 L. 443       182  LOAD_GLOBAL              isinstance
              184  LOAD_FAST                'node'
              186  LOAD_ATTR                result
              188  LOAD_GLOBAL              np
              190  LOAD_ATTR                ndarray
              192  CALL_FUNCTION_2       2  '2 positional arguments'
          194_196  POP_JUMP_IF_FALSE   276  'to 276'

 L. 444       198  LOAD_FAST                'node'
              200  LOAD_ATTR                definition
              202  LOAD_CONST               None
              204  COMPARE_OP               is-not
          206_208  POP_JUMP_IF_FALSE   276  'to 276'
              210  LOAD_FAST                'node'
              212  LOAD_ATTR                definition
              214  LOAD_STR                 ''
              216  COMPARE_OP               !=
          218_220  POP_JUMP_IF_FALSE   276  'to 276'

 L. 445       222  LOAD_CONST               0
              224  LOAD_CONST               None
              226  IMPORT_NAME              re
              228  STORE_FAST               're'

 L. 446       230  LOAD_FAST                're'
              232  LOAD_METHOD              sub

 L. 447       234  LOAD_STR                 '[\\s+]'
              236  LOAD_STR                 ''
              238  LOAD_GLOBAL              str
              240  LOAD_FAST                'node'
              242  LOAD_ATTR                definition
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  LOAD_METHOD              strip
              248  LOAD_STR                 ' \t\n\r'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  CALL_METHOD_3         3  '3 positional arguments'
              254  LOAD_METHOD              lower
              256  CALL_METHOD_0         0  '0 positional arguments'
              258  STORE_FAST               'deff'

 L. 448       260  LOAD_FAST                'deff'
              262  LOAD_METHOD              startswith
              264  LOAD_STR                 'result=np.'
              266  CALL_METHOD_1         1  '1 positional argument'
          268_270  POP_JUMP_IF_FALSE   276  'to 276'

 L. 449       272  LOAD_STR                 '1'
              274  STORE_FAST               'res'
            276_0  COME_FROM           268  '268'
            276_1  COME_FROM           218  '218'
            276_2  COME_FROM           206  '206'
            276_3  COME_FROM           194  '194'
            276_4  COME_FROM           180  '180'

 L. 451       276  LOAD_FAST                'res'
              278  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 180_0

    def hasDim(self, result, dim):
        if dim in result.dims:
            return True
        return False

    def getIndexes(self, node, result=None):
        res = []
        if result is None:
            result = node._result
        if isinstance(result, cubepy.Cube):
            res = list(result.dims)
        return res

    def getIndexesWithLevels(self, node, result=None):
        res = []
        if result is None:
            result = node._result
        if isinstance(result, cubepy.Cube):
            if result is not None:
                _model = node.model
                for indexItem in result.dims:
                    itemDim = indexItem
                    item = {'field':itemDim,  'name':itemDim,  'description':'', 
                     'levels':[]}
                    if node.model.existNode(itemDim):
                        levelNode = node.model.getNode(itemDim)
                        if levelNode.title:
                            item['name'] = levelNode.title
                            item['description'] = levelNode.description
                        if levelNode.hierarchy_parents is not None:

                            def buildLevels(parents, levelList):
                                if not isinstance(parents, list):
                                    parents = [
                                     parents]
                                for parentIndexId in parents:
                                    parentIndexNode = _model.getNode(parentIndexId)
                                    if parentIndexNode is None:
                                        raise ValueError(f"Node {parentIndexId} not found")
                                    levelItem = {'field':parentIndexId, 
                                     'name':parentIndexNode.title or parentIndexId}
                                    levelList.append(levelItem)
                                    _dummy = parentIndexNode.result
                                    if parentIndexNode.hierarchy_parents is not None:
                                        buildLevels(parentIndexNode.hierarchy_parents, levelList)

                            listOfLevels = [{'field':itemDim,  'name':item['name']}]
                            indexParents = levelNode.hierarchy_parents
                            buildLevels(indexParents, listOfLevels)
                            item['levels'] = listOfLevels
                    res.append(item)

        return res

    def getIndexType(self, nodeDic, nodeId, indexId):
        numerics = [
         'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        res = 'S'
        if (indexId is not None) & (indexId in nodeDic):
            node = nodeDic[indexId]
            if isinstance(node.result, cubepy.Index):
                if str(node.result.values.dtype) in numerics:
                    res = 'N'
                else:
                    res = 'S'
            elif isinstance(node.result, np.ndarray):
                if str(node.result.dtype) in numerics:
                    res = 'N'
                else:
                    res = 'S'
            else:
                res = 'S'
        return res

    def getIndexValues(self, nodeDic, data: IndexValuesReq, result=None):
        res = []
        if (data.index_id is not None) & (data.index_id in nodeDic):
            node = nodeDic[data.index_id]
            if isinstance(node.result, cubepy.Index):
                res = node.result.values.tolist()
            else:
                if isinstance(node.result, np.ndarray):
                    res = node.result.tolist()
                else:
                    res = list(node.result)
        elif data.text1:
            text1 = data.text1.lower()
            if data.filter == filterChoices.CONTAINS.value:
                res = list(filter(lambda item: text1 in str(item).lower(), res))
            else:
                if data.filter == filterChoices.NOT_CONTAINS.value:
                    res = list(filter(lambda item: text1 not in str(item).lower(), res))
        return res

    def previewNode(self, nodeDic, nodeId):
        import pyplan_core.cubepy.Helpers as Helpers
        from sys import getsizeof
        res = {'resultType':str(type(nodeDic[nodeId].result)), 
         'dims':[],  'console':nodeDic[nodeId].lastEvaluationConsole, 
         'preview':''}
        if isinstance(nodeDic[nodeId].result, cubepy.Cube):
            cube = nodeDic[nodeId].result
            for _axis in cube.axes:
                _nodeTitle = None
                if _axis.name in nodeDic:
                    _nodeTitle = nodeDic[_axis.name].title
                elif _nodeTitle is None:
                    _item = _axis.name + ' [' + str(len(_axis)) + ']'
                else:
                    _item = _nodeTitle + ' (' + _axis.name + ') [' + str(len(_axis)) + ']'
                res['dims'].append(_item)

            res['preview'] += 'Dimensions: ' + str(cube.ndim)
            res['preview'] += '\nShape: ' + str(cube.shape)
            res['preview'] += '\nSize: ' + str(cube.size)
            res['preview'] += '\nMemory: ' + str(round(getsizeof(cube) / 1024 / 1024, 2)) + ' Mb'
            if cube.values is not None:
                res['preview'] += '\nData type: ' + str(cube.values.dtype) + ' (' + kindToString(cube.values.dtype.kind) + ')'
                res['preview'] += '\nValues: \n\n' + str(cube.values)[:1000]
        elif isinstance(nodeDic[nodeId].result, cubepy.Index):
            index = nodeDic[nodeId].result
            res['preview'] += 'Size: ' + str(len(index))
            res['preview'] += '\nMemory: ' + str(round(getsizeof(index) / 1024 / 1024, 2)) + ' Mb'
            if index.values is not None:
                res['preview'] += '\nData type: ' + str(index.values.dtype) + ' (' + kindToString(index.values.dtype.kind) + ')'
                res['preview'] += '\nValues: \n\t' + '\n\t'.join([''.join(str(row)) for row in index.values[:100]])
        return json.dumps(res)

    def dumpNodeToFile(self, nodeDic, nodeId, fileName):
        definition = nodeDic[nodeId].result.generateDefinition()
        with open(fileName, 'w') as (f):
            f.write(definition)
            f.close()

    def geoUnclusterData(self, result, nodeDic, nodeId, rowIndex, attIndex, latField='latitude', lngField='longitude', geoField='geoField', labelField='labelField', sizeField='sizeField', colorField='colorField', iconField='iconField'):
        latField = 'latitude' if latField is None else latField
        lngField = 'longitude' if lngField is None else lngField
        geoField = 'geoField' if geoField is None else geoField
        labelField = 'labelField' if labelField is None else labelField
        sizeField = 'sizeField' if sizeField is None else sizeField
        colorField = 'colorField' if colorField is None else colorField
        iconField = 'iconField' if iconField is None else iconField
        _tmp_for_geo = cubepy.Index('tmp_for_geo', [
         latField, lngField, geoField, labelField, sizeField, colorField, iconField])
        _idx = nodeDic[attIndex].result
        rowIndexObj = nodeDic[rowIndex].result
        mapCube = result[(_idx == _tmp_for_geo)].transpose([
         rowIndex, 'tmp_for_geo']).values
        res = dict()
        points = []
        pos = 0
        for itemRow in mapCube:
            vo = dict()
            vo['id'] = str(rowIndexObj.values[pos])
            vo['lat'] = itemRow[0]
            vo['lng'] = itemRow[1]
            vo['geoDef'] = itemRow[2]
            vo['labelRes'] = itemRow[3]
            vo['sizeRes'] = itemRow[4]
            vo['colorRes'] = itemRow[5]
            vo['iconRes'] = itemRow[6]
            points.append(vo)
            pos += 1

        res['points'] = points
        return res