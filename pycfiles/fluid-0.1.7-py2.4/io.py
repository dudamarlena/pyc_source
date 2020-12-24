# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fluid/io.py
# Compiled at: 2006-12-04 09:19:16
"""Input/output routines.
"""
__version__ = '$Revision: 14 $'
import re, numarray, pycdf, matfile
from fluid import dtypes
import opendap.client, opendap.exceptions

class FileError(opendap.exceptions.DODSError):
    __module__ = __name__


class UnknownTypeError(opendap.exceptions.DODSError):
    __module__ = __name__


def open(filename):
    """Generic open function.
    
    This function is a generic open that can handle NetCDF files, Matlab
    files or DODS servers. It returns a Pydods DatasetType object.
    """
    matches = [
     (
      '^(http|https)://', _open_dods), ('\\.(nc|NC|cdf|CDF)$', _open_netcdf), ('\\.(mat|MAT)$', _open_matlab)]
    for (pattern, func) in matches:
        if re.search(pattern, filename):
            return func(filename)

    raise UnknownTypeError, "I don't know how to open %s." % filename


def save(filename, *args):
    """Generic save funcion.

    This function is a generic save function. For now it an only handle
    saving to NetCDF files.
    """
    matches = [
     (
      '\\.(nc|NC|cdf|CDF)$', _save_netcdf)]
    for (pattern, func) in matches:
        if re.search(pattern, filename):
            return func(filename, *args)

    raise UnknownTypeError, "i don't know how to save to %s." % filename


def _open_matlab(filename):
    typeconvert = {'1': 'Byte', 's': 'Int16', 'i': 'Int32', 'l': 'Int32', 'b': 'Uint16', 'w': 'Uint16', 'u': 'Uint32', 'f': 'Float32', 'd': 'Float64', 'c': 'String'}
    try:
        f = matfile.load(filename)
    except:
        raise FileError, 'Unable to open file %s' % filename

    dataset = dtypes.DatasetType()
    dataset.attributes = {'filename': filename}
    for (k, v) in f.items():
        if k.startswith('__'):
            k = k.replace('__', '')
            dataset.attributes[k] = v
        else:
            dataset[k] = dtypes.ArrayType()
            dataset[k].name = k
            dataset[k].data = v
            dataset[k].attributes = {}
            dataset[k].shape = v.shape
            dataset[k].type = typeconvert[v.typecode()]
            dataset[k].dimensions = tuple([ 'x%d' % i for (i, s) in enumerate(v.shape) ])

    return dataset


def _open_dods(url):
    return opendap.client.Dataset(url)


def _open_netcdf(filename):
    typeconvert = (None, 'Byte', 'String', 'Int16', 'Int32', 'Float32', 'Float64')
    try:
        try:
            f = pycdf.CDF(filename)
        except:
            raise FileError, 'Unable to open file %s' % filename

        dataset = dtypes.DatasetType()
        dataset.attributes = f.attributes()
        grids = [ grid for grid in f.variables().keys() if grid not in f.dimensions().keys() ]
        for grid in grids:
            dataset[grid] = dtypes.GridType()
            G = dataset[grid]
            G.name = grid
            G.array = dtypes.ArrayType()
            G.array.name = grid
            G.array.type = typeconvert[f.var(grid).inq_type()]
            G.array.dimensions = f.var(grid).dimensions()
            G.array.shape = f.var(grid).shape()
            G.array.attributes = f.var(grid).attributes()
            G.array.data = numarray.array(f.var(grid)[:])
            G.maps = {}
            for map_ in G.array.dimensions:
                G.maps[map_] = dtypes.ArrayType()
                G.maps[map_].name = map_
                G.maps[map_].type = typeconvert[f.var(map_).inq_type()]
                G.maps[map_].dimensions = f.var(map_).dimensions()
                G.maps[map_].shape = f.var(map_).shape()
                G.maps[map_].attributes = f.var(map_).attributes()
                G.maps[map_].data = numarray.array(f.var(map_)[:])
                dataset[map_] = G.maps[map_]

    finally:
        f.close()
    return dataset


def _save_netcdf(filename, *args):
    dataset = dtypes.DatasetType()
    dataset.attributes = {}
    for arg in args:
        if isinstance(arg, dtypes.DatasetType):
            dataset.update(arg)
            dataset.attributes.update(arg.attributes)
        elif isinstance(arg, dtypes.BaseType):
            dataset[arg.name] = arg
        else:
            raise UnknownTypeError, '%s is not a valid object.' % arg

    try:
        try:
            f = pycdf.CDF(filename, pycdf.NC.WRITE | pycdf.NC.CREATE)
        except:
            raise FileError, 'Unable to open file %s' % filename

        f.automode()
        for (k, v) in dataset.attributes.items():
            setattr(f, k, v)

        typeconvert = {'Byte': pycdf.NC.BYTE, 'String': pycdf.NC.CHAR, 'Int16': pycdf.NC.SHORT, 'Int32': pycdf.NC.INT, 'Float32': pycdf.NC.FLOAT, 'Float64': pycdf.NC.DOUBLE}
        for var in dataset.values():
            dims = []
            for (dim, shape) in zip(var.dimensions, var.shape):
                if not f.dimensions().has_key(dim):
                    dims.append(f.def_dim(dim, shape))
                else:
                    dims.append(f.dim(dim))

            outvar = f.def_var(var.name, typeconvert[var.type], tuple(dims))
            outvar[:] = var.data[:]
            for (k, v) in var.attributes.items():
                setattr(outvar, k, v)

    finally:
        f.close()