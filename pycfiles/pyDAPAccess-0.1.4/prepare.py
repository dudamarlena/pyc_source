# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pydap/responses/wms/prepare.py
# Compiled at: 2012-11-22 16:51:44
import sys, numpy
from pydap.handlers.netcdf import nc, var_attrs
from pydap.responses.wms import fix_data

def prepare_netcdf():
    filename = sys.argv[1]
    if nc.__module__ == 'pupynere':
        raise Exception, 'Pupynere cannot open netcdf files in append mode. Please install either PyNIO, netCDF4, Scientific.IO.NetCDF or pynetcdf.'
    f = nc(filename, 'a')
    for name, var in f.variables.items():
        if name in f.dimensions or hasattr(var, 'actual_range'):
            continue
        data = fix_data(numpy.asarray(var[:]), var_attrs(var))
        var.actual_range = (numpy.amin(data), numpy.amax(data))

    f.close()