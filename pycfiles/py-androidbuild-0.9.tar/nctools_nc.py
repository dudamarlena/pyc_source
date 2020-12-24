# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/tools/nctools_nc.py
# Compiled at: 2016-03-23 12:35:00
__doc__ = '\nNCTOOLS\n@summary: Netcdf data object, to help loading and writing data\n@change Created on 7 sept. 2012\n@author: rdussurg\n'
import numpy as np, matplotlib.pyplot as plt, matplotlib.pylab as pylab
from netCDF4 import Dataset as ncfile
import glob, os
from altimetry.tools import recale, in_limits, where_list, recale_limits, get_caller
from collections import OrderedDict
from warnings import warn

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
            dstr = np.append(dstr, ':')
            sz = np.long(varDimval[vid])
        else:
            drange = kwargs[vn]
            if len(drange) == 2:
                drange = drange + (1, )
            if nc.variables.has_key(vn):
                dumvar = nc.variables[vn][:]
            else:
                dumvar = np.arange(len(nc.dimensions[vn]))
            if vn.startswith('lon'):
                dumvar = recale(dumvar, degrees=True)
            fg = (dumvar >= drange[0]) & (dumvar <= drange[1])
            if fg.sum() == 0:
                dumvar = recale(dumvar, degrees=True)
                drange = tuple(recale(drange, degrees=True).astype(np.long))
                fg = (dumvar >= drange[0]) & (dumvar <= drange[1])
            if fg.sum() == 0:
                raise IndexError(('{0} {1} is not matching given dimensions {2}').format(vn, (np.nanmin(nc.variables[vn][:]), np.nanmax(nc.variables[vn][:])), drange))
            if len(fg) == 1:
                dstr = np.append(dstr, ':')
                sz = 1
            elif len(fg) == 0:
                sz = 0
            else:
                dumind = np.arange(varDimval[vid]).compress(fg)
                bg = dumind[0]
                en = dumind[(-1)] + 1
                st = drange[2]
                dstr = np.append(dstr, ('{0}:{1}:{2}').format(bg, en, st))
                sz = np.long(np.mod(np.float(en - bg - 1) / st, np.float(en - bg)) + 1.0)
        dims.update({vn: sz})
        shape = shape + (sz,)

    sz = [ len(i) for i in ind_list ]
    dstr = (',').join(dstr)
    if missDim:
        cmd = 'varOut = var[:]'
    else:
        cmd = ('varOut = var[{0}]').format(dstr)
    exec cmd
    if var.__dict__.has_key('_FillValue'):
        fill_value = var._FillValue
        mask = varOut == var._FillValue
    elif var.__dict__.has_key('missing_value'):
        fill_value = var._FillValue
        mask = varOut == var._FillValue
    else:
        fill_value = None
        mask = np.zeros(varOut.shape, dtype='bool')
    if var.__dict__.has_key('scale'):
        varOut = varOut * var.scale
    else:
        if var.__dict__.has_key('scale_factor'):
            varOut = varOut * var.scale_factor
        if var.__dict__.has_key('add_offset'):
            varOut = varOut + var.add_offset
        if isinstance(varOut, np.ndarray):
            varOut = np.ma.masked_array(varOut, mask=mask, dtype=varOut.dtype, fill_value=fill_value)
        elif isinstance(varOut, np.ma.masked_array):
            var.mask = mask
        else:
            raise ('This data type {} has not been defined - code it!').format(type(varOut))
        varOut.data[varOut.mask] = varOut.fill_value
        if not missDim:
            varOut = np.transpose(varOut, tuple(range(len(dims.keys()[1:]))[::-1]))
        dims.update({'_ndims': len(dims.keys()[1:])})
        outStr = {'_dimensions': dims, 'data': varOut}
        for A in var.__dict__.keys():
            outStr[A] = var.getncattr(A)

    return outStr