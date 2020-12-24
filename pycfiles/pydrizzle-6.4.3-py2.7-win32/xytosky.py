# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pydrizzle\xytosky.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import string, copy, os, pyfits, numpy as np
from numpy import char as C
from math import *
import pydrizzle
from stsci.tools import wcsutil
yes = True
no = False

def XYtoSky_pars(input, x=None, y=None, coords=None, colnames=None, linear=yes, idckey='IDCTAB', hms=no, output=None, verbose=yes):
    if not coords:
        xy = (x, y)
    else:
        xy = []
        if coords.find('.fits') > 0:
            if not colnames:
                _clist = ['X', 'Y']
            else:
                _clist = colnames.split(',')
            _ftab = pyfits.open(coords)
            x = _ftab[1].data.field(_clist[0]).tolist()
            y = _ftab[1].data.field(_clist[1]).tolist()
            for i in xrange(len(x)):
                xy.append([x[i], y[i]])

            _ftab.close()
            del _ftab
        else:
            _ifile = open(coords)
            _lines = _ifile.readlines()
            _ifile.close()
            if colnames:
                _clist = colnames.split(',')
            else:
                _clist = [
                 '1', '2']
            for n in xrange(len(_clist)):
                _clist[n] = string.atoi(_clist[n]) - 1

            for line in _lines:
                line = line.strip()
                line.replace('\t', ' ')
                if len(line) > 0 and line[0] != '#':
                    _xy = line.split()
                    x = string.atof(_xy[_clist[0]])
                    y = string.atof(_xy[_clist[1]])
                    xy.append([x, y])

    radec = XYtoSky(input, xy, idckey=idckey, linear=linear, verbose=no)
    if isinstance(radec, type([])):
        radd, decdd = [], []
        for pos in radec:
            radd.append(pos[0])
            decdd.append(pos[1])

        radd = np.array(radd)
        decdd = np.array(decdd)
    else:
        radd = np.array([radec[0]])
        decdd = np.array([radec[1]])
    if hms:
        ra, dec = wcsutil.ddtohms(radd, decdd, verbose=verbose)
    else:
        ra, dec = radd, decdd
        if not output or verbose:
            for i in xrange(len(ra)):
                print 'RA (deg.) = ', ra[i], ', Dec (deg.)= ', dec[i]

    if output:
        _olines = []
        if output == coords:
            if coords.find('.fits') > 0:
                _fout = pyfits.open(coords, 'update')
                _fout[1].data
                _tcol = _fout[1].columns
                raname = 'RA'
                decname = 'Dec'
                if hms:
                    racol = pyfits.Column(name=raname, format='24a', array=C.array(ra))
                    deccol = pyfits.Column(name=decname, format='24a', array=C.array(dec))
                else:
                    racol = pyfits.Column(name=raname, format='1d', array=ra)
                    deccol = pyfits.Column(name=decname, format='1d', array=dec)
                _tcol.add_col(racol)
                _tcol.add_col(deccol)
                _thdu = pyfits.new_table(_tcol)
                del _fout[1]
                _fout.append(_thdu)
                _fout.close()
                del _fout
                del _thdu
                del _tcol
            else:
                _olines.insert(0, '# Image: ' + input + '\n')
                _olines.insert(0, '# RA Dec positions computed by PyDrizzle\n')
                pos = 0
                for line in _lines:
                    line = line.strip()
                    if line[0] != '#' and line != '':
                        line = line + '    ' + str(ra[pos]) + '    ' + str(dec[pos]) + '\n'
                        pos = pos + 1
                    _olines.append(line)

                _ofile = open(output, 'w')
                _ofile.writelines(_olines)
                _ofile.close()
        else:
            _olines.append('# RA Dec positions computed by PyDrizzle\n')
            _olines.append('# Image: ' + input + '\n')
            if coords:
                for pos in xrange(len(ra)):
                    _str = str(ra[pos]) + '    ' + str(dec[pos]) + '\n'
                    _olines.append(_str)

            else:
                _str = str(ra) + '    ' + str(dec) + '\n'
                _olines.append(_str)
            _ofile = open(output, 'w')
            _ofile.writelines(_olines)
            _ofile.close()
    return (
     ra, dec)


def XYtoSky(input, pos, idckey='IDCTAB', linear=yes, verbose=no):
    """ Convert input pixel position(s) into RA/Dec position(s).
        Output will be either an (ra,dec) pair or a 'list' of (ra,dec)
        pairs, not a numpy, to correspond with the input position(s).

        Parameter:
            input - Filename with extension specification of image
            pos   - Either a single [x,y] pair or a list of [x,y] pairs.
            idckey - Keyword which points to the IDC table to be used.
            linear - If no, apply distortion correction for image.

    """
    _insplit = string.split(input, '[')
    if len(_insplit) == 1:
        raise IOError, 'No extension specified for input image!'
    if not isinstance(pos, np.ndarray):
        if np.array(pos).ndim > 1:
            pos = np.array(pos, dtype=np.float64)
    _exposure = pydrizzle.Exposure(input, idckey=idckey)
    ra, dec = _exposure.geometry.XYtoSky(pos, linear=linear, verbose=verbose)
    if not isinstance(ra, np.ndarray):
        return (
         ra, dec)
    else:
        _radec = np.zeros(shape=(len(ra), 2), dtype=ra.dtype)
        _radec[:, 0] = ra
        _radec[:, 1] = dec
        return _radec.tolist()