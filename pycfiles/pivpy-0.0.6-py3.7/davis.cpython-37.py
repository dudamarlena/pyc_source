# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pivpy/davis.py
# Compiled at: 2019-11-29 15:27:31
# Size of source mod 2**32: 5718 bytes
"""
Created on Tue Jul 23 19:33:20 2019

@author: lior
"""
import numpy as np, xarray as xr, os, re, ReadIM

def ReadDavis(path, time=0):
    """
    input path for files format from davis tested for im7&vc7
    out put [X Y U V mask]
    valid only for 2d piv cases
    RETURN:   
     in case of images (image type=0):
              X = scaled x-coordinates
              Y = scaled y-coordinates      
              U = scaled image intensities
              v=0
              MASK=0
            in case of 2D vector fields (A.IType = 1,2 or 3):
              X = scaled x-coordinates
               Y = scaled y-coordinates
               U = scaled vx-components of vectors
               V = scaled vy-components of vectors

    """
    buff, vatts = ReadIM.extra.get_Buffer_andAttributeList(path)
    v_array, buff1 = ReadIM.extra.buffer_as_array(buff)
    nx = buff.nx
    nz = buff.nz
    ny = buff.ny
    baseRangeX = np.arange(nx)
    baseRangeY = np.arange(ny)
    baseRangeZ = np.arange(nz)
    lhs1 = (baseRangeX + 0.5) * buff.vectorGrid * buff.scaleX.factor + buff.scaleX.offset
    lhs2 = (baseRangeY + 0.5) * buff.vectorGrid * buff.scaleY.factor + buff.scaleY.offset
    lhs3 = 0
    lhs4 = 0
    mask = 0
    if buff.image_sub_type <= 0:
        lhs3 = v_array[0, :, :]
        lhs4 = v_array[1, :, :]
        Im = xr.DataArray(v_array, dims=('frame', 'z', 'x'), coords={'x':lhs1[0, :],  'z':lhs2[:, 0],  'frame':[0, 1]})
        data = xr.Dataset({'Im': Im})
    else:
        if buff.image_sub_type == 2:
            lhs1, lhs2 = np.meshgrid(lhs1, lhs2)
            lhs3 = v_array[0, :, :] * buff.scaleI.factor + buff.scaleI.offset
            lhs4 = v_array[1, :, :] * buff.scaleI.factor + buff.scaleI.offset
            if buff.scaleY.factor < 0.0:
                lhs4 = -lhs4
            lhs3 = lhs3[:, :, np.newaxis]
            lhs4 = lhs4[:, :, np.newaxis]
            u = xr.DataArray(lhs3, dims=('z', 'x', 't'), coords={'x':lhs1[0, :],  'z':lhs2[:, 0],  't':[time]})
            v = xr.DataArray(lhs4, dims=('z', 'x', 't'), coords={'x':lhs1[0, :],  'z':lhs2[:, 0],  't':[time]})
            data = xr.Dataset({'u':u,  'v':v})
        else:
            if buff.image_sub_type == 3 or buff.image_sub_type == 1:
                lhs1, lhs2 = np.meshgrid(lhs1, lhs2)
                lhs3 = lhs1 * 0
                lhs4 = lhs2 * 0
                maskData = v_array[0, :, :]
                for i in range(5):
                    mask = maskData == i + 1
                    if i < 4:
                        dat = v_array[2 * i + 1, :, :]
                        lhs3[mask] = dat[mask]
                        dat = v_array[2 * i + 2, :, :]
                        lhs4[mask] = dat[mask]
                    else:
                        dat = v_array[7, :, :]
                        lhs3[mask] = dat[mask]
                        dat = v_array[8, :, :]
                        lhs4[mask] = dat[mask]

                lhs3 = lhs3 * buff.scaleI.factor + buff.scaleI.offset
                lhs4 = lhs4 * buff.scaleI.factor + buff.scaleI.offset
                if buff.scaleY.factor < 0.0:
                    lhs4 = -1 * lhs4
                mask = maskData == 0
                lhs3 = lhs3[:, :, np.newaxis]
                lhs4 = lhs4[:, :, np.newaxis]
                maskData = maskData[:, :, np.newaxis]
                u = xr.DataArray(lhs3, dims=('z', 'x', 't'), coords={'x':lhs1[0, :],  'z':lhs2[:, 0],  't':[time]})
                v = xr.DataArray(lhs4, dims=('z', 'x', 't'), coords={'x':lhs1[0, :],  'z':lhs2[:, 0],  't':[time]})
                chc = xr.DataArray(maskData, dims=('z', 'x', 't'), coords={'x':lhs1[0, :],  'z':lhs2[:, 0],  't':[time]})
                data = xr.Dataset({'u':u,  'v':v,  'chc':chc})
            data.attrs['Info'] = ReadIM.extra.att2dict(vatts)
            ReadIM.DestroyBuffer(buff1)
            del buff1
            ReadIM.DestroyBuffer(buff)
            del buff
            ReadIM.DestroyAttributeListSafe(vatts)
            del vatts
            return data


def load_directory(path, basename=''):
    """ 
    load_directory (path)

    Loads all the .VEC files in the directory into a single
    xarray dataset with variables and units added as attributes

    Input: 
        directory : path to the directory with .vec files

    Output:
        data : xarray DataSet with dimensions: x,y,t and 
               data arrays of u,v,
               attributes of variables and units

    See more: loadvec
    """
    files = [f for f in os.listdir(path) if f.endswith('.vc7')]
    variables, units, rows, cols, dt, frame = parse_header(files[0])
    data = []
    for i, f in enumerate(files):
        data.append(loadvec(f, rows, cols, variables, units, dt, frame + i - 1))

    combined = xr.concat(data, dim='t')
    combined.attrs['variables'] = variables
    combined.attrs['units'] = units
    combined.attrs['dt'] = dt
    combined.attrs['files'] = files
    return combined


path = 'C:\\Users\\lior\\Documents\\ibrrTau\\timeDependedVecMaps'
files = [f for f in os.listdir(path) if f.endswith('.vc7')]
data = []
data.append(ReadDavis(path + '\\' + files[(-1)], 1))
data.append(ReadDavis(path + '\\' + files[(-2)], 2))
combined = xr.concat(data, dim='t')