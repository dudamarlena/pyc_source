# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/cubepy/factory.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 32935 bytes
import numpy as np
import pyplan_core.cubepy as cubepy
import numbers
from sys import platform
from pyplan_core.cubepy.cube import kindToString, apply_op
import os, csv
random = -123798
byVal = 1
byPos = 2
exact = 1
start_with = 2
end_with = 3
contain = 4

def cube(axes, values=None, broadcast=True, dtype=None):
    """Create a cube  object. 
    axes: list of axis of the cube
    values: optional, list of values of the cube. Can be other cubes for build a report.
    Ex.
        cp.cube([time])
        cp.cube([time,product])
        cp.cube([time,product],[10,20,30,40,50,60,70,80])
        cp.cube([time,product],cp.random)
        
        cp.cube([index_reports],[report_1,report_2])
    """
    if values is None:
        if dtype is not None:
            if dtype is str:
                return cubepy.Cube.full(axes, '', dtype='U25')
            if kindToString(np.dtype(dtype).kind) == 'string':
                return cubepy.Cube.full(axes, '', dtype=dtype)
    else:
        return cubepy.Cube.zeros(axes)
        if isinstance(values, list) or isinstance(values, np.ndarray):
            if len(values) > 0:
                if isinstance(values[0], cubepy.Cube):
                    if isinstance(axes, list):
                        axes = axes[0]
                    return cubepy.stack(values, axes, broadcast)
            return cubepy.Cube(axes, values, fillValues=True, dtype=dtype)
        if isinstance(values, numbers.Number) and values == random:
            theSize = [len(x) for x in axes]
            return cube(axes, np.random.randint(100, size=theSize), dtype=dtype)
    return cubepy.Cube.full(axes, values, dtype=dtype)


def index(name, values):
    """Create a index object.
    name: name for the index
    values: list of values of the index.
    Ex.
        cp.index("items",["Item 1","Item 2","Item 3"])
        cp.index("years",[2016,2017,2018])
    """
    if values is None:
        values = [
         'Item 1', 'Item 2', 'Item 3']
    return cubepy.Index(name, values)


def find(param1, param2, compareType=1, caseSensitive=True):
    """
    param1: value or indexarray for compare
    param2: index compare to
    compareType: cp.exact=1, cp.start_with=2, cp.end_with=3, cp.contain=4  
    caseSensitive: able to differentiate between uppercase and lowercase (by default True)

    If param1 is a scalar (numeric or str) and param2 is an index:  return cube indexed by param2 with True on ocurrences of param2
        Ex. result = cp.apply("te", region, cp.end_with)
    If param1 is an index and param2 is an index too:  return cube indexed by param1 and param2 with True on ocurrences of param1 on param2
        Ex. result = cp.apply(subregion, region, cp.contain)

    """

    def _fn(item, value):
        if isinstance(item, str) == False:
            item = str(item)
        elif isinstance(value, str) == False:
            value = str(value)
        else:
            if compareType == 1:
                if caseSensitive:
                    return item == value
                    return item.lower() == value.lower()
                else:
                    pass
            if compareType == 2:
                if caseSensitive:
                    return item[:len(value)] == value
                return item[:len(value)].lower() == value.lower()
            else:
                if compareType == 3:
                    if caseSensitive:
                        return item[-len(value):] == value
                    return item[-len(value):].lower() == value.lower()
                else:
                    if compareType == 4:
                        if caseSensitive:
                            return value in item
                        return value.lower() in item.lower()

    if isinstance(param1, str) or str(param1).isnumeric():
        if isinstance(param2, cubepy.Index):
            vfn = np.vectorize(_fn)
            return cubepy.Cube([param2], vfn(param2.values, param1))
    if isinstance(param1, cubepy.Index):
        if isinstance(param2, cubepy.Index):
            _res = cubepy.Cube.full([param1, param2], False)
            rr = 0
            for row in param1.values:
                cc = 0
                for col in param2.values:
                    _res.values[(rr, cc)] = _fn(col, row)
                    cc += 1

                rr += 1

            return _res


def selectText(data, first=None, last=None):
    """Returns a new cube with the text contained between the 'first' and 'last' characters of cube / index 'data'. Starts counting from 0.
            If 'first' character is ommited, it returns every character from the first character of 'data' to the 'last' character, inclusive.
            If 'last' character is ommited, it returns every character from "first" character of 'data', to the last character available for each cell.
    """
    if first is None:
        if last is None:
            sliced_data = apply(lambda x: x[:], data)
        else:
            sliced_data = apply(lambda x: x[:last], data)
    elif last is None:
        sliced_data = apply(lambda x: x[first:], data)
    else:
        sliced_data = apply(lambda x: x[first:last], data)
    return sliced_data


def apply(fn, param1, param2=None, start=None):
    """
    Apply functions to index and cubes. Multiple results can be obtained
    fn: function to apply
    param1: index or cube
    param2: index or cube
    start: scalar or cube
        Ex. 
            cp.apply(lambda x: x[:2] ,indexRegion): return new cube indexed by "indexRegion" and apply fn on each item
            cp.apply(lambda x: x*5 ,cubeSales): return new cube result of apply fn on all values of the cubeSales
            cp.apply( cp.addPeriods, start_proj , end_proj): Return new cube result of apply fn on "start_proj" with "end_proj"
            cp.apply(lambda x: x+1, indexYear, start=10) : Return new cube indexed by "indexYear", result of apply fn starting with scalar value "10"
            cp.apply(lambda x: x+1, indexYear, start=prices) : Return new cube indexed by "indexYear", result of apply fn starting with cube "prices"
    """
    if callable(fn):
        vfn = np.vectorize(fn)
        if param2 is None:
            if isinstance(param1, cubepy.Index):
                if start is None:
                    return cubepy.Cube([param1], vfn(param1.values))
                if isinstance(start, cubepy.Cube):
                    values = [
                     start.values]
                    numEls = len(param1)
                    for nn in range(numEls - 1):
                        values.append(fn(values[nn]))

                    new_axes = start._axes.insert(param1, 0)
                    return cubepy.Cube(new_axes, values)
                values = [start]
                numEls = len(param1)
                for nn in range(numEls - 1):
                    values.append(fn(values[nn]))

                return cubepy.Cube(param1, values)
            if isinstance(param1, cubepy.Cube):
                return param1.apply(fn)
        elif isinstance(param1, cubepy.Cube):
            if isinstance(param2, cubepy.Cube):
                return apply_op(param1, param2, vfn)


def max(cube1, cube2):
    """Return max value between two cubes
    """
    return (cube1 > cube2) * cube1 + (cube1 <= cube2) * cube2


def min(cube1, cube2):
    """Return min value between two cubes
    """
    return (cube1 > cube2) * cube2 + (cube1 <= cube2) * cube1


def sum(cube, axis=None, keep=None, group=None, sort_grp=True):
    """Sum of array elements over a given axis.
    :param axis: Axis or axes along which a sum is performed. The default (axis = None) is perform a sum
    over all the dimensions of the input array. axis may be negative, in which case it counts from the last
    to the first axis. If this is a tuple of ints, a sum is performed on multiple axes, instead of a single
    axis or all the axes as before.
    :return: new Cube instance or a scalar value
    """
    return cube.reduce(np.sum, axis, keep, group, sort_grp)


def subscript(cube, index, value):
    """Filter cube1 using the index and the value. Return a new cube without the index1 dimension
        Ex.
            cp.subscript(nodo_ejemplo,index_para_ejemplo,"Item 1")
    """
    return cube[(index == value)]


def slice(cube, index, value):
    """Filter cube using the index and the value. Return a new cube without the index dimension
        Ex.
            cp.slice(nodo_ejemplo,index_para_ejemplo,2)
    """
    if isinstance(index, cubepy.Index):
        index = index.name
    if isinstance(value, str) or str(value).isnumeric():
        value = [
         value]
    return cube.take(index, value).squeeze()


def shift(cube, axis, n=1, cval=0):
    """Returns a cube with the axis shifted.
        Ex.
            cp.shift(nodo_ejemplo,index_para_ejemplo,1)
    """
    return cube.shift(axis, n, cval)


def subset(cube, indexName='new index'):
    """Returns a list of all the elements of the index for which cube is true. The function is used to create a new index that is a subset of an existing index.
        Ex. cp.subset(cantidades>0)
    """
    cond = cube > 0
    values = cond.axes[0].values[cond.values]
    return index(indexName, values)


def aggregate(cube, mapCube, indexToRemove, targetIndex):
    """ Aggregates the values in Cube to generate the result indexed by  targetIndex.
        Map gives the value of targetIndex for each element of indexToRemove

        Example for aggregating time information into annual index the syntax is:
            cp.aggregate(cube, map, time, years )
    """
    grouping_index_mat = cubepy.Cube([targetIndex], targetIndex.values)
    mat_allocation = mapCube == grouping_index_mat
    return (cube * mat_allocation).sum(indexToRemove)


def cumulate(cube, index):
    """ TODO coment
    """
    pos = 0
    tmpMat = cubepy.Cube.zeros(cube.axes)
    tmpInd = cubepy.Cube.zeros([index])
    for j in index.values:
        tmpInd.values[pos:pos + 1] = 1
        tmpMat = tmpMat + (tmpInd * cube).sum(index) * (j == index)
        pos = pos + 1

    return tmpMat


def cumProd(cube, index):
    """Return the cumulative product of elements along a given axis
        param cube: cube 
        param axis: axis name (str), index (int) or instance
        Ex:
            cp.cumProd(nodo,indice)
    """
    return cube.cumProd(index)


def irr(flow, time_index):
    """Returns the Internal Rate of Return (IRR) of a series of periodic payments (negative values) and inflows (positive values). The IRR is the discount rate at which the Net Present Value (NPV) of the flows equals zero. 
        The variable flow must be indexed by time_index.

    If the cash flow never changes sign, cp.irr() has no solution and returns NAN (Not A Number).
    """
    import pandas as pd
    _cube_dimensions = index('flowdims', flow.dims)
    _rest_of_indexes_labels = subset(_cube_dimensions != time_index.name).values
    _rest_of_indexes = [flow.axis(xx) for xx in _rest_of_indexes_labels]
    _cube = None
    if len(_rest_of_indexes) == 0:
        _cube = np.irr(flow.values)
    else:
        _cube = cube(_rest_of_indexes)
        _multivalues = [idx.values for idx in _rest_of_indexes]
        _values = pd.MultiIndex.from_product(_multivalues).values
        for _item in _values:
            _filter = []
            for _nn in range(len(_item)):
                _filter.append(_rest_of_indexes[_nn].filter([_item[_nn]]))

            _irr = np.irr(flow.filter(_filter).squeeze().values)
            _cube.set_data(_filter, _irr)

    return _cube


def npv(rate, flow, time_index, offset=1):
    """"Returns the Net Present Value (NPV) of a cash flow with equally spaced periods. The flow parameter must contain a series of periodic payments (negative values) and inflows (positive values), indexed by time_index.
        The optional offset parameter especifies the offset of the first value relative to the current time period. By default, offset is set to 1, indicating that the first value is discounted as if it is one step in the future
    """
    _number_of_periods = time_index.pos + offset
    _present_values = flow / (1 + rate) ** _number_of_periods
    _npv = _present_values.sum(axis=time_index)
    return _npv


def splitText(text, separator=',', resultIndex=None, indexName='new index'):
    """Split text into a list of substrings by each occurrence of separator.
        text:  string or cp.index used for split
        separator: string for use as separator
        resultIndex: optional, for return cp.cube indexes by this index
        indexName: optional, string name for new index
        Ex:
            cp.splitText("Uno Dos Tres Cuatro Cinco Seis", separator=" ") 
            cp.splitText(indice_para_split, separator="-") 
            cp.splitText("Uno Dos Tres Cuatro Cinco Seis"," ",result_index)  
            cp.splitText(indice_para_split, "-", result_index)  

    """
    if isinstance(text, str):
        _arr = text.split(separator)
        if resultIndex is None:
            return self.index(indexName, _arr)
        return self.cube(resultIndex, _arr)
    else:
        if isinstance(text, cubepy.Index):
            _arr = []
            for item in text.values:
                _tmpArr = str(item).split(separator)
                if resultIndex is not None:
                    _tmpNpArray = np.array(_tmpArr)
                    _tmpArr = []
                    for _nn in range(len(resultIndex)):
                        if _nn < len(_tmpNpArray):
                            _tmpArr.append(_tmpNpArray[_nn])
                        else:
                            _tmpArr.append('')

                _arr = _arr + _tmpArr

            _arrnp = np.array(_arr).flatten()
            if resultIndex is None:
                return index(indexName, _arrnp)
            return cube([text, resultIndex], _arrnp)


def changeIndex(cube, oldIndex, newIndex, compareMode=1, default=None):
    """Returns a new Cube instance with the axes changed,looking newIndex on oldIndex by value o by position.
        param Comparemode: cp.byVal or cp.byPos
        Ex:
            cp.changeIndex(nodo_original,indice_original,indice_cambiado,cp.byVal)
            cp.changeIndex(nodo_original,indice_original,indice_cambiado,cp.byPos)
    """
    return cube.change_axis(oldIndex, newIndex, compareMode, default=default)


def copyIndex(cube, indexName='new index'):
    """Generate a cp.index with current unique values of the cube. 
    The cube must have only one dimension
    """
    import pandas as pd
    if cube.ndim > 1:
        raise ValueError('The cube must have only one dimension')
    np_values = cube.values.flatten()
    seripandas = pd.Series(np_values)
    return index(indexName, seripandas.unique())


def cascadeVolume(demand, ranges, consumption_range_index=None):
    """TODO Comment
    Ex:
            cp.cascadeVolume(cantidades,limites_rango_consum)
            cp.cascadeVolume(cantidades,limites_rango_consum,"rangos_consumo")
            cp.cascadeVolume(cantidades,limites_rango_consum,rangos_consumo)
    """
    if consumption_range_index is None:
        if ranges.ndim == 1:
            consumption_range_index = ranges.dims[0]
        else:
            raise ValueError('You must specify the consumption_range_index')
    elif isinstance(consumption_range_index, cubepy.Index):
        consumption_range_index = consumption_range_index.name
    vol_entre_lim = ranges - ranges.shift(consumption_range_index, -1, 0)
    ConsumoBajoLimite = (ranges < demand) * vol_entre_lim
    ConsEnRangos = (demand > ranges) * 1
    ultrango = ConsEnRangos - ConsEnRangos.shift(consumption_range_index, -1, 1) == -1
    ConsumoLimite = (demand - ConsumoBajoLimite.sum(consumption_range_index)) * ultrango
    return ConsumoBajoLimite + ConsumoLimite


def bandAllocation(demand, ranges, consumption_range_index=None):
    """TODO Comment
        Ex:
            cp.bandAllocation(cantidades,limites_rango_consum)
            cp.bandAllocation(cantidades,limites_rango_consum,"rangos_consumo")
            cp.bandAllocation(cantidades,limites_rango_consum,rangos_consumo)
    """
    if consumption_range_index is None:
        if ranges.ndim == 1:
            consumption_range_index = ranges.dims[0]
        else:
            raise ValueError('You must specify the consumption_range_index')
    elif isinstance(consumption_range_index, cubepy.Index):
        consumption_range_index = consumption_range_index.name
    ConsEnRangos = (demand > ranges) * 1
    ultrango = ConsEnRangos - ConsEnRangos.shift(consumption_range_index, -1, 1) == -1
    ConsumoLimite = demand * ultrango
    return ConsumoLimite


def dispatch(contract_vol, contract_price, contract_index, demand):
    """TODO comment
        Ex:
            cp.dispatch(contract_volumes,prices,contracts,demand)
    """
    order_index = index('order', range(len(contract_index)))
    contract_order = argsort(contract_price, contract_index)
    vol_by_dispatch_order = (contract_order == order_index) * contract_vol
    cum_vol = cumulate(vol_by_dispatch_order, order_index).sum(contract_index)
    return (cascadeVolume(demand, cum_vol, order_index) * (contract_order == order_index)).sum(order_index)


def argsort(cube, axis):
    """Return new cube with the position of values sorted by axis
        ex.
            cp.argsort(nodo_1,index_a)
    """
    return cube.argsort(axis)


def iif(condition, truePart, falsePart=None):
    """Inline if. Evaluate condition and return truePart or fasePart
        ex. 
            cp.iif( producto=="Producto A", cantidades*1000 , cantidades)
            cp.iif( cantidades > 10, cantidades , 0)
    """
    if isinstance(condition, cubepy.Cube):
        _true = condition * truePart
        if falsePart is None:
            return _true
        _false = ~condition * falsePart
        return _true + _false
    else:
        if isinstance(condition, bool):
            if condition:
                return truePart
            return falsePart


def cubeFromPandas(dataframe, cubeIndexes, valueColumns, indexColumnHeaders=None, replaceByIndex=None):
    """Create new cp.cube, converting pandas to multidimensional data, according to the parameters
        dataframe: pandas dataframe
        cubeIndexes: objects cp.index for perform change index
        valueColumns: string with column name of the dataframe where contain the values
                        cp.index with columns names for convert colums to index
        indexColumnHeaders: (optional) column names in pandas to parse with cubeIndexes. Used if header on dataframe is not equal to index identifiers.
        replaceByIndex: (optional) replace index used in valueColumns for this index. (using changeindex)
    """
    import pandas as pd
    valueIndex = None
    if isinstance(valueColumns, cubepy.Index):
        valueIndex = valueColumns
        valueColumns = valueIndex.values
    else:
        if isinstance(valueColumns, str):
            valueColumns = np.array([valueColumns])
    if indexColumnHeaders is None:
        indexColumnHeaders = [index.name for index in cubeIndexes]
    _allindexes = cubeIndexes
    _allIndexNames = indexColumnHeaders[:]
    if valueIndex is not None:
        _allindexes.append(valueIndex)
        _allIndexNames.append('data_index')
    if isinstance(dataframe, pd.DataFrame):
        cols_not_in_df = [col for col in valueColumns if col not in dataframe.columns]
        for col in cols_not_in_df:
            dataframe[col] = np.nan

    _full = dataframe.reset_index().melt(id_vars=indexColumnHeaders, value_vars=valueColumns, var_name='data_index', value_name='data_value')
    if _full.size == 0:
        _cube = cube(_allindexes, np.array([], dtype='O'))
    else:
        _full = _full.groupby(_allIndexNames, as_index=False).sum()
        _dtype = _full['data_value'].dtype
        _dataType = kindToString(_dtype.kind)
        if _dataType == 'string':
            _full = _full[((_full['data_value'] != '') & _full['data_value'].notna())]
        else:
            _full = _full[((_full['data_value'] != 0) & _full['data_value'].notna())]
        _size = [len(x) for x in _allindexes]
        _emptyData = np.zeros(_size, dtype=_dtype)
        _cube = cube(_allindexes, _emptyData, _dtype)
        _valuePos = len(_full.columns)
        for _row in _full.itertuples():
            _arr = []
            _isOK = True
            _value = _row[_valuePos]
            for nn in range(1, len(_allIndexNames) + 1):
                _indexValue = _row[nn]
                if _indexValue in _allindexes[(nn - 1)]._indices:
                    _pos = _allindexes[(nn - 1)]._indices[_indexValue]
                    _arr.append(_pos)
                else:
                    _isOK = False
                    break

            if _isOK:
                _cube._values[tuple(_arr)] = _value

        if valueIndex is not None:
            if replaceByIndex is not None:
                _cube = changeIndex(_cube, valueIndex, replaceByIndex, 2)
        return _cube


def indexFromPandas(dataframe, columnName=None, removeEmpty=True, indexName='new index'):
    """ Return a cp.index from an column of a pandas dataframe.
    dataframe: pandas dataframe
    columnName: dataframe column name used for create cp.index. By default is created using the first column
    removeEmpty: True for remove empty rows
        Ex.
            cp.indexFromPandas(df)
            cp.indexFromPandas(df,"column10")
    """
    _serie = None
    if columnName is None:
        _serie = dataframe[dataframe.columns[0]]
    else:
        _serie = dataframe[columnName]
    if removeEmpty:
        _serie.dropna(inplace=True)
        if kindToString(_serie.dtype.kind) == 'string' or kindToString(_serie.dtype.kind) == 'object':
            _serie = _serie[(_serie != '')]
    return index(indexName, _serie.unique())


def pandasFromCube(cube, dataColumnName='value', keepIndexOrder=False):
    """
    Return indexed Dataframe created from cubePy Cube
    """
    import pandas as pd
    multiIndexValues = [idx.values for idx in cube.axes]
    allIndexNames = [idx.name for idx in cube.axes]
    multiindex = pd.MultiIndex.from_product(multiIndexValues, names=allIndexNames)
    serie = pd.Series(data=(cube.values.flatten()), index=multiindex)
    df = pd.DataFrame(serie)
    if keepIndexOrder:
        df = df.reset_index()
        for cubeIndex in cube.axes:
            df[cubeIndex.name] = df[cubeIndex.name].astype(pd.api.types.CategoricalDtype(cubeIndex.values))

        df.set_index(allIndexNames, inplace=True)
    df.columns = [
     dataColumnName]
    return df


def excel(filepath, useOpenpyxl=False, dataOnly=True, readOnly=True):
    r""" Create excel object from filepath.
    filepath: path to excel file
    useOpenpyxl: True for use custom 
    dataOnly: True for view only the values, not formula
    readOnly: True for read only, False for write options
    Ex.
            cp.excel("\path     o       he\excelfile.xlsx")
    """
    if isLinux():
        filepath = filepath.replace('\\', '/')
    elif os.path.isfile(filepath):
        if useOpenpyxl:
            from openpyxl import load_workbook
            return load_workbook(filepath, data_only=dataOnly, read_only=readOnly)
        return filepath
    else:
        raise ValueError('File not found')


def pandasFromExcel--- This code section failed: ---

 L. 635         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              pandas
                6  STORE_FAST               'pd'

 L. 637         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'excel'
               12  LOAD_GLOBAL              str
               14  CALL_FUNCTION_2       2  '2 positional arguments'
            16_18  POP_JUMP_IF_FALSE   484  'to 484'

 L. 639        20  LOAD_GLOBAL              isLinux
               22  CALL_FUNCTION_0       0  '0 positional arguments'
            24_26  POP_JUMP_IF_FALSE   266  'to 266'

 L. 640        28  LOAD_FAST                'excel'
               30  STORE_FAST               'filename'

 L. 641        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              dirname
               38  LOAD_FAST                'filename'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_FAST               'target_dir'

 L. 642        44  LOAD_GLOBAL              os
               46  LOAD_ATTR                path
               48  LOAD_METHOD              splitext
               50  LOAD_FAST                'filename'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'file_name'
               58  STORE_FAST               'file_extension'

 L. 643        60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              join
               66  LOAD_FAST                'target_dir'
               68  LOAD_FAST                'file_name'
               70  CALL_METHOD_2         2  '2 positional arguments'
               72  STORE_FAST               'target_dir'

 L. 644        74  LOAD_GLOBAL              os
               76  LOAD_ATTR                path
               78  LOAD_METHOD              join
               80  LOAD_FAST                'target_dir'
               82  LOAD_FAST                'namedRange'
               84  FORMAT_VALUE          0  ''
               86  LOAD_STR                 '.pkl'
               88  BUILD_STRING_2        2 
               90  CALL_METHOD_2         2  '2 positional arguments'
               92  STORE_FAST               'file_to_read_legacy'

 L. 645        94  LOAD_FAST                'target_dir'
               96  LOAD_CONST               None
               98  LOAD_FAST                'target_dir'
              100  LOAD_METHOD              rfind
              102  LOAD_STR                 '/'
              104  CALL_METHOD_1         1  '1 positional argument'
              106  LOAD_CONST               1
              108  BINARY_ADD       
              110  BUILD_SLICE_2         2 
              112  BINARY_SUBSCR    
              114  FORMAT_VALUE          0  ''
              116  LOAD_STR                 '.'
              118  LOAD_FAST                'target_dir'
              120  LOAD_FAST                'target_dir'
              122  LOAD_METHOD              rfind
              124  LOAD_STR                 '/'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  LOAD_CONST               1
              130  BINARY_ADD       
              132  LOAD_CONST               None
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  FORMAT_VALUE          0  ''
              140  BUILD_STRING_3        3 
              142  STORE_FAST               'target_dir'

 L. 647       144  LOAD_GLOBAL              os
              146  LOAD_ATTR                path
              148  LOAD_METHOD              isfile
              150  LOAD_GLOBAL              os
              152  LOAD_ATTR                path
              154  LOAD_METHOD              join
              156  LOAD_FAST                'target_dir'
              158  LOAD_FAST                'namedRange'
              160  FORMAT_VALUE          0  ''
              162  LOAD_STR                 '.pkl'
              164  BUILD_STRING_2        2 
              166  CALL_METHOD_2         2  '2 positional arguments'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  POP_JUMP_IF_FALSE   192  'to 192'
              172  LOAD_GLOBAL              os
              174  LOAD_ATTR                path
              176  LOAD_METHOD              join
              178  LOAD_FAST                'target_dir'
              180  LOAD_FAST                'namedRange'
              182  FORMAT_VALUE          0  ''
              184  LOAD_STR                 '.pkl'
              186  BUILD_STRING_2        2 
              188  CALL_METHOD_2         2  '2 positional arguments'
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           170  '170'
              192  LOAD_FAST                'file_to_read_legacy'
            194_0  COME_FROM           190  '190'
              194  STORE_FAST               'file_to_read'

 L. 649       196  LOAD_GLOBAL              os
              198  LOAD_ATTR                path
              200  LOAD_METHOD              isfile
              202  LOAD_FAST                'file_to_read'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_JUMP_IF_FALSE   248  'to 248'

 L. 650       208  LOAD_FAST                'pd'
              210  LOAD_ATTR                read_pickle
              212  LOAD_FAST                'file_to_read'
              214  LOAD_STR                 'gzip'
              216  LOAD_CONST               ('compression',)
              218  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              220  STORE_FAST               'df'

 L. 651       222  LOAD_FAST                'indexes'
              224  LOAD_CONST               None
              226  COMPARE_OP               is-not
              228  POP_JUMP_IF_FALSE   244  'to 244'

 L. 652       230  LOAD_FAST                'df'
              232  LOAD_ATTR                set_index
              234  LOAD_FAST                'indexes'
              236  LOAD_CONST               True
              238  LOAD_CONST               ('inplace',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  POP_TOP          
            244_0  COME_FROM           228  '228'

 L. 653       244  LOAD_FAST                'df'
              246  RETURN_VALUE     
            248_0  COME_FROM           206  '206'

 L. 656       248  LOAD_GLOBAL              ValueError
              250  LOAD_STR                 "Optimized version not found for: '"
              252  LOAD_FAST                'filename'
              254  FORMAT_VALUE          0  ''
              256  LOAD_STR                 "'"
              258  BUILD_STRING_3        3 
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  RAISE_VARARGS_1       1  'exception instance'
              264  JUMP_FORWARD        894  'to 894'
            266_0  COME_FROM            24  '24'

 L. 659       266  LOAD_CONST               0
              268  LOAD_CONST               None
              270  IMPORT_NAME              pyodbc
              272  STORE_FAST               'pyodbc'

 L. 661       274  LOAD_FAST                'pyodbc'
              276  LOAD_ATTR                connect
              278  LOAD_FAST                'driver'
              280  LOAD_FAST                'excel'
              282  BINARY_MODULO    
              284  LOAD_CONST               True
              286  LOAD_CONST               ('autocommit',)
              288  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              290  STORE_FAST               'cnxn'

 L. 662       292  LOAD_FAST                'cnxn'
              294  LOAD_METHOD              cursor
              296  CALL_METHOD_0         0  '0 positional arguments'
              298  STORE_FAST               'cursor'

 L. 663       300  LOAD_STR                 ''
              302  STORE_FAST               'table'

 L. 664       304  LOAD_FAST                'sheetName'
              306  LOAD_CONST               None
              308  COMPARE_OP               is-not
          310_312  POP_JUMP_IF_FALSE   326  'to 326'

 L. 665       314  LOAD_STR                 '['
              316  LOAD_FAST                'sheetName'
              318  BINARY_ADD       
              320  LOAD_STR                 '$]'
              322  BINARY_ADD       
              324  STORE_FAST               'table'
            326_0  COME_FROM           310  '310'

 L. 666       326  LOAD_FAST                'namedRange'
              328  LOAD_CONST               None
              330  COMPARE_OP               is-not
          332_334  POP_JUMP_IF_FALSE   348  'to 348'

 L. 667       336  LOAD_STR                 '['
              338  LOAD_FAST                'namedRange'
              340  BINARY_ADD       
              342  LOAD_STR                 ']'
              344  BINARY_ADD       
              346  STORE_FAST               'table'
            348_0  COME_FROM           332  '332'

 L. 668       348  LOAD_FAST                'cellRange'
              350  LOAD_CONST               None
              352  COMPARE_OP               is-not
          354_356  POP_JUMP_IF_FALSE   378  'to 378'

 L. 669       358  LOAD_STR                 '['
              360  LOAD_FAST                'sheetName'
              362  BINARY_ADD       
              364  LOAD_STR                 '$'
              366  BINARY_ADD       
              368  LOAD_FAST                'cellRange'
              370  BINARY_ADD       
              372  LOAD_STR                 ']'
              374  BINARY_ADD       
              376  STORE_FAST               'table'
            378_0  COME_FROM           354  '354'

 L. 671       378  LOAD_FAST                'cursor'
              380  LOAD_METHOD              execute
              382  LOAD_STR                 'SELECT * FROM '
              384  LOAD_FAST                'table'
              386  BINARY_ADD       
              388  CALL_METHOD_1         1  '1 positional argument'
              390  POP_TOP          

 L. 672       392  LOAD_FAST                'cursor'
              394  LOAD_METHOD              fetchall
              396  CALL_METHOD_0         0  '0 positional arguments'
              398  STORE_FAST               'rows'

 L. 673       400  LOAD_LISTCOMP            '<code_object <listcomp>>'
              402  LOAD_STR                 'pandasFromExcel.<locals>.<listcomp>'
              404  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              406  LOAD_FAST                'cursor'
              408  LOAD_ATTR                description
              410  GET_ITER         
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  STORE_FAST               'columnNames'

 L. 674       416  LOAD_FAST                'cnxn'
              418  LOAD_METHOD              close
              420  CALL_METHOD_0         0  '0 positional arguments'
              422  POP_TOP          

 L. 676       424  LOAD_FAST                'pd'
              426  LOAD_ATTR                DataFrame
              428  LOAD_ATTR                from_records
              430  LOAD_FAST                'rows'
              432  LOAD_FAST                'columnNames'
              434  LOAD_CONST               ('columns',)
              436  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              438  STORE_FAST               'df'

 L. 677       440  LOAD_FAST                'df'
              442  LOAD_ATTR                dropna
              444  LOAD_STR                 'all'
              446  LOAD_CONST               ('how',)
              448  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              450  STORE_FAST               'df'

 L. 678       452  LOAD_FAST                'indexes'
              454  LOAD_CONST               None
              456  COMPARE_OP               is-not
          458_460  POP_JUMP_IF_FALSE   476  'to 476'

 L. 679       462  LOAD_FAST                'df'
              464  LOAD_ATTR                set_index
              466  LOAD_FAST                'indexes'
              468  LOAD_CONST               True
              470  LOAD_CONST               ('inplace',)
              472  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              474  POP_TOP          
            476_0  COME_FROM           458  '458'

 L. 680       476  LOAD_FAST                'df'
              478  RETURN_VALUE     
          480_482  JUMP_FORWARD        894  'to 894'
            484_0  COME_FROM            16  '16'

 L. 683       484  LOAD_STR                 'openpyxl.workbook'
              486  LOAD_GLOBAL              str
              488  LOAD_GLOBAL              type
              490  LOAD_FAST                'excel'
              492  CALL_FUNCTION_1       1  '1 positional argument'
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  COMPARE_OP               in
          498_500  POP_JUMP_IF_FALSE   886  'to 886'

 L. 684       502  LOAD_CONST               None
              504  STORE_FAST               'rangeToRead'

 L. 685       506  LOAD_FAST                'namedRange'
              508  LOAD_CONST               None
              510  COMPARE_OP               is-not
          512_514  POP_JUMP_IF_FALSE   570  'to 570'

 L. 686       516  LOAD_FAST                'excel'
              518  LOAD_ATTR                defined_names
              520  LOAD_FAST                'namedRange'
              522  BINARY_SUBSCR    
              524  STORE_FAST               'the_range'

 L. 687       526  LOAD_FAST                'the_range'
              528  LOAD_ATTR                destinations
              530  STORE_FAST               'dests'

 L. 688       532  SETUP_LOOP          606  'to 606'
              534  LOAD_FAST                'dests'
              536  GET_ITER         
              538  FOR_ITER            566  'to 566'
              540  UNPACK_SEQUENCE_2     2 
              542  STORE_FAST               'title'
              544  STORE_FAST               'coord'

 L. 689       546  LOAD_FAST                'excel'
              548  LOAD_FAST                'title'
              550  BINARY_SUBSCR    
              552  STORE_FAST               'ws'

 L. 690       554  LOAD_FAST                'ws'
              556  LOAD_FAST                'coord'
              558  BINARY_SUBSCR    
              560  STORE_FAST               'rangeToRead'
          562_564  JUMP_BACK           538  'to 538'
              566  POP_BLOCK        
              568  JUMP_FORWARD        606  'to 606'
            570_0  COME_FROM           512  '512'

 L. 691       570  LOAD_FAST                'cellRange'
              572  LOAD_CONST               None
              574  COMPARE_OP               is-not
          576_578  POP_JUMP_IF_FALSE   598  'to 598'

 L. 692       580  LOAD_FAST                'excel'
              582  LOAD_FAST                'sheetName'
              584  BINARY_SUBSCR    
              586  STORE_FAST               'ws'

 L. 693       588  LOAD_FAST                'ws'
              590  LOAD_FAST                'cellRange'
              592  BINARY_SUBSCR    
              594  STORE_FAST               'rangeToRead'
              596  JUMP_FORWARD        606  'to 606'
            598_0  COME_FROM           576  '576'

 L. 695       598  LOAD_FAST                'excel'
              600  LOAD_FAST                'sheetName'
              602  BINARY_SUBSCR    
              604  STORE_FAST               'rangeToRead'
            606_0  COME_FROM           596  '596'
            606_1  COME_FROM           568  '568'
            606_2  COME_FROM_LOOP      532  '532'

 L. 697       606  LOAD_CONST               0
              608  STORE_FAST               'nn'

 L. 698       610  BUILD_LIST_0          0 
              612  STORE_FAST               'cols'

 L. 699       614  BUILD_LIST_0          0 
              616  STORE_FAST               'values'

 L. 700       618  SETUP_LOOP          688  'to 688'
              620  LOAD_FAST                'rangeToRead'
              622  GET_ITER         
              624  FOR_ITER            686  'to 686'
              626  STORE_FAST               'row'

 L. 701       628  LOAD_FAST                'nn'
              630  LOAD_CONST               0
              632  COMPARE_OP               ==
          634_636  POP_JUMP_IF_FALSE   654  'to 654'

 L. 702       638  LOAD_LISTCOMP            '<code_object <listcomp>>'
              640  LOAD_STR                 'pandasFromExcel.<locals>.<listcomp>'
              642  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              644  LOAD_FAST                'row'
              646  GET_ITER         
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  STORE_FAST               'cols'
              652  JUMP_FORWARD        674  'to 674'
            654_0  COME_FROM           634  '634'

 L. 704       654  LOAD_FAST                'values'
              656  LOAD_METHOD              append
              658  LOAD_LISTCOMP            '<code_object <listcomp>>'
              660  LOAD_STR                 'pandasFromExcel.<locals>.<listcomp>'
              662  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              664  LOAD_FAST                'row'
              666  GET_ITER         
              668  CALL_FUNCTION_1       1  '1 positional argument'
              670  CALL_METHOD_1         1  '1 positional argument'
              672  POP_TOP          
            674_0  COME_FROM           652  '652'

 L. 705       674  LOAD_FAST                'nn'
            676_0  COME_FROM           264  '264'
              676  LOAD_CONST               1
              678  INPLACE_ADD      
              680  STORE_FAST               'nn'
          682_684  JUMP_BACK           624  'to 624'
              686  POP_BLOCK        
            688_0  COME_FROM_LOOP      618  '618'

 L. 706       688  LOAD_CONST               0
              690  STORE_FAST               'nn'

 L. 707       692  BUILD_LIST_0          0 
              694  STORE_FAST               '_finalCols'

 L. 708       696  SETUP_LOOP          760  'to 760'
              698  LOAD_FAST                'cols'
              700  GET_ITER         
              702  FOR_ITER            758  'to 758'
              704  STORE_FAST               '_col'

 L. 709       706  LOAD_FAST                '_col'
              708  LOAD_CONST               None
              710  COMPARE_OP               is
          712_714  POP_JUMP_IF_FALSE   744  'to 744'

 L. 710       716  LOAD_FAST                '_finalCols'
              718  LOAD_METHOD              append
              720  LOAD_STR                 'Unnamed'
              722  LOAD_GLOBAL              str
              724  LOAD_FAST                'nn'
              726  CALL_FUNCTION_1       1  '1 positional argument'
              728  BINARY_ADD       
              730  CALL_METHOD_1         1  '1 positional argument'
              732  POP_TOP          

 L. 711       734  LOAD_FAST                'nn'
              736  LOAD_CONST               1
              738  INPLACE_ADD      
              740  STORE_FAST               'nn'
              742  JUMP_BACK           702  'to 702'
            744_0  COME_FROM           712  '712'

 L. 713       744  LOAD_FAST                '_finalCols'
              746  LOAD_METHOD              append
              748  LOAD_FAST                '_col'
              750  CALL_METHOD_1         1  '1 positional argument'
              752  POP_TOP          
          754_756  JUMP_BACK           702  'to 702'
              758  POP_BLOCK        
            760_0  COME_FROM_LOOP      696  '696'

 L. 715       760  LOAD_FAST                'pd'
              762  LOAD_ATTR                DataFrame
              764  LOAD_FAST                'values'
              766  LOAD_FAST                '_finalCols'
              768  LOAD_CONST               ('columns',)
              770  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              772  STORE_FAST               'df'

 L. 716       774  LOAD_FAST                'indexes'
              776  LOAD_CONST               None
              778  COMPARE_OP               is-not
          780_782  POP_JUMP_IF_FALSE   874  'to 874'

 L. 717       784  LOAD_GLOBAL              isinstance
              786  LOAD_FAST                'indexes'
              788  LOAD_GLOBAL              str
              790  CALL_FUNCTION_2       2  '2 positional arguments'
          792_794  POP_JUMP_IF_FALSE   802  'to 802'

 L. 718       796  LOAD_FAST                'indexes'
              798  BUILD_LIST_1          1 
              800  STORE_FAST               'indexes'
            802_0  COME_FROM           792  '792'

 L. 719       802  BUILD_LIST_0          0 
              804  STORE_FAST               'toIndex'

 L. 720       806  SETUP_LOOP          846  'to 846'
              808  LOAD_FAST                'indexes'
              810  GET_ITER         
            812_0  COME_FROM           826  '826'
              812  FOR_ITER            844  'to 844'
              814  STORE_FAST               'indexColumn'

 L. 721       816  LOAD_FAST                'indexColumn'
              818  LOAD_FAST                'df'
              820  LOAD_ATTR                columns
              822  LOAD_ATTR                values
              824  COMPARE_OP               in
          826_828  POP_JUMP_IF_FALSE   812  'to 812'

 L. 722       830  LOAD_FAST                'toIndex'
              832  LOAD_METHOD              append
              834  LOAD_FAST                'indexColumn'
              836  CALL_METHOD_1         1  '1 positional argument'
              838  POP_TOP          
          840_842  JUMP_BACK           812  'to 812'
              844  POP_BLOCK        
            846_0  COME_FROM_LOOP      806  '806'

 L. 723       846  LOAD_GLOBAL              len
              848  LOAD_FAST                'toIndex'
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  LOAD_CONST               0
              854  COMPARE_OP               >
          856_858  POP_JUMP_IF_FALSE   874  'to 874'

 L. 724       860  LOAD_FAST                'df'
              862  LOAD_ATTR                set_index
              864  LOAD_FAST                'toIndex'
              866  LOAD_CONST               True
              868  LOAD_CONST               ('inplace',)
              870  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              872  POP_TOP          
            874_0  COME_FROM           856  '856'
            874_1  COME_FROM           780  '780'

 L. 726       874  LOAD_FAST                'df'
              876  LOAD_ATTR                dropna
              878  LOAD_STR                 'all'
              880  LOAD_CONST               ('how',)
              882  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              884  RETURN_VALUE     
            886_0  COME_FROM           498  '498'

 L. 728       886  LOAD_GLOBAL              ValueError
              888  LOAD_STR                 'excel can be cp.excel object'
              890  CALL_FUNCTION_1       1  '1 positional argument'
              892  RAISE_VARARGS_1       1  'exception instance'
            894_0  COME_FROM           480  '480'

Parse error at or near `LOAD_CONST' instruction at offset 676


def indexFromExcel(excel, sheetName=None, namedRange=None, cellRange=None, columnName=None, removeEmpty=True, indexName='new index'):
    """ Return a cp.index from an excel file.
    excel: cp.excel object
    sheetName: sheet name to be read
    namedRange: name of the range to be read
    cellRange: used with sheetname, for read from a simple range
    columnName: dataframe column name used for create cp.index. By default is created using the first column
    removeEmpty: True for remove empty rows
    indexName: new index name 
        Ex.
            cp.indexFromExcel(excelNode,"Sheet 1")
            cp.indexFromExcel(excelNode,namedRange="name_range")
            cp.indexFromExcel(excelNode,namedRange="name_range", columnName="indicadores")
    """
    if isinstance(excel, str) or 'openpyxl.workbook' in str(type(excel)):
        _df = pandasFromExcel(excel, sheetName, namedRange, cellRange)
        return indexFromPandas(_df, columnName, removeEmpty, indexName=indexName)
    raise ValueError('excel can be cp.excel object or a str path to the filename')


def cubeFromExcel(excel, sheetName=None, namedRange=None, cellRange=None, cubeIndexes=None, valueColumns=None, indexColumnHeaders=None, replaceByIndex=None):
    """ Return a cp.cube from excel file.
        excel: cp.excel object
    sheetName: sheet name to be read
    namedRange: name of the range to be read
    cellRange: used with sheetname, for read from a simple range
    cubeIndexes: objects cp.index for perform change index
    valueColumns: string with column name of the dataframe where contain the values
                    cp.index with columns names for convert colums to index
    indexColumnHeaders: (optional) column names in pandas to parse with cubeIndexes. Used if header on dataframe is not equal to index identifiers.
    replaceByIndex: (optional) replace index used in valueColumns for this index. (using changeindex)

        Ex.
            cp.cubeFromExcel(excelNode,"Sheet 1",cubeIndexes=[indicadores],valueColumns="descuentos")
            cp.cubeFromExcel(excelNode,namedRange="nombre_rango",cubeIndexes=[indicadores],valueColumns=time)
    """
    if isinstance(excel, str) or 'openpyxl.workbook' in str(type(excel)):
        _df = pandasFromExcel(excel, sheetName, namedRange, cellRange)
        return cubeFromPandas(_df, cubeIndexes, valueColumns, indexColumnHeaders, replaceByIndex=replaceByIndex)
    raise ValueError('excel can be cp.excel object or a str path to the filename')


def sequence(initialNum, finalNum, stepSize=1, dtype=None, indexName='new index'):
    """
    Creates an index with a list of numbers increasing or decreasing from initial_num to final_num by increments (or decrements) of stepSize, which is optional and defaults to 1
    """
    values = np.arange(initialNum, (finalNum + 1), step=stepSize, dtype=dtype)
    return index(indexName, values)


def lookup(cubeWithData, cubeWithMap, sharedIndex):
    """
    Returns the value of cubeWithData indexed by the index of cubeWithMap.
    cubeWithData must be indexed by sharedIndex and cubeWithData values must correspond to elements of sharedIndex.
    For example: Let's say you have a cube with an estimated inflation rate by Country ("inflation_rate" is the name of the cube; "country" is the name of the index) and you want to assign it to the corresponding Company depending on its location. On the other hand, there's a many-to-one map where each Company is allocated to a single Country ("country_to_company_allocation"). The sharedIndex, in this case, is Country ("country").
    As a result, 
        cp.lookup( inflation_rate , country_to_company_allocation , country )
    will return the estimated inflation rate by Company.
    """
    _final_cube = ((cubeWithMap == sharedIndex) * cubeWithData).sum(sharedIndex)
    return _final_cube


def cubeFromNumpy(npArray):
    """ 
    Return a cube object from numpy Array. Generate temporal indexes
    """
    _dimsNames = ['axis ' + str(x) for x in range(npArray.ndim)]
    _dimsValues = [list(x) for x in (range(npArray.shape[y]) for y in range(npArray.ndim))]
    _indexes = [cubepy.Index(_dimsNames[x], _dimsValues[x]) for x in range(len(_dimsNames))]
    _cube = cube(_indexes, npArray)
    return _cube


def movingStats(cube, index, window=12, fn=np.mean):
    """
        Allows to calculate in a moving Window the selected statistics measure
    """
    _realWindow = abs(window)
    _fInvert = lambda x: x[::-1].rolling(_realWindow).apply(fn)[::-1].shift(-1)
    _fNorm = lambda x: x.rolling(_realWindow).apply(fn).shift()
    _realF = _fNorm if window < 0 else _fInvert
    _levelList = [lvl.name for lvl in cube.axes if lvl.name != index.name]
    _df = pandasFromCube(cube)
    if cube.ndim > 1:
        _df = _df.groupby(level=_levelList)['value'].apply(_realF)
    else:
        _df = _df.apply(_realF)
    return cubeFromPandas(_df, cube.axes, 'value')


def isLinux():
    if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
        return True
    return False