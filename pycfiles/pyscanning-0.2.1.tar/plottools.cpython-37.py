# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gmartine/pyscannerbit/pyscannerbit/plottools.py
# Compiled at: 2020-03-04 01:47:30
# Size of source mod 2**32: 17256 bytes
import numpy as np, h5py, time, csv, os, subprocess as sp, array, re, unicodedata, operator, shlex
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import matplotlib as mpl
import scipy.stats as sps
from itertools import groupby
from operator import itemgetter
font = {'family':'serif', 
 'weight':'normal', 
 'size':16}
(mpl.rc)(*('font', ), **font)

def unicode2ascii(string):
    try:
        outstr = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
    except TypeError:
        outstr = string

    return outstr


def column(matrix, i):
    return [row[i] for row in matrix]


from math import floor, log10

def un2str(x, xe, precision=2):
    """pretty print nominal value and uncertainty

    x  - nominal value
    xe - uncertainty
    precision - number of significant digits in uncertainty

    returns shortest string representation of `x +- xe` either as
        x.xx(ee)e+xx
    or as
        xxx.xx(ee)"""
    try:
        x_exp = int(floor(log10(x)))
    except ValueError:
        x_exp = -int(floor(log10(-x)))

    try:
        xe_exp = int(floor(log10(xe)))
    except ValueError:
        xe_exp = -int(floor(log10(-xe)))

    un_exp = xe_exp - precision + 1
    un_int = round(xe * 10 ** (-un_exp))
    no_exp = un_exp
    no_int = round(x * 10 ** (-no_exp))
    fieldw = -x_exp - no_exp
    fmt = '%%.%df' % fieldw
    result1 = (fmt + '(%.0f)e%d') % (no_int * 10 ** (-fieldw), un_int, x_exp)
    fieldw = max(0, -no_exp)
    fmt = '%%.%df' % fieldw
    result2 = (fmt + '(%.0f)') % (no_int * 10 ** no_exp, un_int * 10 ** max(0, un_exp))
    if len(result2) <= len(result1):
        return result2
    return result1


CLs = [
 0.68, 0.95]
df = 2
rellevels = [sps.chi2.isf(1 - CL, df) for CL in CLs]
mn = 0
mx = 5
s0 = 0.0 / (mx - mn)
s1 = 1.0 / (mx - mn)
s2 = 2.0 / (mx - mn)
s3 = 3.0 / (mx - mn)
s4 = 4.0 / (mx - mn)
s5 = 5.0 / (mx - mn)
cdict = {'red':(
  (
   s0, 0.0, 0.0), (s1, 1.0, 1.0), (s2, 1.0, 1.0), (s3, 1.0, 1.0), (s4, 0.5, 0.5), (s5, 0.2, 0.2)), 
 'green':(
  (
   s0, 1.0, 1.0), (s1, 1.0, 1.0), (s2, 0.5, 0.5), (s3, 0.0, 0.0), (s4, 0.0, 0.0), (s5, 0.0, 0.0)), 
 'blue':(
  (
   s0, 0.0, 0.0), (s1, 0.0, 0.0), (s2, 0.0, 0.0), (s3, 0.0, 0.0), (s4, 0.0, 0.0), (s5, 0.0, 0.0))}
chi2cmap = colors.LinearSegmentedColormap('chi2_colormap', cdict, 1024)
chi2cmap.set_bad('w', 1.0)
cdict2 = {'red':((0.0, 1.0, 1.0), (1.0, 0.0, 0.0)), 
 'green':((0.0, 1.0, 1.0), (1.0, 0.0, 0.0)), 
 'blue':((0.0, 1.0, 1.0), (1.0, 0.0, 0.0))}
cdict3 = {'red':((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)), 
 'green':((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)), 
 'blue':((0.0, 0.0, 0.0), (1.0, 1.0, 1.0))}
cdict4 = {'red':((0.0, 1.0, 1.0), (0.01, 0.0, 0.0), (0.05, 0.1, 0.1), (1.0, 0.9, 0.9)), 
 'green':((0.0, 1.0, 1.0), (0.01, 0.3, 0.3), (0.05, 0.1, 0.1), (1.0, 0.9, 0.9)), 
 'blue':((0.0, 1.0, 1.0), (0.01, 0.3, 0.3), (0.05, 0.1, 0.1), (1.0, 1.0, 1.0))}
margcmap = colors.LinearSegmentedColormap('marg_colormap', cdict4, 1024)
margconts = [0.68, 0.95]

def getcols(structarr, colnames):
    """"helper function to retrieve a normal, unstructured numpy array from the
    structured array that the dataset returns
    Args
    structarr - result of dset[:], or dset[0:1000] if a subset of rows is desired
    colnames  - list of field names to retrieve from array
    """
    data = np.array([structarr[col] for col in colnames]).transpose()
    print(data.shape, type(data))
    try:
        dataout = data[(~np.isnan(data).any(1))]
    except TypeError as err:
        try:
            print('TypeError encountered, dumping extra data...')
            for i, row in enumerate(data):
                try:
                    ~np.isnan(row).any(1)
                except (TypeError, NotImplementedError) as err2:
                    try:
                        print('TypeError or NotImplementedError occurred running isnan function on row {0}, dumping row...'.format(i))
                        print(row, type(row))
                        raise err2
                    finally:
                        err2 = None
                        del err2

        finally:
            err = None
            del err

    print(dataout.shape)
    print('NaN count: ', len(data) - len(dataout))
    return dataout


def bin2d(data, nxbins, nybins, binop='min', doconts=False):
    """2d binning algorithm
    Args
    data - n rows * 3 column dataset, columns in order x,y,z. Binning done
    by x,y
    binop - Operation to perform on bins. Available options:
        'min' - Returns the minimum z value for each bin
        'max' - Returns the maximum z value for each bin
    nxbins - Number of bins to use in x direction
    nybins -    "      "              y   "
    """
    x = data[:, 0]
    y = data[:, 1]
    zvals = data[:, 2]
    eps = 1e-10
    xindexes = np.floor((1 - eps) * nxbins * (x - min(x)) / (max(x) - min(x)))
    yindexes = np.floor((1 - eps) * nybins * (y - min(y)) / (max(y) - min(y)))
    outarray = np.zeros((nxbins, nybins))
    grouped = [list(value) for key, value in groupby((sorted(zip(xindexes, yindexes, zvals))), key=(itemgetter(0, 1)))]
    bininds = [nybins * bin[0][0] + bin[0][1] for bin in grouped]
    if binop == 'min':
        binvals = [min([el[2] for el in bin]) for bin in grouped]
        outarray[:, :] = np.nan
    elif binop == 'max':
        binvals = [max([el[2] for el in bin]) for bin in grouped]
        outarray[:, :] = 0
    elif binop == 'sum':
        binvals = [sum([el[2] for el in bin]) for bin in grouped]
        outarray[:, :] = 0
    else:
        raise ValueError('Invalid binop value ({0}) supplied to bin2d'.format(binop))
    try:
        outarray.flat[bininds] = binvals
    except ValueError:
        print("WARNING: nan's present in bin index lists, input data maybe degenerate in one or more dimensions.")
        raise

    if binop == 'sum':
        if doconts == True:
            outarray2 = np.zeros((nxbins, nybins))
            outarray2[:, :] = 1.0
            sb = np.array(sorted((zip(bininds, binvals)), key=(itemgetter(1)), reverse=True))
            outarray2.flat[list(sb[:, 0])] = list(np.cumsum(sb[:, 1]))
            return (
             outarray.transpose(), outarray2.transpose())
    return outarray.transpose()


def bin1d(data, nbins, binop='min'):
    """1d version of bin2d (in fact uses bin2d directly)
    Args:
    data - n rows * 2 column dataset, columns in order x,z. Binning done
    in x, z being the "height" or "density" to be binned.
    binop - Operation to perform on bins. Available options:
        'min' - Returns the minimum z value for each bin
        'max' - Returns the maximum z value for each bin
    nbins - Number of bins to use 
    """
    x = data[:, 0]
    y = np.zeros(x.shape[0])
    y[:x.shape[0] / 2] = 1
    z = data[:, 1]
    return bin2d((np.array(zip(x, y, z))), nbins, 1, binop, doconts=False)[0]


def forceAspect(ax, aspect=1):
    extent = ax.get_window_extent().get_points()
    print(extent)
    ax.set_aspect(abs((extent[(0, 1)] - extent[(0, 0)]) / (extent[(1, 1)] - extent[(1,
                                                                                    0)])) / aspect)


def chi2scatplot(ax, data, title=None, labels=None, s=1):
    """Creates a scatter plot of the data, colored by Delta chi^2 value
    Args:
    ax - Axis object on which to create plot
    data - 3 column numpy array with
        data[:,0] - x data
        data[:,1] - y data
        data[:,2] - chi^2 data
    """
    data = data[data[:, 2].argsort()[::-1]]
    plot = ax.scatter((data[:, 0]), (data[:, 1]), c=(np.sqrt(data[:, 2] - min(data[:, 2]))), s=s, lw=0, cmap=chi2cmap, norm=colors.Normalize(vmin=mn, vmax=mx, clip=True))
    if title:
        ax.set_title(title)
    if labels:
        ax.set_xlabel(labels[0])
    if labels:
        ax.set_ylabel(labels[1])
    ax.set_xlim(min(data[:, 0]), max(data[:, 0]))
    ax.set_ylim(min(data[:, 1]), max(data[:, 1]))
    ax.grid(True)
    return plot


def chi2logscatplot(ax, data, title=None, labels=None):
    """Creates a scatter plot of the data, colored by Delta chi^2 value
    """
    data = data[data[:, 2].argsort()[::-1]]
    plot = ax.scatter((data[:, 0]), (data[:, 1]), c=(np.sqrt(data[:, 2] - min(data[:, 2]))), s=1, lw=0, cmap=chi2cmap, norm=colors.Normalize(vmin=mn, vmax=mx, clip=True))
    ax.set_yscale('log')
    if title:
        ax.set_title(title)
    if labels:
        ax.set_xlabel(labels[0])
    if labels:
        ax.set_ylabel(labels[1])
    ax.set_xlim(min(data[:, 0]), max(data[:, 0]))
    ax.set_ylim(min(data[:, 1]), max(data[:, 1]))
    ax.grid(True)
    return plot


def profplot(ax, data, title=None, labels=None, nybins=100, nxbins=None):
    """Creates a binned, profiled plot of the data, colored by Delta chi^2 value,
    i.e. profile likelihood.
    """
    if nxbins is None:
        nxbins = np.floor(1.618 * nybins)
    x = data[:, 0]
    y = data[:, 1]
    wx = (max(x) - min(x)) / nxbins
    wy = (max(y) - min(y)) / nybins
    xlist = np.arange(min(x), max(x) - wx * 0.01, wx)
    ylist = np.arange(min(y), max(y) - wy * 0.01, wy)
    outarray = bin2d(data, nxbins, nybins, binop='min')
    X, Y = np.meshgrid(xlist, ylist)
    minchi2 = np.nanmin(outarray)
    Dchi2 = np.sqrt(outarray - minchi2)
    masked_array = np.ma.array(Dchi2, mask=(np.isnan(Dchi2)))
    im = ax.imshow(masked_array, origin='lower', interpolation='nearest', extent=(
     min(xlist), max(xlist) + wx, min(ylist), max(ylist) + wy),
      cmap=chi2cmap,
      norm=colors.Normalize(vmin=mn, vmax=mx, clip=True),
      aspect='auto')
    CS = ax.contour((X + wx / 2), (Y + wy / 2), (outarray - minchi2), levels=rellevels, lw=3)
    bfidx = np.where(outarray.flat == minchi2)
    ax.plot([X.flat[bfidx]], [Y.flat[bfidx]], 'ko')
    if labels:
        ax.set_xlabel(labels[0])
    if labels:
        ax.set_ylabel(labels[1])
    ax.set_xlim(min(data[:, 0]), max(data[:, 0]))
    ax.set_ylim(min(data[:, 1]), max(data[:, 1]))
    ax.grid(True)
    return im


def margplot(ax, data, nxbins=100, nybins=100, title=None, labels=None):
    """Creates a binned marginalised plot of the data, colored by marginalised posterior
    density.
    """
    x = data[:, 0]
    y = data[:, 1]
    wx = (max(x) - min(x)) / nxbins
    wy = (max(y) - min(y)) / nybins
    xlist = np.arange(min(x), max(x) - wx * 0.01, wx)
    ylist = np.arange(min(y), max(y) - wy * 0.01, wy)
    outarraydens, outarrayconts = bin2d(data, nxbins, nybins, binop='sum', doconts=True)
    X, Y = np.meshgrid(xlist, ylist)
    maxpoint = max(outarraydens.flat)
    im = ax.imshow(outarraydens, origin='lower', interpolation='nearest', extent=(
     min(xlist), max(xlist) + wx, min(ylist), max(ylist) + wy),
      cmap=margcmap,
      aspect='auto')
    CS = ax.contour((X + wx / 2), (Y + wy / 2), outarrayconts, levels=margconts, lw=3, colors=[(0, 1, 0), (1, 1, 0)])
    bfidx = np.where(outarraydens.flatten() == maxpoint)
    ax.plot([X.flat[bfidx]], [Y.flat[bfidx]], 'ko')
    if labels:
        ax.set_xlabel(labels[0])
    if labels:
        ax.set_ylabel(labels[1])
    ax.set_xlim(min(data[:, 0]), max(data[:, 0]))
    ax.set_ylim(min(data[:, 1]), max(data[:, 1]))
    ax.grid(True)
    return im


def margplot1D(ax, data, title=None, labels=None, trim=True):
    """Creates a 1D binned marginalised plot of the data
    Args:
    data[:,0] - x data
    data[:,1] - corresponding posterior masses 
    trim - Cut off outer bins containing less than 0.01% probability mass
    """
    nxbins = 200
    x = data[:, 0]
    wx = (max(x) - min(x)) / nxbins
    xlist = np.arange(min(x), max(x) - wx * 0.01, wx)
    outarraydens = bin1d(data, nxbins, binop='sum')
    if trim:
        while True:
            posl = 0
            pmass = outarraydens[posl]
            while pmass < 0.001:
                posl += 1
                pmass = outarraydens[posl]

            posh = len(outarraydens) - 1
            pmass = outarraydens[posh]
            while pmass < 0.001:
                posh -= 1
                pmass = outarraydens[posh]

            data = data[np.logical_and(data[:, 0] > xlist[posl], data[:, 0] < xlist[(posh + 1)])]
            x = data[:, 0]
            wx = (max(x) - min(x)) / nxbins
            xlist = np.arange(min(x), max(x) - wx * 0.01, wx)
            if posh - posl > 80:
                break
            outarraydens = bin1d(data, nxbins, binop='sum')

    im = ax.bar(xlist, outarraydens, wx, linewidth=0, color='b', alpha=0.4)
    if labels:
        ax.set_xlabel(labels)
    ax.set_ylabel('Binned posterior mass')
    ax.set_xlim(min(data[:, 0]), max(data[:, 0]))
    return im