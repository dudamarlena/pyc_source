# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/metaarray/MetaArray.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 56944 bytes
"""
MetaArray.py -  Class encapsulating ndarray with meta data
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more infomation.

MetaArray is an array class based on numpy.ndarray that allows storage of per-axis meta data
such as axis values, names, units, column names, etc. It also enables several
new methods for slicing and indexing the array based on this meta data. 
More info at http://www.scipy.org/Cookbook/MetaArray
"""
import numpy as np, types, copy, threading, os, re, pickle
from functools import reduce
USE_HDF5 = True
try:
    import h5py
    HAVE_HDF5 = True
except:
    USE_HDF5 = False
    HAVE_HDF5 = False

def axis(name=None, cols=None, values=None, units=None):
    """Convenience function for generating axis descriptions when defining MetaArrays"""
    ax = {}
    cNameOrder = [
     'name', 'units', 'title']
    if name is not None:
        ax['name'] = name
    if values is not None:
        ax['values'] = values
    if units is not None:
        ax['units'] = units
    if cols is not None:
        ax['cols'] = []
        for c in cols:
            if type(c) != list:
                if type(c) != tuple:
                    c = [
                     c]
            col = {}
            for i in range(0, len(c)):
                col[cNameOrder[i]] = c[i]

            ax['cols'].append(col)

    return ax


class sliceGenerator(object):
    __doc__ = 'Just a compact way to generate tuples of slice objects.'

    def __getitem__(self, arg):
        return arg

    def __getslice__(self, arg):
        return arg


SLICER = sliceGenerator()

class MetaArray(object):
    __doc__ = "N-dimensional array with meta data such as axis titles, units, and column names.\n  \n    May be initialized with a file name, a tuple representing the dimensions of the array,\n    or any arguments that could be passed on to numpy.array()\n  \n    The info argument sets the metadata for the entire array. It is composed of a list\n    of axis descriptions where each axis may have a name, title, units, and a list of column \n    descriptions. An additional dict at the end of the axis list may specify parameters\n    that apply to values in the entire array.\n  \n    For example:\n        A 2D array of altitude values for a topographical map might look like\n            info=[\n        {'name': 'lat', 'title': 'Lattitude'}, \n        {'name': 'lon', 'title': 'Longitude'}, \n        {'title': 'Altitude', 'units': 'm'}\n      ]\n        In this case, every value in the array represents the altitude in feet at the lat, lon\n        position represented by the array index. All of the following return the \n        value at lat=10, lon=5:\n            array[10, 5]\n            array['lon':5, 'lat':10]\n            array['lat':10][5]\n        Now suppose we want to combine this data with another array of equal dimensions that\n        represents the average rainfall for each location. We could easily store these as two \n        separate arrays or combine them into a 3D array with this description:\n            info=[\n        {'name': 'vals', 'cols': [\n          {'name': 'altitude', 'units': 'm'}, \n          {'name': 'rainfall', 'units': 'cm/year'}\n        ]},\n        {'name': 'lat', 'title': 'Lattitude'}, \n        {'name': 'lon', 'title': 'Longitude'}\n      ]\n        We can now access the altitude values with array[0] or array['altitude'], and the\n        rainfall values with array[1] or array['rainfall']. All of the following return\n        the rainfall value at lat=10, lon=5:\n            array[1, 10, 5]\n            array['lon':5, 'lat':10, 'val': 'rainfall']\n            array['rainfall', 'lon':5, 'lat':10]\n        Notice that in the second example, there is no need for an extra (4th) axis description\n        since the actual values are described (name and units) in the column info for the first axis.\n    "
    version = '2'
    defaultCompression = None
    nameTypes = [
     basestring, tuple]

    @staticmethod
    def isNameType(var):
        return any([isinstance(var, t) for t in MetaArray.nameTypes])

    wrapMethods = set(['__eq__', '__ne__', '__le__', '__lt__', '__ge__', '__gt__'])

    def __init__(self, data=None, info=None, dtype=None, file=None, copy=False, **kwargs):
        object.__init__(self)
        self._isHDF = False
        if file is not None:
            self._data = None
            (self.readFile)(file, **kwargs)
            if kwargs.get('readAllData', True) and self._data is None:
                raise Exception('File read failed: %s' % file)
        else:
            self._info = info
            if hasattr(data, 'implements') and data.implements('MetaArray'):
                self._info = data._info
                self._data = data.asarray()
            else:
                if isinstance(data, tuple):
                    self._data = np.empty(data, dtype=dtype)
                else:
                    self._data = np.array(data, dtype=dtype, copy=copy)
        self.checkInfo()

    def checkInfo(self):
        info = self._info
        if info is None:
            if self._data is None:
                return
            self._info = [{} for i in range(self.ndim)]
            return
        else:
            try:
                info = list(info)
            except:
                raise Exception('Info must be a list of axis specifications')

            if len(info) < self.ndim + 1:
                info.extend([{}] * (self.ndim + 1 - len(info)))
            else:
                if len(info) > self.ndim + 1:
                    raise Exception('Info parameter must be list of length ndim+1 or less.')
            for i in range(len(info)):
                if not isinstance(info[i], dict):
                    if info[i] is None:
                        info[i] = {}
                    else:
                        raise Exception('Axis specification must be Dict or None')
                if i < self.ndim and 'values' in info[i]:
                    if type(info[i]['values']) is list:
                        info[i]['values'] = np.array(info[i]['values'])
                    else:
                        if type(info[i]['values']) is not np.ndarray:
                            raise Exception('Axis values must be specified as list or ndarray')
                        if info[i]['values'].ndim != 1 or info[i]['values'].shape[0] != self.shape[i]:
                            raise Exception('Values array for axis %d has incorrect shape. (given %s, but should be %s)' % (i, str(info[i]['values'].shape), str((self.shape[i],))))
                    if i < self.ndim and 'cols' in info[i]:
                        if not isinstance(info[i]['cols'], list):
                            info[i]['cols'] = list(info[i]['cols'])
                        if len(info[i]['cols']) != self.shape[i]:
                            raise Exception('Length of column list for axis %d does not match data. (given %d, but should be %d)' % (i, len(info[i]['cols']), self.shape[i]))

    def implements(self, name=None):
        if name is None:
            return [
             'MetaArray']
        return name == 'MetaArray'

    def __getitem__(self, ind):
        nInd = self._interpretIndexes(ind)
        a = self._data[nInd]
        if len(nInd) == self.ndim:
            if np.all([not isinstance(ind, slice) for ind in nInd]):
                return a
        info = []
        extraInfo = self._info[(-1)].copy()
        for i in range(0, len(nInd)):
            if type(nInd[i]) in [slice, list] or isinstance(nInd[i], np.ndarray):
                info.append(self._axisSlice(i, nInd[i]))
            else:
                newInfo = self._axisSlice(i, nInd[i])
                name = None
                colName = None
                for k in newInfo:
                    if k == 'cols':
                        if 'cols' not in extraInfo:
                            extraInfo['cols'] = []
                        extraInfo['cols'].append(newInfo[k])
                        if 'units' in newInfo[k]:
                            extraInfo['units'] = newInfo[k]['units']
                        if 'name' in newInfo[k]:
                            colName = newInfo[k]['name']
                        else:
                            if k == 'name':
                                name = newInfo[k]
                    else:
                        if k not in extraInfo:
                            extraInfo[k] = newInfo[k]
                        extraInfo[k] = newInfo[k]

            if 'name' not in extraInfo:
                if name is None:
                    if colName is not None:
                        extraInfo['name'] = colName
                    else:
                        if colName is not None:
                            extraInfo['name'] = str(name) + ': ' + str(colName)
                else:
                    extraInfo['name'] = name

        info.append(extraInfo)
        return MetaArray(a, info=info)

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def shape(self):
        return self._data.shape

    @property
    def dtype(self):
        return self._data.dtype

    def __len__(self):
        return len(self._data)

    def __getslice__(self, *args):
        return self.__getitem__(slice(*args))

    def __setitem__(self, ind, val):
        nInd = self._interpretIndexes(ind)
        try:
            self._data[nInd] = val
        except:
            print(self, nInd, val)
            raise

    def __getattr__(self, attr):
        if attr in self.wrapMethods:
            return getattr(self._data, attr)
        raise AttributeError(attr)

    def __eq__(self, b):
        return self._binop('__eq__', b)

    def __ne__(self, b):
        return self._binop('__ne__', b)

    def __sub__(self, b):
        return self._binop('__sub__', b)

    def __add__(self, b):
        return self._binop('__add__', b)

    def __mul__(self, b):
        return self._binop('__mul__', b)

    def __div__(self, b):
        return self._binop('__div__', b)

    def __truediv__(self, b):
        return self._binop('__truediv__', b)

    def _binop(self, op, b):
        if isinstance(b, MetaArray):
            b = b.asarray()
        a = self.asarray()
        c = getattr(a, op)(b)
        if c.shape != a.shape:
            raise Exception('Binary operators with MetaArray must return an array of the same shape (this shape is %s, result shape was %s)' % (a.shape, c.shape))
        return MetaArray(c, info=(self.infoCopy()))

    def asarray(self):
        if isinstance(self._data, np.ndarray):
            return self._data
        return np.array(self._data)

    def __array__(self):
        return self.asarray()

    def view(self, typ):
        if typ is np.ndarray:
            return self.asarray()
        raise Exception('invalid view type: %s' % str(typ))

    def axisValues(self, axis):
        """Return the list of values for an axis"""
        ax = self._interpretAxis(axis)
        if 'values' in self._info[ax]:
            return self._info[ax]['values']
        raise Exception('Array axis %s (%d) has no associated values.' % (str(axis), ax))

    def xvals(self, axis):
        """Synonym for axisValues()"""
        return self.axisValues(axis)

    def axisHasValues(self, axis):
        ax = self._interpretAxis(axis)
        return 'values' in self._info[ax]

    def axisHasColumns(self, axis):
        ax = self._interpretAxis(axis)
        return 'cols' in self._info[ax]

    def axisUnits(self, axis):
        """Return the units for axis"""
        ax = self._info[self._interpretAxis(axis)]
        if 'units' in ax:
            return ax['units']

    def hasColumn(self, axis, col):
        ax = self._info[self._interpretAxis(axis)]
        if 'cols' in ax:
            for c in ax['cols']:
                if c['name'] == col:
                    return True

        return False

    def listColumns(self, axis=None):
        """Return a list of column names for axis. If axis is not specified, then return a dict of {axisName: (column names), ...}."""
        if axis is None:
            ret = {}
            for i in range(self.ndim):
                if 'cols' in self._info[i]:
                    cols = [c['name'] for c in self._info[i]['cols']]
                else:
                    cols = []
                ret[self.axisName(i)] = cols

            return ret
        axis = self._interpretAxis(axis)
        return [c['name'] for c in self._info[axis]['cols']]

    def columnName(self, axis, col):
        ax = self._info[self._interpretAxis(axis)]
        return ax['cols'][col]['name']

    def axisName(self, n):
        return self._info[n].get('name', n)

    def columnUnits(self, axis, column):
        """Return the units for column in axis"""
        ax = self._info[self._interpretAxis(axis)]
        if 'cols' in ax:
            for c in ax['cols']:
                if c['name'] == column:
                    return c['units']

            raise Exception('Axis %s has no column named %s' % (str(axis), str(column)))
        else:
            raise Exception('Axis %s has no column definitions' % str(axis))

    def rowsort(self, axis, key=0):
        """Return this object with all records sorted along axis using key as the index to the values to compare. Does not yet modify meta info."""
        keyList = self[key]
        order = keyList.argsort()
        if type(axis) == int:
            ind = [
             slice(None)] * axis
            ind.append(order)
        else:
            if isinstance(axis, basestring):
                ind = (
                 slice(axis, order),)
        return self[tuple(ind)]

    def append(self, val, axis):
        """Return this object with val appended along axis. Does not yet combine meta info."""
        s = list(self.shape)
        axis = self._interpretAxis(axis)
        s[axis] += 1
        n = MetaArray((tuple(s)), info=(self._info), dtype=(self.dtype))
        ind = [slice(None)] * self.ndim
        ind[axis] = slice(None, -1)
        n[tuple(ind)] = self
        ind[axis] = -1
        n[tuple(ind)] = val
        return n

    def extend(self, val, axis):
        """Return the concatenation along axis of this object and val. Does not yet combine meta info."""
        axis = self._interpretAxis(axis)
        return MetaArray((np.concatenate(self, val, axis)), info=(self._info))

    def infoCopy(self, axis=None):
        """Return a deep copy of the axis meta info for this object"""
        if axis is None:
            return copy.deepcopy(self._info)
        return copy.deepcopy(self._info[self._interpretAxis(axis)])

    def copy(self):
        return MetaArray((self._data.copy()), info=(self.infoCopy()))

    def _interpretIndexes(self, ind):
        if not isinstance(ind, tuple):
            if isinstance(ind, list) and len(ind) > 0 and isinstance(ind[0], slice):
                ind = tuple(ind)
            else:
                ind = (
                 ind,)
        nInd = [
         slice(None)] * self.ndim
        numOk = True
        for i in range(0, len(ind)):
            axis, index, isNamed = self._interpretIndex(ind[i], i, numOk)
            nInd[axis] = index
            if isNamed:
                numOk = False

        return tuple(nInd)

    def _interpretAxis(self, axis):
        if isinstance(axis, basestring) or isinstance(axis, tuple):
            return self._getAxis(axis)
        return axis

    def _interpretIndex(self, ind, pos, numOk):
        if type(ind) is int:
            if not numOk:
                raise Exception('string and integer indexes may not follow named indexes')
            else:
                return (
                 pos, ind, False)
                if MetaArray.isNameType(ind):
                    if not numOk:
                        raise Exception('string and integer indexes may not follow named indexes')
                    return (pos, self._getIndex(pos, ind), False)
                if type(ind) is slice:
                    if MetaArray.isNameType(ind.start) or MetaArray.isNameType(ind.stop):
                        axis = self._interpretAxis(ind.start)
                        if MetaArray.isNameType(ind.stop):
                            index = self._getIndex(axis, ind.stop)
                    elif isinstance(ind.stop, float) or isinstance(ind.step, float):
                        if 'values' in self._info[axis]:
                            if ind.stop is None:
                                mask = self.xvals(axis) < ind.step
                            else:
                                if ind.step is None:
                                    mask = self.xvals(axis) >= ind.stop
                                else:
                                    mask = (self.xvals(axis) >= ind.stop) * (self.xvals(axis) < ind.step)
                            index = mask
                    elif isinstance(ind.stop, int) or isinstance(ind.step, int):
                        if ind.step is None:
                            index = ind.stop
                    else:
                        index = slice(ind.stop, ind.step)
                else:
                    if type(ind.stop) is list:
                        index = []
                        for i in ind.stop:
                            if type(i) is int:
                                index.append(i)
                            elif MetaArray.isNameType(i):
                                index.append(self._getIndex(axis, i))
                            else:
                                index = ind.stop
                                break

                    else:
                        index = ind.stop
                return (
                 axis, index, True)
            return (
             pos, ind, False)
        else:
            if type(ind) is list:
                indList = [self._interpretIndex(i, pos, numOk)[1] for i in ind]
                return (pos, indList, False)
            if not numOk:
                raise Exception('string and integer indexes may not follow named indexes')
            return (pos, ind, False)

    def _getAxis(self, name):
        for i in range(0, len(self._info)):
            axis = self._info[i]
            if 'name' in axis and axis['name'] == name:
                return i

        raise Exception('No axis named %s.\n  info=%s' % (name, self._info))

    def _getIndex(self, axis, name):
        ax = self._info[axis]
        if ax is not None:
            if 'cols' in ax:
                for i in range(0, len(ax['cols'])):
                    if 'name' in ax['cols'][i] and ax['cols'][i]['name'] == name:
                        return i

        raise Exception('Axis %d has no column named %s.\n  info=%s' % (axis, name, self._info))

    def _axisCopy(self, i):
        return copy.deepcopy(self._info[i])

    def _axisSlice(self, i, cols):
        if 'cols' in self._info[i] or 'values' in self._info[i]:
            ax = self._axisCopy(i)
            if 'cols' in ax:
                sl = np.array(ax['cols'])[cols]
                if isinstance(sl, np.ndarray):
                    sl = list(sl)
                ax['cols'] = sl
            if 'values' in ax:
                ax['values'] = np.array(ax['values'])[cols]
        else:
            ax = self._info[i]
        return ax

    def prettyInfo(self):
        s = ''
        titles = []
        maxl = 0
        for i in range(len(self._info) - 1):
            ax = self._info[i]
            axs = ''
            if 'name' in ax:
                axs += '"%s"' % str(ax['name'])
            else:
                axs += '%d' % i
            if 'units' in ax:
                axs += ' (%s)' % str(ax['units'])
            titles.append(axs)
            if len(axs) > maxl:
                maxl = len(axs)

        for i in range(min(self.ndim, len(self._info) - 1)):
            ax = self._info[i]
            axs = titles[i]
            axs += '%s[%d] :' % (' ' * (maxl + 2 - len(axs)), self.shape[i])
            if 'values' in ax:
                v0 = ax['values'][0]
                v1 = ax['values'][(-1)]
                axs += ' values: [%g ... %g] (step %g)' % (v0, v1, (v1 - v0) / (self.shape[i] - 1))
            if 'cols' in ax:
                axs += ' columns: '
                colstrs = []
                for c in range(len(ax['cols'])):
                    col = ax['cols'][c]
                    cs = str(col.get('name', c))
                    if 'units' in col:
                        cs += ' (%s)' % col['units']
                    colstrs.append(cs)

                axs += '[' + ', '.join(colstrs) + ']'
            s += axs + '\n'

        s += str(self._info[(-1)])
        return s

    def __repr__(self):
        return '%s\n-----------------------------------------------\n%s' % (self.view(np.ndarray).__repr__(), self.prettyInfo())

    def __str__(self):
        return self.__repr__()

    def axisCollapsingFn(self, fn, axis=None, *args, **kargs):
        fn = getattr(self._data, fn)
        if axis is None:
            return fn(axis, *args, **kargs)
        info = self.infoCopy()
        axis = self._interpretAxis(axis)
        info.pop(axis)
        return MetaArray(fn(axis, *args, **kargs), info=info)

    def mean(self, axis=None, *args, **kargs):
        return (self.axisCollapsingFn)('mean', axis, *args, **kargs)

    def min(self, axis=None, *args, **kargs):
        return (self.axisCollapsingFn)('min', axis, *args, **kargs)

    def max(self, axis=None, *args, **kargs):
        return (self.axisCollapsingFn)('max', axis, *args, **kargs)

    def transpose(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            order = args[0]
        else:
            order = args
        order = [self._interpretAxis(ax) for ax in order]
        infoOrder = order + list(range(len(order), len(self._info)))
        info = [self._info[i] for i in infoOrder]
        order = order + list(range(len(order), self.ndim))
        try:
            if self._isHDF:
                return MetaArray((np.array(self._data).transpose(order)), info=info)
            return MetaArray((self._data.transpose(order)), info=info)
        except:
            print(order)
            raise

    def readFile(self, filename, **kwargs):
        """Load the data and meta info stored in *filename*
        Different arguments are allowed depending on the type of file.
        For HDF5 files:
        
            *writable* (bool) if True, then any modifications to data in the array will be stored to disk.
            *readAllData* (bool) if True, then all data in the array is immediately read from disk
                          and the file is closed (this is the default for files < 500MB). Otherwise, the file will
                          be left open and data will be read only as requested (this is 
                          the default for files >= 500MB).
        
        
        """
        with open(filename, 'rb') as (fd):
            magic = fd.read(8)
            if magic == '\x89HDF\r\n\x1a\n':
                fd.close()
                (self._readHDF5)(filename, **kwargs)
                self._isHDF = True
            else:
                fd.seek(0)
                meta = MetaArray._readMeta(fd)
                if not kwargs.get('readAllData', True):
                    self._data = np.empty((meta['shape']), dtype=(meta['type']))
                elif 'version' in meta:
                    ver = meta['version']
                else:
                    ver = 1
                rFuncName = '_readData%s' % str(ver)
                if not hasattr(MetaArray, rFuncName):
                    raise Exception("This MetaArray library does not support array version '%s'" % ver)
                rFunc = getattr(self, rFuncName)
                rFunc(fd, meta, **kwargs)
                self._isHDF = False

    @staticmethod
    def _readMeta(fd):
        """Read meta array from the top of a file. Read lines until a blank line is reached.
        This function should ideally work for ALL versions of MetaArray.
        """
        meta = ''
        while True:
            line = fd.readline().strip()
            if line == '':
                break
            meta += line

        ret = eval(meta)
        return ret

    def _readData1(self, fd, meta, mmap=False, **kwds):
        frameSize = 1
        for ax in meta['info']:
            if 'values_len' in ax:
                ax['values'] = np.fromstring((fd.read(ax['values_len'])), dtype=(ax['values_type']))
                frameSize *= ax['values_len']
                del ax['values_len']
                del ax['values_type']

        self._info = meta['info']
        if not kwds.get('readAllData', True):
            return
        if mmap:
            subarr = np.memmap(fd, dtype=(meta['type']), mode='r', shape=(meta['shape']))
        else:
            subarr = np.fromstring((fd.read()), dtype=(meta['type']))
            subarr.shape = meta['shape']
        self._data = subarr

    def _readData2(self, fd, meta, mmap=False, subset=None, **kwds):
        dynAxis = None
        frameSize = 1
        for i in range(len(meta['info'])):
            ax = meta['info'][i]
            if 'values_len' in ax:
                if ax['values_len'] == 'dynamic':
                    if dynAxis is not None:
                        raise Exception('MetaArray has more than one dynamic axis! (this is not allowed)')
                    dynAxis = i
                else:
                    ax['values'] = np.fromstring((fd.read(ax['values_len'])), dtype=(ax['values_type']))
                    frameSize *= ax['values_len']
                    del ax['values_len']
                    del ax['values_type']

        self._info = meta['info']
        if not kwds.get('readAllData', True):
            return
        if dynAxis is None:
            if meta['type'] == 'object':
                if mmap:
                    raise Exception('memmap not supported for arrays with dtype=object')
                subarr = pickle.loads(fd.read())
            else:
                if mmap:
                    subarr = np.memmap(fd, dtype=(meta['type']), mode='r', shape=(meta['shape']))
                else:
                    subarr = np.fromstring((fd.read()), dtype=(meta['type']))
            subarr.shape = meta['shape']
        else:
            if mmap:
                raise Exception('memmap not supported for non-contiguous arrays. Use rewriteContiguous() to convert.')
            ax = meta['info'][dynAxis]
            xVals = []
            frames = []
            frameShape = list(meta['shape'])
            frameShape[dynAxis] = 1
            frameSize = reduce(lambda a, b: a * b, frameShape)
            n = 0
            while 1:
                while 1:
                    line = fd.readline()
                    if line != '\n':
                        break

                if line == '':
                    break
                else:
                    inf = eval(line)
                    if meta['type'] == 'object':
                        data = pickle.loads(fd.read(inf['len']))
                    else:
                        data = np.fromstring((fd.read(inf['len'])), dtype=(meta['type']))
                    if data.size != frameSize * inf['numFrames']:
                        raise Exception('Wrong frame size in MetaArray file! (frame %d)' % n)
                    else:
                        shape = list(frameShape)
                        shape[dynAxis] = inf['numFrames']
                        data.shape = shape
                        if subset is not None:
                            dSlice = subset[dynAxis]
                            if dSlice.start is None:
                                dStart = 0
                            else:
                                dStart = max(0, dSlice.start - n)
                            if dSlice.stop is None:
                                dStop = data.shape[dynAxis]
                            else:
                                dStop = min(data.shape[dynAxis], dSlice.stop - n)
                            newSubset = list(subset[:])
                            newSubset[dynAxis] = slice(dStart, dStop)
                            if dStop > dStart:
                                frames.append(data[tuple(newSubset)].copy())
                        else:
                            frames.append(data)
                n += inf['numFrames']
                if 'xVals' in inf:
                    xVals.extend(inf['xVals'])

            subarr = np.concatenate(frames, axis=dynAxis)
            if len(xVals) > 0:
                ax['values'] = np.array(xVals, dtype=(ax['values_type']))
            del ax['values_len']
            del ax['values_type']
        self._info = meta['info']
        self._data = subarr

    def _readHDF5(self, fileName, readAllData=None, writable=False, **kargs):
        if 'close' in kargs:
            if readAllData is None:
                readAllData = kargs['close']
            elif readAllData is True:
                if writable is True:
                    raise Exception('Incompatible arguments: readAllData=True and writable=True')
                elif not HAVE_HDF5:
                    try:
                        assert writable == False
                        assert readAllData != False
                        self._readHDF5Remote(fileName)
                        return
                    except:
                        raise Exception("The file '%s' is HDF5-formatted, but the HDF5 library (h5py) was not found." % fileName)

                if readAllData is None:
                    size = os.stat(fileName).st_size
                    readAllData = size < 500000000.0
                if writable is True:
                    mode = 'r+'
            else:
                mode = 'r'
            f = h5py.File(fileName, mode)
            ver = f.attrs['MetaArray']
            if ver > MetaArray.version:
                print('Warning: This file was written with MetaArray version %s, but you are using version %s. (Will attempt to read anyway)' % (str(ver), str(MetaArray.version)))
            meta = MetaArray.readHDF5Meta(f['info'])
            self._info = meta
            self._data = writable or readAllData or f['data']
            self._openFile = f
        else:
            self._data = f['data'][:]
            f.close()

    def _readHDF5Remote(self, fileName):
        proc = getattr(MetaArray, '_hdf5Process', None)
        if proc == False:
            raise Exception('remote read failed')
        if proc == None:
            from .. import multiprocess as mp
            proc = mp.Process(executable='/usr/bin/python')
            proc.setProxyOptions(deferGetattr=True)
            MetaArray._hdf5Process = proc
            MetaArray._h5py_metaarray = proc._import('pyqtgraph.metaarray')
        ma = MetaArray._h5py_metaarray.MetaArray(file=fileName)
        self._data = ma.asarray()._getValue()
        self._info = ma._info._getValue()

    @staticmethod
    def mapHDF5Array(data, writable=False):
        off = data.id.get_offset()
        if writable:
            mode = 'r+'
        else:
            mode = 'r'
        if off is None:
            raise Exception('This dataset uses chunked storage; it can not be memory-mapped. (store using mappable=True)')
        return np.memmap(filename=(data.file.filename), offset=off, dtype=(data.dtype), shape=(data.shape), mode=mode)

    @staticmethod
    def readHDF5Meta(root, mmap=False):
        data = {}
        for k in root.attrs:
            val = root.attrs[k]
            if isinstance(val, basestring):
                try:
                    val = eval(val)
                except:
                    raise Exception('Can not evaluate string: "%s"' % val)

            data[k] = val

        for k in root:
            obj = root[k]
            if isinstance(obj, h5py.highlevel.Group):
                val = MetaArray.readHDF5Meta(obj)
            else:
                if isinstance(obj, h5py.highlevel.Dataset):
                    if mmap:
                        val = MetaArray.mapHDF5Array(obj)
                    else:
                        val = obj[:]
                else:
                    raise Exception("Don't know what to do with type '%s'" % str(type(obj)))
            data[k] = val

        typ = root.attrs['_metaType_']
        del data['_metaType_']
        if typ == 'dict':
            return data
        if typ == 'list' or typ == 'tuple':
            d2 = [
             None] * len(data)
            for k in data:
                d2[int(k)] = data[k]

            if typ == 'tuple':
                d2 = tuple(d2)
            return d2
        raise Exception("Don't understand metaType '%s'" % typ)

    def write(self, fileName, **opts):
        """Write this object to a file. The object can be restored by calling MetaArray(file=fileName)
        opts:
            appendAxis: the name (or index) of the appendable axis. Allows the array to grow.
            compression: None, 'gzip' (good compression), 'lzf' (fast compression), etc.
            chunks: bool or tuple specifying chunk shape
        """
        if USE_HDF5:
            if HAVE_HDF5:
                return (self.writeHDF5)(fileName, **opts)
        return (self.writeMa)(fileName, **opts)

    def writeMeta(self, fileName):
        """Used to re-write meta info to the given file.
        This feature is only available for HDF5 files."""
        f = h5py.File(fileName, 'r+')
        if f.attrs['MetaArray'] != MetaArray.version:
            raise Exception('The file %s was created with a different version of MetaArray. Will not modify.' % fileName)
        del f['info']
        self.writeHDF5Meta(f, 'info', self._info)
        f.close()

    def writeHDF5(self, fileName, **opts):
        comp = self.defaultCompression
        if isinstance(comp, tuple):
            comp, copts = comp
        else:
            copts = None
        dsOpts = {'compression':comp, 
         'chunks':True}
        if copts is not None:
            dsOpts['compression_opts'] = copts
        else:
            appAxis = opts.get('appendAxis', None)
            if appAxis is not None:
                appAxis = self._interpretAxis(appAxis)
                cs = [min(100000, x) for x in self.shape]
                cs[appAxis] = 1
                dsOpts['chunks'] = tuple(cs)
            else:
                cs = [min(100000, x) for x in self.shape]
                for i in range(self.ndim):
                    if 'cols' in self._info[i]:
                        cs[i] = 1

                dsOpts['chunks'] = tuple(cs)
            for k in dsOpts:
                if k in opts:
                    dsOpts[k] = opts[k]

            if opts.get('mappable', False):
                dsOpts = {'chunks':None,  'compression':None}
            append = False
            if appAxis is not None:
                maxShape = list(self.shape)
                ax = self._interpretAxis(appAxis)
                maxShape[ax] = None
                if os.path.exists(fileName):
                    append = True
                dsOpts['maxshape'] = tuple(maxShape)
            else:
                dsOpts['maxshape'] = None
        if append:
            f = h5py.File(fileName, 'r+')
            if f.attrs['MetaArray'] != MetaArray.version:
                raise Exception('The file %s was created with a different version of MetaArray. Will not modify.' % fileName)
            data = f['data']
            shape = list(data.shape)
            shape[ax] += self.shape[ax]
            data.resize(tuple(shape))
            sl = [slice(None)] * len(data.shape)
            sl[ax] = slice(-self.shape[ax], None)
            data[tuple(sl)] = self.view(np.ndarray)
            axInfo = f['info'][str(ax)]
            if 'values' in axInfo:
                v = axInfo['values']
                v2 = self._info[ax]['values']
                shape = list(v.shape)
                shape[0] += v2.shape[0]
                v.resize(shape)
                v[-v2.shape[0]:] = v2
            f.close()
        else:
            f = h5py.File(fileName, 'w')
            f.attrs['MetaArray'] = MetaArray.version
            (f.create_dataset)('data', data=self.view(np.ndarray), **dsOpts)
            if isinstance(dsOpts['chunks'], tuple):
                dsOpts['chunks'] = True
                if 'maxshape' in dsOpts:
                    del dsOpts['maxshape']
            (self.writeHDF5Meta)(f, 'info', (self._info), **dsOpts)
            f.close()

    def writeHDF5Meta--- This code section failed: ---

 L.1143         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              np
                6  LOAD_ATTR                ndarray
                8  CALL_FUNCTION_2       2  '2 positional arguments'
               10  POP_JUMP_IF_FALSE    60  'to 60'

 L.1144        12  LOAD_CONST               (None,)
               14  LOAD_FAST                'data'
               16  LOAD_ATTR                shape
               18  LOAD_CONST               1
               20  LOAD_CONST               None
               22  BUILD_SLICE_2         2 
               24  BINARY_SUBSCR    
               26  BINARY_ADD       
               28  LOAD_FAST                'dsOpts'
               30  LOAD_STR                 'maxshape'
               32  STORE_SUBSCR     

 L.1145        34  LOAD_FAST                'root'
               36  LOAD_ATTR                create_dataset
               38  LOAD_FAST                'name'
               40  BUILD_TUPLE_1         1 
               42  LOAD_STR                 'data'
               44  LOAD_FAST                'data'
               46  BUILD_MAP_1           1 
               48  LOAD_FAST                'dsOpts'
               50  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               52  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               54  POP_TOP          
            56_58  JUMP_FORWARD        370  'to 370'
             60_0  COME_FROM            10  '10'

 L.1146        60  LOAD_GLOBAL              isinstance
               62  LOAD_FAST                'data'
               64  LOAD_GLOBAL              list
               66  CALL_FUNCTION_2       2  '2 positional arguments'
               68  POP_JUMP_IF_TRUE     80  'to 80'
               70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'data'
               74  LOAD_GLOBAL              tuple
               76  CALL_FUNCTION_2       2  '2 positional arguments'
               78  POP_JUMP_IF_FALSE   172  'to 172'
             80_0  COME_FROM            68  '68'

 L.1147        80  LOAD_FAST                'root'
               82  LOAD_METHOD              create_group
               84  LOAD_FAST                'name'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'gr'

 L.1148        90  LOAD_GLOBAL              isinstance
               92  LOAD_FAST                'data'
               94  LOAD_GLOBAL              list
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_JUMP_IF_FALSE   112  'to 112'

 L.1149       100  LOAD_STR                 'list'
              102  LOAD_FAST                'gr'
              104  LOAD_ATTR                attrs
              106  LOAD_STR                 '_metaType_'
              108  STORE_SUBSCR     
              110  JUMP_FORWARD        122  'to 122'
            112_0  COME_FROM            98  '98'

 L.1151       112  LOAD_STR                 'tuple'
              114  LOAD_FAST                'gr'
              116  LOAD_ATTR                attrs
              118  LOAD_STR                 '_metaType_'
              120  STORE_SUBSCR     
            122_0  COME_FROM           110  '110'

 L.1153       122  SETUP_LOOP          370  'to 370'
              124  LOAD_GLOBAL              range
              126  LOAD_GLOBAL              len
              128  LOAD_FAST                'data'
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  GET_ITER         
              136  FOR_ITER            168  'to 168'
              138  STORE_FAST               'i'

 L.1154       140  LOAD_FAST                'self'
              142  LOAD_ATTR                writeHDF5Meta
              144  LOAD_FAST                'gr'
              146  LOAD_GLOBAL              str
              148  LOAD_FAST                'i'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  LOAD_FAST                'data'
              154  LOAD_FAST                'i'
              156  BINARY_SUBSCR    
              158  BUILD_TUPLE_3         3 
              160  LOAD_FAST                'dsOpts'
              162  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              164  POP_TOP          
              166  JUMP_BACK           136  'to 136'
              168  POP_BLOCK        
              170  JUMP_FORWARD        370  'to 370'
            172_0  COME_FROM            78  '78'

 L.1155       172  LOAD_GLOBAL              isinstance
              174  LOAD_FAST                'data'
              176  LOAD_GLOBAL              dict
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  POP_JUMP_IF_FALSE   244  'to 244'

 L.1156       182  LOAD_FAST                'root'
              184  LOAD_METHOD              create_group
              186  LOAD_FAST                'name'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  STORE_FAST               'gr'

 L.1157       192  LOAD_STR                 'dict'
              194  LOAD_FAST                'gr'
              196  LOAD_ATTR                attrs
              198  LOAD_STR                 '_metaType_'
              200  STORE_SUBSCR     

 L.1158       202  SETUP_LOOP          370  'to 370'
              204  LOAD_FAST                'data'
              206  LOAD_METHOD              items
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  GET_ITER         
              212  FOR_ITER            240  'to 240'
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'k'
              218  STORE_FAST               'v'

 L.1159       220  LOAD_FAST                'self'
              222  LOAD_ATTR                writeHDF5Meta
              224  LOAD_FAST                'gr'
              226  LOAD_FAST                'k'
              228  LOAD_FAST                'v'
              230  BUILD_TUPLE_3         3 
              232  LOAD_FAST                'dsOpts'
              234  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              236  POP_TOP          
              238  JUMP_BACK           212  'to 212'
              240  POP_BLOCK        
              242  JUMP_FORWARD        370  'to 370'
            244_0  COME_FROM           180  '180'

 L.1160       244  LOAD_GLOBAL              isinstance
              246  LOAD_FAST                'data'
              248  LOAD_GLOBAL              int
              250  CALL_FUNCTION_2       2  '2 positional arguments'
          252_254  POP_JUMP_IF_TRUE    296  'to 296'
              256  LOAD_GLOBAL              isinstance
              258  LOAD_FAST                'data'
              260  LOAD_GLOBAL              float
              262  CALL_FUNCTION_2       2  '2 positional arguments'
          264_266  POP_JUMP_IF_TRUE    296  'to 296'
              268  LOAD_GLOBAL              isinstance
              270  LOAD_FAST                'data'
              272  LOAD_GLOBAL              np
              274  LOAD_ATTR                integer
              276  CALL_FUNCTION_2       2  '2 positional arguments'
          278_280  POP_JUMP_IF_TRUE    296  'to 296'
              282  LOAD_GLOBAL              isinstance
              284  LOAD_FAST                'data'
              286  LOAD_GLOBAL              np
              288  LOAD_ATTR                floating
              290  CALL_FUNCTION_2       2  '2 positional arguments'
          292_294  POP_JUMP_IF_FALSE   308  'to 308'
            296_0  COME_FROM           278  '278'
            296_1  COME_FROM           264  '264'
            296_2  COME_FROM           252  '252'

 L.1161       296  LOAD_FAST                'data'
              298  LOAD_FAST                'root'
              300  LOAD_ATTR                attrs
              302  LOAD_FAST                'name'
              304  STORE_SUBSCR     
              306  JUMP_FORWARD        370  'to 370'
            308_0  COME_FROM           292  '292'

 L.1163       308  SETUP_EXCEPT        328  'to 328'

 L.1164       310  LOAD_GLOBAL              repr
              312  LOAD_FAST                'data'
              314  CALL_FUNCTION_1       1  '1 positional argument'
              316  LOAD_FAST                'root'
              318  LOAD_ATTR                attrs
              320  LOAD_FAST                'name'
              322  STORE_SUBSCR     
              324  POP_BLOCK        
              326  JUMP_FORWARD        370  'to 370'
            328_0  COME_FROM_EXCEPT    308  '308'

 L.1165       328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          

 L.1166       334  LOAD_GLOBAL              print
              336  LOAD_STR                 "Can not store meta data of type '%s' in HDF5. (key is '%s')"
              338  LOAD_GLOBAL              str
              340  LOAD_GLOBAL              type
              342  LOAD_FAST                'data'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  LOAD_GLOBAL              str
              350  LOAD_FAST                'name'
              352  CALL_FUNCTION_1       1  '1 positional argument'
              354  BUILD_TUPLE_2         2 
              356  BINARY_MODULO    
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  POP_TOP          

 L.1167       362  RAISE_VARARGS_0       0  'reraise'
              364  POP_EXCEPT       
              366  JUMP_FORWARD        370  'to 370'
              368  END_FINALLY      
            370_0  COME_FROM           366  '366'
            370_1  COME_FROM           326  '326'
            370_2  COME_FROM           306  '306'
            370_3  COME_FROM           242  '242'
            370_4  COME_FROM_LOOP      202  '202'
            370_5  COME_FROM           170  '170'
            370_6  COME_FROM_LOOP      122  '122'
            370_7  COME_FROM            56  '56'

Parse error at or near `JUMP_FORWARD' instruction at offset 306

    def writeMa(self, fileName, appendAxis=None, newFile=False):
        """Write an old-style .ma file"""
        meta = {'shape':self.shape, 
         'type':str(self.dtype),  'info':self.infoCopy(),  'version':MetaArray.version}
        axstrs = []
        if appendAxis is not None:
            if MetaArray.isNameType(appendAxis):
                appendAxis = self._interpretAxis(appendAxis)
            else:
                ax = meta['info'][appendAxis]
                ax['values_len'] = 'dynamic'
                if 'values' in ax:
                    ax['values_type'] = str(ax['values'].dtype)
                    dynXVals = ax['values']
                    del ax['values']
                else:
                    dynXVals = None
        else:
            for ax in meta['info']:
                if 'values' in ax:
                    axstrs.append(ax['values'].tostring())
                    ax['values_len'] = len(axstrs[(-1)])
                    ax['values_type'] = str(ax['values'].dtype)
                    del ax['values']

            if not newFile:
                newFile = not os.path.exists(fileName) or os.stat(fileName).st_size == 0
            if appendAxis is None or newFile:
                fd = open(fileName, 'wb')
                fd.write(str(meta) + '\n\n')
                for ax in axstrs:
                    fd.write(ax)

            else:
                fd = open(fileName, 'ab')
            if self.dtype != object:
                dataStr = self.view(np.ndarray).tostring()
            else:
                dataStr = pickle.dumps(self.view(np.ndarray))
        if appendAxis is not None:
            frameInfo = {'len':len(dataStr), 
             'numFrames':self.shape[appendAxis]}
            if dynXVals is not None:
                frameInfo['xVals'] = list(dynXVals)
            fd.write('\n' + str(frameInfo) + '\n')
        fd.write(dataStr)
        fd.close()

    def writeCsv(self, fileName=None):
        """Write 2D array to CSV file or return the string if no filename is given"""
        if self.ndim > 2:
            raise Exception('CSV Export is only for 2D arrays')
        else:
            if fileName is not None:
                file = open(fileName, 'w')
            else:
                ret = ''
                if 'cols' in self._info[0]:
                    s = ','.join([x['name'] for x in self._info[0]['cols']]) + '\n'
                    if fileName is not None:
                        file.write(s)
                    else:
                        ret += s
            for row in range(0, self.shape[1]):
                s = ','.join(['%g' % x for x in self[:, row]]) + '\n'
                if fileName is not None:
                    file.write(s)
                else:
                    ret += s

            if fileName is not None:
                file.close()
            else:
                return ret


if __name__ == '__main__':
    arr = np.zeros((2, 5, 3, 5), dtype=int)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(arr.shape[2]):
                for l in range(arr.shape[3]):
                    arr[(i, j, k, l)] = (i + 1) * 1000 + (j + 1) * 100 + (k + 1) * 10 + (l + 1)

    info = [
     axis('Axis1'),
     axis('Axis2', values=[1, 2, 3, 4, 5]),
     axis('Axis3', cols=[
      'Ax3Col1',
      ('Ax3Col2', 'mV', 'Axis3 Column2'),
      (('Ax3', 'Col3'), 'A', 'Axis3 Column3')]),
     {'name':'Axis4', 
      'values':np.array([1.1, 1.2, 1.3, 1.4, 1.5]),  'units':'s'},
     {'extra': 'info'}]
    ma = MetaArray(arr, info=info)
    print('====  Original Array =======')
    print(ma)
    print('\n\n')
    print('\n -- normal integer indexing\n')
    print('\n  ma[1]')
    print(ma[1])
    print('\n  ma[1, 2:4]')
    print(ma[1, 2:4])
    print('\n  ma[1, 1:5:2]')
    print(ma[1, 1:5:2])
    print('\n -- named axis indexing\n')
    print("\n  ma['Axis2':3]")
    print(ma['Axis2':3])
    print("\n  ma['Axis2':3:5]")
    print(ma['Axis2':3:5])
    print("\n  ma[1, 'Axis2':3]")
    print(ma[1, 'Axis2':3])
    print("\n  ma[:, 'Axis2':3]")
    print(ma[:, 'Axis2':3])
    print("\n  ma['Axis2':3, 'Axis4':0:2]")
    print(ma['Axis2':3, 'Axis4':0:2])
    print('\n -- column name indexing\n')
    print("\n  ma['Axis3':'Ax3Col1']")
    print(ma['Axis3':'Ax3Col1'])
    print("\n  ma['Axis3':('Ax3','Col3')]")
    print(ma['Axis3':('Ax3', 'Col3')])
    print("\n  ma[:, :, 'Ax3Col2']")
    print(ma[:, :, 'Ax3Col2'])
    print("\n  ma[:, :, ('Ax3','Col3')]")
    print(ma[:, :, ('Ax3', 'Col3')])
    print('\n -- axis value range indexing\n')
    print("\n  ma['Axis2':1.5:4.5]")
    print(ma['Axis2':1.5:4.5])
    print("\n  ma['Axis4':1.15:1.45]")
    print(ma['Axis4':1.15:1.45])
    print("\n  ma['Axis4':1.15:1.25]")
    print(ma['Axis4':1.15:1.25])
    print('\n -- list indexing\n')
    print('\n  ma[:, [0,2,4]]')
    print(ma[:, [0, 2, 4]])
    print("\n  ma['Axis4':[0,2,4]]")
    print(ma['Axis4':[0, 2, 4]])
    print("\n  ma['Axis3':[0, ('Ax3','Col3')]]")
    print(ma['Axis3':[0, ('Ax3', 'Col3')]])
    print('\n -- boolean indexing\n')
    print('\n  ma[:, array([True, True, False, True, False])]')
    print(ma[:, np.array([True, True, False, True, False])])
    print("\n  ma['Axis4':array([True, False, False, False])]")
    print(ma['Axis4':np.array([True, False, False, False])])
    print('\n================  File I/O Tests  ===================\n')
    import tempfile
    tf = tempfile.mktemp()
    tf = 'test.ma'
    print('\n  -- write/read test')
    ma.write(tf)
    ma2 = MetaArray(file=tf)
    print('\nArrays are equivalent:', (ma == ma2).all())
    os.remove(tf)
    print('\n================append test (%s)===============' % tf)
    ma['Axis2':0:2].write(tf, appendAxis='Axis2')
    for i in range(2, ma.shape[1]):
        ma['Axis2':[i]].write(tf, appendAxis='Axis2')

    ma2 = MetaArray(file=tf)
    print('\nArrays are equivalent:', (ma == ma2).all())
    os.remove(tf)
    print('\n==========Memmap test============')
    ma.write(tf, mappable=True)
    ma2 = MetaArray(file=tf, mmap=True)
    print('\nArrays are equivalent:', (ma == ma2).all())
    os.remove(tf)