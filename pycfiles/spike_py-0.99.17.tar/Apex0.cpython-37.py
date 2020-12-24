# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/ mad/CASC4DE/CODES/EUFTICR-NB/spike/File/Apex0.py
# Compiled at: 2020-04-22 11:39:53
# Size of source mod 2**32: 2197 bytes
"""
    Utility to Handle old Apex files - "NMR style"
"""
from __future__ import print_function, division
__author__ = 'Marc André Delsuc'
__date__ = 'April 2020'
import sys, math
import os.path as op
from ..FTICR import FTICRData
from . import BrukerNMR as bkn
VERBOSE = False
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def read_param(filename='acqus'):
    """get the acqus file and return a dictionary"""
    return bkn.read_param(filename=filename)


def Import_1D(filename='fid', verbose=VERBOSE):
    """
    Imports a 1D Bruker fid as a ftICRData
    
    """
    if not op.exists(filename):
        raise Exception(filename + ' : file not found')
    else:
        dire = op.dirname(filename)
        acqu = read_param(bkn.find_acqu(dire))
        size = int(acqu['$TD'])
        if verbose:
            print('imported 1D FID, size =%d\n%s' % (size, acqu['title']))
        data = bkn.read_1D(size, filename, bytorda=(int(acqu['$BYTORDA'])))
        NC = int(acqu['$NC'])
        if NC != 0:
            data *= 2 ** NC
        d = FTICRData(buffer=data)
        d.axis1.specwidth = float(acqu['$SW_h'])
        d.axis1.calibA = float(acqu['$ML1'])
        d.axis1.calibB = float(acqu['$ML2'])
        d.axis1.calibC = float(acqu['$ML3'])
        d.axis1.highmass = float(acqu['$MW_high'])
        d.axis1.highfreq = d.axis1.calibA / float(acqu['$EXC_low'])
        d.axis1.lowfreq = d.axis1.calibA / float(acqu['$EXC_hi'])
        d.axis1.left_point = 0
        d.axis1.offset = 0.0
        math.isclose(d.axis1.calibC, 0.0) or print('Using 3 parameters calibration,  Warning calibB is -ML2')
        d.axis1.calibB *= -1
    proc = read_param(bkn.find_proc(dire))
    pardic = {'acqu':acqu,  'proc':proc}
    d.params = pardic
    if verbose:
        print('imported 1D FID, size =%d\n%s' % (size, acqu['title']))
    return d