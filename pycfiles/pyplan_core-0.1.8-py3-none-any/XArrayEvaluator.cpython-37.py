# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/evaluators/XArrayEvaluator.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 33576 bytes
import json, math, numpy as np, pandas as pd, xarray as xr
import pyplan_core.classes.evaluators.BaseEvaluator as BaseEvaluator
import pyplan_core.classes.evaluators.PandasEvaluator as PandasEvaluator
from pyplan_core.classes.XHelpers import XHelpers, XIndex
import pyplan_core.classes.common.filterChoices as filterChoices
from pyplan_core.classes.common.indexValuesReq import IndexValuesReq

class XArrayEvaluator(BaseEvaluator):
    PAGESIZE = 100
    MAX_COLUMS = 5000

    def evaluateNode(self, result, nodeDic, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0):
        if isinstance(result, xr.DataArray):
            return self.cubeEvaluate(result, nodeDic, nodeId, dims, rows, columns, summaryBy, bottomTotal, rightTotal, fromRow, toRow)

    def cubeEvaluate(self, result, nodeDic, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0):
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
        if fromRow is None or int(fromRow) <= 0:
            fromRow = 1
        if toRow is None or int(toRow) < 1:
            toRow = 100
        fromRow = int(fromRow)
        toRow = int(toRow)
        result = self.applyHierarchy(result, nodeDic, nodeId, dims, rows, columns, sby)
        _filters = {}
        _rows = []
        _columns = []
        if rows is not None:
            for row in rows:
                if self.hasDim(result, str(row['field'])):
                    _rows.append(str(row['field']).split('.')[0])
                    self.addToFilter(nodeDic, row, _filters)

        if columns is not None:
            for column in columns:
                if self.hasDim(result, str(column['field'])):
                    _columns.append(str(column['field']).split('.')[0])
                    self.addToFilter(nodeDic, column, _filters)

        if dims is not None:
            for dim in dims:
                if self.hasDim(result, str(dim['field']).split('.')[0]):
                    self.addToFilter(nodeDic, dim, _filters)

        tmp = None
        filteredResult = result
        if len(_filters) > 0:
            filteredResult = result.sel(_filters)
        if len(_rows) == 0 and len(_columns) == 0 and result.ndim > 0:
            try:
                tmp = sby(filteredResult)
            except Exception as ex:
                try:
                    if 'flexible type' in str(ex):
                        tmp = sby(filteredResult.astype('O'))
                    else:
                        raise ex
                finally:
                    ex = None
                    del ex

            tmp = isinstance(tmp, xr.DataArray) or xr.DataArray(tmp)
        else:
            otherDims = [xx for xx in filteredResult.dims if xx not in _rows + _columns]
            if len(otherDims) > 0:
                squeezable = [filteredResult.sizes[xx] == 1 for xx in otherDims]
                to_squeeze = list(np.array(otherDims)[squeezable])
                if len(to_squeeze) > 0:
                    filteredResult = filteredResult.squeeze(to_squeeze)
                    otherDims = [xx for xx in filteredResult.dims if xx not in _rows + _columns]
                elif len(otherDims) > 0:
                    try:
                        tmp = (filteredResult.reduce(sby, otherDims).transpose)(*_rows + _columns)
                    except Exception as ex:
                        try:
                            if 'flexible type' in str(ex):
                                tmp = (filteredResult.astype('O').reduce(sby, otherDims).transpose)(*_rows + _columns)
                        finally:
                            ex = None
                            del ex

                else:
                    tmp = (filteredResult.transpose)(*_rows + _columns)
            else:
                finalValues = tmp.values
                finalIndexes = []
                if tmp.ndim > 0:
                    finalIndexes = tmp.coords[tmp.dims[0]].values
                finalColumns = [
                 'Total']
                if tmp.ndim == 2:
                    finalColumns = tmp.coords[tmp.dims[1]].values
                _totalRow = None
                if bottomTotal:
                    if len(_rows) > 0:
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
            if self.kindToString(finalValues.dtype.kind) == 'numeric':
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
                res = {'columns':self.checkDateFormat(finalIndexes[:XArrayEvaluator.MAX_COLUMS]).tolist(), 
                 'index':finalColumns, 
                 'data':[
                  finalValues[:XArrayEvaluator.MAX_COLUMS].tolist()]}
            else:
                if len(_columns) == 0:
                    if len(finalIndexes) > self.PAGESIZE:
                        pageInfo = {'fromRow':int(fromRow),  'toRow':int(toRow), 
                         'totalRows':len(finalIndexes)}
                    onRow = _rows[0]
                    res = {'columns':finalColumns, 
                     'index':self.checkDateFormat(finalIndexes[fromRow - 1:toRow]).tolist(), 
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
                    res = {'columns':self.checkDateFormat(finalColumns[:XArrayEvaluator.MAX_COLUMS]).tolist(), 
                     'index':self.checkDateFormat(finalIndexes[fromRow - 1:toRow]).tolist(), 
                     'data':finalValues[fromRow - 1:toRow, :XArrayEvaluator.MAX_COLUMS].tolist()}
                    if _totalRow is not None:
                        res['index'].append('Total')
                        res['data'].append(_totalRow[:XArrayEvaluator.MAX_COLUMS].tolist())
                return self.createResult(res, result_structure, onRow=onRow, onColumn=onColumn, node=(nodeDic[nodeId]), pageInfo=pageInfo)

    def getStructure(self, result):
        structure = dict()
        structure['type'] = str(type(result))
        structure['dims'] = list(result.dims)
        return structure

    def checkStructure(self, result, resultType):
        """ Check current vs result structure. Result False for distinct structure """
        res = True
        if resultType:
            try:
                structure = json.loads(resultType)
                result_structure = self.getStructure(result)
                res = structure['type'] == result_structure['type'] and all((elem in list(result_structure['dims']) for elem in list(structure['dims'])))
            except Exception as ex:
                try:
                    print(f"Error checking structure: {ex}")
                finally:
                    ex = None
                    del ex

        return res

    def hasDim(self, result, dim):
        if dim.split('.')[0] in result.dims:
            return True
        return False

    def addToFilter(self, nodeDic, dim, filters):
        if 'values' in dim:
            if dim['values'] is not None:
                if len(dim['values']) > 0:
                    field = str(dim['field']).split('.')[0]
                    nodeId = None
                    indexType = None
                    indexType = self.getIndexType(nodeDic, nodeId, field)
                    _values = None
                    if indexType == 'S':
                        _values = [str(xx['value']) for xx in dim['values']]
                    else:
                        _values = [int(xx['value']) for xx in dim['values']]
                    all_values = None
                    npValues = np.array(_values)
                    if field in nodeDic:
                        all_values = nodeDic[field].result.values
                    else:
                        if len(dim['field'].split('.')) > 1:
                            node_id = str(dim['field']).split('.')[1]
                            if field in nodeDic[node_id].result.dims:
                                all_values = nodeDic[node_id].result.coords[field].values
                        else:
                            serie = pd.Series(all_values)
                            if all_values is not None and serie.isin(npValues).any():
                                npValues = all_values[serie.isin(npValues)]
                        if len(npValues) > 0:
                            filters[field] = npValues

    def getIndexes(self, node, result=None):
        if result is None:
            result = node._result
        return [xx + '.' + node.identifier for xx in result.dims]

    def getIndexesWithLevels(self, node, result=None):
        res = []
        if result is None:
            result = node._result
        if result is not None:
            _model = node.model
            for indexItem in result.dims:
                itemDim = indexItem.split(',')[0]
                item = {'field':itemDim + '.' + node.identifier,  'name':itemDim, 
                 'description':'',  'levels':[]}
                if _model.existNode(itemDim):
                    levelNode = _model.getNode(itemDim)
                    if levelNode.title:
                        item['name'] = levelNode.title
                        item['description'] = levelNode.description
                    if levelNode.numberFormat:
                        item['numberFormat'] = levelNode.numberFormat
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
                elif 'datetime' in result.coords[itemDim].dtype.name:
                    item['numberFormat'] = '2,DD,0,,0,0,4,0,$,5,FULL,0'
                res.append(item)

        return res

    def isIndexed(self, result):
        if result is not None:
            obj = result
            if isinstance(obj, pd.Series):
                obj = pd.DataFrame({'values': obj})
            if isinstance(obj, pd.DataFrame):
                if isinstance(obj.index, pd.MultiIndex) or isinstance(obj.index, pd.Index):
                    if len(obj.index.names) > 0:
                        if obj.index.names[0] is not None:
                            return True
        return False

    def getIndexValues(self, nodeDic, data: IndexValuesReq, result=None):
        res = []
        if data.node_id:
            if (data.node_id is not None) & (data.node_id in nodeDic):
                node = nodeDic[data.node_id]
                if result is None:
                    result = node.result
                res = self.checkDateFormat(result[data.index_id].values).tolist()
        elif (data.index_id is not None) & (data.index_id in nodeDic):
            node = nodeDic[data.index_id]
            if result is None:
                result = node.result
            elif isinstance(result, XIndex):
                res = result.values.tolist()
            else:
                if isinstance(result, np.ndarray):
                    res = self.checkDateFormat(result).tolist()
                else:
                    res = list(result)
        if data.text1:
            text1 = data.text1.lower()
            if data.filter == filterChoices.CONTAINS.value:
                res = list(filter(lambda item: text1 in str(item).lower(), res))
            else:
                if data.filter == filterChoices.NOT_CONTAINS.value:
                    res = list(filter(lambda item: text1 not in str(item).lower(), res))
        return res

    def getIndexType(self, nodeDic, nodeId, indexId):
        numerics = [
         'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        res = 'S'
        if (indexId is not None) & (indexId in nodeDic):
            node = nodeDic[indexId]
            if isinstance(node.result, XIndex) or isinstance(node.result, pd.Index):
                if str(node.result.values.dtype) in numerics:
                    res = 'N'
        elif isinstance(node.result, np.ndarray):
            if str(node.result.dtype) in numerics:
                res = 'N'
            elif nodeId:
                if (nodeId is not None) & (nodeId in nodeDic):
                    node = nodeDic[nodeId]
                    if str(node.result.coords[indexId].values.dtype) in numerics:
                        res = 'N'
        return res

    def getCubeValues(self, result, nodeDic, nodeId, query):
        if isinstance(result, xr.DataArray):
            res = {'dims':[],  'values':[]}
            query['columns'] = [xx.split('.')[0] for xx in query['columns']]
            _filters = {}
            if query['filters'] is not None:
                for dimFilter in query['filters']:
                    field = str(dimFilter['field']).split('.')[0]
                    if self.hasDim(result, field):
                        dimFilter['values'] = [{'value': xx} for xx in dimFilter['values']]
                        self.addToFilter(nodeDic, dimFilter, _filters)

            _filteredResult = result
            if len(_filters):
                _filteredResult = result.sel(_filters)
            else:
                nodeIndexes = self.getIndexes(nodeDic[nodeId], result)
                nodeIndexes = [xx.split('.')[0] for xx in nodeIndexes]
                for col in query['columns']:
                    if col in nodeIndexes:
                        item = {'field':col,  'count':0, 
                         'values':[str(v) for v in self.checkDateFormat(_filteredResult.coords[col].values).tolist()]}
                        item['count'] = len(item['values'])
                        res['dims'].append(item)

                otherDims = [xx for xx in _filteredResult.dims if xx not in query['columns']]
                if len(otherDims) > 0:
                    squeezable = [_filteredResult.sizes[xx] == 1 for xx in otherDims]
                    to_squeeze = list(np.array(otherDims)[squeezable])
                    if len(to_squeeze) > 0:
                        _filteredResult = _filteredResult.squeeze(to_squeeze)
                        otherDims = [xx for xx in _filteredResult.dims if xx not in query['columns']]
                    resultValues = None
                    if len(otherDims) > 0:
                        resultValues = _filteredResult.sum(otherDims)
                else:
                    resultValues = _filteredResult
            if isinstance(resultValues, xr.DataArray):
                if pd.isnull(resultValues).any():
                    new_values = None
                    try:
                        new_values = np.where(np.isnan(resultValues), None, resultValues)
                    except:
                        new_values = resultValues.values
                        new_values[pd.isnull(new_values)] = None

                    resultValues = resultValues.copy(data=new_values)
                elif len(query['columns']) > 0:
                    res['values'] = (resultValues.transpose)(*query['columns']).values.reshape(resultValues.size).tolist()
                else:
                    res['values'] = [
                     resultValues.values.tolist()]
            else:
                res['values'] = resultValues
            return res

    def getCubeDimensionValues(self, result, nodeDic, nodeId, query):
        if isinstance(result, xr.DataArray):
            if len(query['columns']) > 0:
                dimension = query['columns'][(-1)]
            if dimension + '.' + nodeId in self.getIndexes(nodeDic[nodeId], result):
                finalList = [str(v) for v in self.checkDateFormat(result.coords[dimension].values).tolist()[:1000]]
                finalList.sort()
                return finalList
        return []

    def getCubeMetadata(self, result, nodeDic, nodeId):
        res = None
        if isinstance(result, xr.DataArray):
            res = {'dims':[],  'measures':[],  'aggregator':'sum', 
             'isEditable':True if self.isTable(nodeDic[nodeId]) == '1' else False, 
             'nodeProperties':{'title':nodeDic[nodeId].title if nodeDic[nodeId].title is not None else nodeDic[nodeId].identifier, 
              'numberFormat':nodeDic[nodeId].numberFormat, 
              'resultType':json.dumps(self.getStructure(result))}}
            if nodeDic[nodeId].model.isNodeInScenario(nodeDic[nodeId].identifier):
                res['nodeProperties']['scenario'] = True
            for dim in result.dims:
                indexPart = str(dim).split('.')[0]
                itemDim = {'field':dim, 
                 'name':indexPart}
                if indexPart in nodeDic:
                    if nodeDic[indexPart].title is not None:
                        itemDim['name'] = nodeDic[indexPart].title
                    if nodeDic[indexPart].numberFormat:
                        itemDim['numberFormat'] = nodeDic[indexPart].numberFormat
                res['dims'].append(itemDim)

            res['measures'].append({'field':'datavalue', 
             'name':'datavalue'})
        return res

    def isTable--- This code section failed: ---

 L. 507         0  LOAD_STR                 '0'
                2  STORE_FAST               'res'

 L. 508         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'node'
                8  LOAD_ATTR                result
               10  LOAD_GLOBAL              xr
               12  LOAD_ATTR                DataArray
               14  CALL_FUNCTION_2       2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE   120  'to 120'

 L. 509        18  LOAD_FAST                'node'
               20  LOAD_ATTR                definition
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE   120  'to 120'
               28  LOAD_FAST                'node'
               30  LOAD_ATTR                definition
               32  LOAD_STR                 ''
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE   120  'to 120'

 L. 510        38  LOAD_CONST               0
               40  LOAD_CONST               None
               42  IMPORT_NAME              re
               44  STORE_FAST               're'

 L. 511        46  LOAD_FAST                're'
               48  LOAD_METHOD              sub

 L. 512        50  LOAD_STR                 '[\\s+]'
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

 L. 513        76  LOAD_FAST                'deff'
               78  LOAD_METHOD              startswith
               80  LOAD_STR                 'result=pp.dataarray('
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_JUMP_IF_TRUE    116  'to 116'
               86  LOAD_FAST                'deff'
               88  LOAD_METHOD              startswith
               90  LOAD_STR                 'result=pp.cube('
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_JUMP_IF_TRUE    116  'to 116'
               96  LOAD_FAST                'deff'
               98  LOAD_METHOD              startswith
              100  LOAD_STR                 'result=xr.dataarray('
              102  CALL_METHOD_1         1  '1 positional argument'
              104  POP_JUMP_IF_TRUE    116  'to 116'
              106  LOAD_FAST                'deff'
              108  LOAD_METHOD              startswith
              110  LOAD_STR                 'result=create_dataarray('
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_JUMP_IF_FALSE   120  'to 120'
            116_0  COME_FROM           104  '104'
            116_1  COME_FROM            94  '94'
            116_2  COME_FROM            84  '84'

 L. 514       116  LOAD_STR                 '1'
              118  STORE_FAST               'res'
            120_0  COME_FROM           114  '114'
            120_1  COME_FROM            36  '36'
            120_2  COME_FROM            26  '26'
            120_3  COME_FROM            16  '16'

 L. 516       120  LOAD_FAST                'res'
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 120_0

    def setNodeValueChanges(self, nodeDic, nodeId, nodeChanges):
        if isinstance(nodeDic[nodeId].result, xr.DataArray):
            for change in nodeChanges['changes']:
                newValue = change['definition']
                filters = {}
                for filterItem in change['filterList']:
                    aux = {'field':filterItem['Key'],  'values':[
                      {'value': filterItem['Value']}]}
                    self.addToFilter(nodeDic, aux, filters)

                for key in filters:
                    filters[key] = slice(filters[key][0], filters[key][0])

                nodeDic[nodeId].result.loc[filters] = newValue

            nodeDic[nodeId].definition = self.generateNodeDefinition(nodeDic, nodeId)
            return 'ok'

    def generateNodeDefinition(self, nodeDic, nodeId, forceXArray=False):
        array = nodeDic[nodeId].result
        np.set_printoptions(threshold=(np.prod(array.values.shape)))
        data = np.array2string((array.values), separator=',', precision=20, formatter={'float_kind': lambda x:                        if np.isnan(x):
'np.nan' # Avoid dead code: repr(x)}).replace('\n', '')
        indexes = []
        for dim in list(array.dims):
            if dim in nodeDic:
                indexes.append(dim)
            else:
                index_values = np.array2string((array[dim].values), separator=',', precision=20, formatter={'float_kind': lambda x:                                if np.isnan(x):
'np.nan' # Avoid dead code: repr(x)}).replace('\n', '')
                coord = f"pd.Index({index_values},name='{dim}')"
                indexes.append(coord)

        indexes = '[' + ','.join(indexes).replace("'", '"') + ']'
        if not forceXArray:
            if 'xr.DataArray' in nodeDic[nodeId].definition or 'create_dataarray' in nodeDic[nodeId].definition:
                if self.kindToString(array.values.dtype.kind) == 'string' or self.kindToString(array.values.dtype.kind) == 'object':
                    deff = f'result = xr.DataArray({data},{indexes}).astype("O")'
                else:
                    deff = f"result = xr.DataArray({data},{indexes})"
        elif self.kindToString(array.values.dtype.kind) == 'string' or self.kindToString(array.values.dtype.kind) == 'object':
            deff = 'result = pp.cube(' + indexes + ',' + data + ", dtype='O')"
        else:
            deff = 'result = pp.cube(' + indexes + ',' + data + ')'
        return deff

    def dumpNodeToFile(self, nodeDic, nodeId, fileName):
        definition = self.generateNodeDefinition(nodeDic, nodeId)
        with open(fileName, 'w') as (f):
            f.write(definition)
            f.close()

    def applyHierarchy(self, result, nodeDic, nodeId, dims, rows, columns, sby):

        def hierarchize(dataArray, levels, maps, hierarchyDic):
            mapArray = nodeDic[maps[0]].result
            coordValues = mapArray.values.copy()
            targetIndexId = nodeDic[levels[1]].result.name
            for pos, level in enumerate(levels):
                if pos > 0 and maps[pos] is not None:
                    mapArrayLevel = nodeDic[maps[pos]].result
                    for ii in range(len(coordValues)):
                        if coordValues[ii] is not None:
                            try:
                                newVal = mapArrayLevel.sel({mapArrayLevel.dims[0]: coordValues[ii]},
                                  drop=True).values.item(0)
                                coordValues[ii] = newVal
                            except Exception as ex:
                                try:
                                    coordValues[ii] = None
                                finally:
                                    ex = None
                                    del ex

            dataArray.coords[levels[0]].values = coordValues
            _df = dataArray.to_series()
            _df = _df.groupby((list(dataArray.dims)), sort=False).agg(sby)
            _da = _df.to_xarray()
            reindex_dic = dict()
            for dimension in _da.dims:
                if dimension == levels[0]:
                    reindex_dic[dimension] = nodeDic[levels[-1:][0]].result.values

            _db = _da.reindex(reindex_dic)
            return _db

        allDims = (dims or []) + (rows or []) + (columns or [])
        hierarchyDic = dict()
        for dim in allDims:
            if dim and dim['currentLevel'] and dim['currentLevel'] != str(dim['field']).split('.')[0]:
                hierarchyDic[str(dim['field']).split('.')[0]] = dim['currentLevel']

                def findPath(indexNode, level, levels, maps):
                    if indexNode.identifier == level:
                        levels.append(indexNode.identifier)
                        maps.append(None)
                        return True
                        _for_calc = indexNode.result
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
                result = hierarchize(result.copy(), levels, maps, hierarchyDic)

        return result

    def geoUnclusterData(self, result, nodeDic, nodeId, rowIndex, attIndex, latField='latitude', lngField='longitude', geoField='geoField', labelField='labelField', sizeField='sizeField', colorField='colorField', iconField='iconField'):
        _tmp_for_geo = XIndex('tmp_for_geo', [
         latField, lngField, geoField, labelField, sizeField, colorField, iconField])
        attIndex = attIndex.split('.')[0]
        rowIndex = rowIndex.split('.')[0]
        _idx = nodeDic[attIndex].result
        rowIndexObj = nodeDic[rowIndex].result
        mapCube = (XHelpers.changeIndex(None, result, _idx, _tmp_for_geo).transpose)(*[
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
        for nn, point in enumerate(res['points']):
            if nn == 0:
                try:
                    if not math.isnan(float(point['sizeRes'])):
                        res['minSize'] = float(point['sizeRes'])
                        res['maxSize'] = float(point['sizeRes'])
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

                try:
                    if not math.isnan(float(point['colorRes'])):
                        res['minColor'] = float(point['colorRes'])
                        res['maxColor'] = float(point['colorRes'])
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

                try:
                    if not math.isnan(float(point['iconRes'])):
                        res['minIcon'] = float(point['iconRes'])
                        res['maxIcon'] = float(point['iconRes'])
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

            else:
                try:
                    if not math.isnan(float(point['sizeRes'])):
                        if point['sizeRes'] > res['maxSize']:
                            res['maxSize'] = point['sizeRes']
                        if point['sizeRes'] < res['minSize']:
                            res['minSize'] = point['sizeRes']
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

                try:
                    if not math.isnan(float(point['colorRes'])):
                        if point['colorRes'] > res['maxColor']:
                            res['maxColor'] = point['colorRes']
                        if point['colorRes'] < res['minColor']:
                            res['minColor'] = point['colorRes']
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

                try:
                    if not math.isnan(float(point['iconRes'])):
                        if point['iconRes'] > res['maxIcon']:
                            res['maxIcon'] = point['iconRes']
                        if point['iconRes'] < res['minIcon']:
                            res['minIcon'] = point['iconRes']
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

        return res

    def postCalculate(self, node, result):
        """Method executed after calculate node
        """
        if isinstance(result, xr.DataArray):
            result.name = node.title

    def copyAsValues(self, result, nodeDic, nodeId):
        """ Copy node as values """
        newDef = ''
        if isinstance(result, float) or isinstance(result, int):
            newDef = 'result = ' + str(result)
        else:
            if isinstance(result, xr.DataArray):
                newDef = self.generateNodeDefinition(nodeDic, nodeId, True)
            else:
                return False
        nodeDic[nodeId].definition = newDef
        return True

    def previewNode(self, nodeDic, nodeId):
        if nodeDic[nodeId].result is not None:
            _result = nodeDic[nodeId].result
            res = {'resultType':str(type(_result)), 
             'dims':[],  'console':nodeDic[nodeId].lastEvaluationConsole, 
             'preview':''}
            _preview = ''
            _preview = f"{type(_result)} - dtype: {_result.dtype}"
            _preview += f"\n\n{_result.coords}"
            _preview += f"\n\nTotal cells: {_result.sizes} = {_result.size} cells"
            _preview += f"\n\nSample data: \n {_result.data}"
            res['preview'] = _preview
            return json.dumps(res)
        return self.generateEmptyPreviewResponse(nodeDic, nodeId)

    def kindToString(self, kind):
        """Returns the data type on human-readable string
        """
        if kind in {'U', 'S'}:
            return 'string'
        if kind in {'b'}:
            return 'boolean'
        if kind in {'i', 'f', 'c', 'u'}:
            return 'numeric'
        if kind in {'m', 'M'}:
            return 'date'
        if kind in {'O'}:
            return 'object'
        if kind in {'V'}:
            return 'void'