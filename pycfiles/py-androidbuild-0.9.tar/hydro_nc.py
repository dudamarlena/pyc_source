# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/data/hydro_nc.py
# Compiled at: 2016-03-23 12:35:00
import os, glob, inspect, fnmatch, numpy as np, matplotlib.pyplot as plt
from netCDF4 import Dataset as ncfile
try:
    import seawater.gibbs as gsw, seawater.csiro as csw
except ImportError:
    pass

from scipy import interpolate
from warnings import warn
from altimetry.tools import recale_limits, in_limits, cumulative_distance, calcul_distance, where_list, cnes_convert, plot_map, get_caller
from collections import OrderedDict

def load_ncVar(varName, nc=None, **kwargs):
    if nc is None:
        raise Exception('No Netcdf file passed')
    var = nc.variables[varName]
    var.set_auto_maskandscale(False)
    varDim = [ str(dim) for dim in var.dimensions ]
    missDim = len(varDim) == 0
    if missDim:
        warn('No dimension found')
    else:
        varDimval = [ len(nc.dimensions[dimname]) for dimname in varDim ]
    attrStr = var.__dict__
    ind_list = []
    dims = OrderedDict({'_ndims': 0})
    dstr = []
    shape = ()
    for vid, vn in enumerate(varDim):
        if not kwargs.has_key(vn):
            ind_list.append(xrange(varDimval[vid]))
            dims.update({enum[1]: varDimval[enum[0]]})
        else:
            dumind = kwargs[vn]
            if isinstance(dumind, np.ndarray):
                dumind = dumind.tolist()
            if type(dumind) is not list:
                dumind = [dumind]
            ind_list.append(dumind)
            dims.update({vid: len(dumind)})

    sz = [ len(i) for i in ind_list ]
    if not where_list([0], sz)[0] == -1:
        varOut = var[[0]][[]]
    else:
        varOut = var[ind_list]
        if var.shape == (1, 1):
            varOut = varOut.reshape(var.shape)
    if var.__dict__.has_key('_FillValue'):
        mask = varOut == var._FillValue
    elif var.__dict__.has_key('missing_value'):
        mask = varOut == var.missing_value
    else:
        mask = np.zeros(varOut.shape, dtype='bool')
    if var.__dict__.has_key('scale'):
        varOut = varOut * var.scale
    elif var.__dict__.has_key('scale_factor'):
        varOut = varOut * var.scale_factor
    if var.__dict__.has_key('add_offset'):
        varOut = varOut + var.add_offset
    if isinstance(varOut, np.ndarray):
        varOut = np.ma.masked_array(varOut, mask=mask)
    elif isinstance(varOut, np.ma.masked_array):
        var.mask = mask
    else:
        raise ('This data type {} has not been defined - code it!').format(type(varOut))
    attrStr = var.__dict__
    attrStr.pop('_FillValue', None)
    varOut.__dict__.update(attrStr)
    outStr = {'_dimensions': dims, 'data': varOut}
    dims.update({'_ndims': len(dims.keys()[1:])})
    return outStr