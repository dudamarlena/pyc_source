# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pup.py
# Compiled at: 2013-12-05 12:50:56
from datetime import datetime
import numpy

class Dimension(object):

    def __init__(self, length):
        self.length = length


class Variable(object):

    def __init__(self, data, dimensions=None, record=False, **kwargs):
        if isinstance(data, basestring):
            data = list(data)
        missing_value = kwargs.get('missing_value') or kwargs.get('_FillValue') or getattr(data, 'fill_value', None)
        if missing_value is not None:
            kwargs.setdefault('missing_value', missing_value)
            kwargs.setdefault('_FillValue', missing_value)
            self.data = numpy.ma.asarray(data).filled(missing_value)
        else:
            self.data = numpy.asarray(data)
        self.dimensions = dimensions
        self.record = record
        self.attributes = kwargs
        return


class Group(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class NetCDF(object):

    @classmethod
    def save(klass, filename, **kwargs):
        if hasattr(klass, 'loader') and callable(getattr(klass, 'loader')):
            loader = getattr(klass, 'loader')
        else:
            from pupynere import netcdf_file as loader
        out = loader(filename, 'w', **kwargs)
        process(klass, out)
        out.close()


def format(attr):
    if isinstance(attr, (tuple, list)):
        return map(format, attr)
    else:
        return str(attr)


def process(obj, target):
    for name in dir(obj):
        attr = getattr(obj, name)
        if name.startswith('__') or not isinstance(attr, (tuple, list, basestring)):
            continue
        setattr(target, name, format(attr))

    for name in dir(obj):
        attr = getattr(obj, name)
        if isinstance(attr, (Variable, Dimension)):
            attr.name = name

    for name in dir(obj):
        attr = getattr(obj, name)
        if isinstance(attr, Dimension):
            target.createDimension(name, attr.length)

    for name in dir(obj):
        attr = getattr(obj, name)
        if isinstance(attr, Group):
            group = target.createGroup(name)
            process(attr, group)

    variables = []
    for name in dir(obj):
        attr = getattr(obj, name)
        if isinstance(attr, Variable):
            variables.append(attr)

    variables.sort(key=lambda var: not var.record)
    for variable in variables:
        if variable.dimensions is None:
            variable.dimensions = [
             variable]
        for dim in variable.dimensions:
            if dim.name not in target.dimensions:
                if dim.record:
                    target.createDimension(dim.name, None)
                else:
                    target.createDimension(dim.name, len(dim.data))

        if variable.data.dtype == numpy.int64:
            variable.data = variable.data.astype(numpy.int32)
        var = target.createVariable(variable.name, variable.data.dtype, tuple(dim.name for dim in variable.dimensions))
        var[:] = variable.data[:]
        for k, v in variable.attributes.items():
            setattr(var, k, v)

    return