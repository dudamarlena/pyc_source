# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/File/Solarix.py
# Compiled at: 2019-08-14 15:56:48
# Size of source mod 2**32: 18826 bytes
"""
Solarix.py

    Utility to Handle Solarix files

Created by mac on 2013-05-24.
updated may 2017 to python 3, added compress option

Copyright (c) 2013 __NMRTEC__. All rights reserved.
"""
from __future__ import print_function, division
import sys, os, unittest, glob
import os.path as op
import numpy as np, array, tables
from xml.dom import minidom
from time import time
import math
from .. import NPKData as npkd
from ..FTICR import FTICRData
from ..File import HDF5File as hf
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def read_param(parfilename):
    """
        Open the given file and retrieve all parameters from apexAcquisition.method
        NC is written when no value for value is found
        
        structure : <param name = "AMS_ActiveExclusion"><value>0</value></param>
       
        read_param returns  values in a dictionnary
    """
    xmldoc = minidom.parse(parfilename)
    x = xmldoc.documentElement
    pp = {}
    children = x.childNodes
    for child in children:
        if child.nodeName == 'paramlist':
            params = child.childNodes
            for param in params:
                if param.nodeName == 'param':
                    k = str(param.getAttribute('name'))
                    for element in param.childNodes:
                        if element.nodeName == 'value':
                            try:
                                v = str(element.firstChild.toxml())
                            except:
                                v = 'NC'

                    pp[k] = v

    return pp


def read_scan(filename):
    """
    Function that returns the number of scan that have been recorded
    It is used to see wether the number of recorded points corresponds to the L_20 parameter
    """
    xmldoc = minidom.parse(filename)
    x = xmldoc.documentElement
    pp = {}
    children = x.childNodes
    count_scan = 0
    for child in children:
        if child.nodeName == 'scan':
            count_scan += 1

    return count_scan


def read_ExciteSweep(filename):
    """
    Function that returns the lower and higher frequency of the pulse generator
    """
    ExciteSweep_lines = np.genfromtxt(filename, comments='*', delimiter='\n')
    highfreq = np.fromstring(ExciteSweep_lines[0])
    lowfreq = np.fromstring(ExciteSweep_lines[(-1)])
    return (lowfreq, highfreq)


def get_param(param, names, values):
    """
    From params, this function returns the  value of the given param
    """
    for i in xrange(len(names)):
        if names[i] == param:
            return values[i]


def locate_acquisition(folder):
    """
        From the given folder this function return the absolute path to the apexAcquisition.method file
        It should always be in a subfolder 
    """
    L = glob.glob(op.join(folder, '*', 'apexAcquisition.method'))
    if len(L) > 1:
        raise Exception('You have more than 1 apexAcquisition.method file in the %s folder, using the first one' % folder)
    else:
        if len(L) == 0:
            raise Exception("You don't have any apexAcquisition.method file in the  %s folder, please double check the path" % folder)
    return L[0]


def locate_ExciteSweep(folder):
    """
        From the given folder this function return the absolute path to the ExciteSweep file
        It should always be in a subfolder 
    """
    L = glob.glob(op.join(folder, '*', 'ExciteSweep'))
    if len(L) > 1:
        raise Exception('You have more than 1 ExciteSweep file in the %s folder, using the first one' % folder)
    else:
        if len(L) == 0:
            raise Exception("You don't have any ExciteSweep file in the  %s folder, please double check the path" % folder)
    return L[0]


def Import_1D(inifolder, outfile='', compress=False):
    """
    Entry point to import 1D spectra
    It returns a FTICRData
    It writes a HDF5 file if an outfile is mentionned
    """
    if sys.maxsize == 2147483647:
        flag = 'l'
    else:
        flag = 'i'
    if op.isfile(inifolder):
        folder = op.dirname(inifolder)
    else:
        if op.isdir(inifolder):
            folder = inifolder
        else:
            if not op.exists(inifolder):
                raise Exception('File does not exist: ' + inifolder)
            else:
                raise Exception('File is undecipherable: ' + inifolder)
    try:
        parfilename = locate_acquisition(folder)
    except:
        raise Exception('%s does not seem to be a valid Solarix spectrum' % (inifolder,))

    params = read_param(parfilename)
    sizeF1 = int(params['TD'])
    if os.path.isfile(os.path.join(folder, 'fid')):
        fname = os.path.join(folder, 'fid')
    else:
        raise Exception('You are dealing with 2D data, you should use Import_2D')
    data = FTICRData(dim=1)
    data.axis1.size = sizeF1
    data.axis1.specwidth = float(params['SW_h'])
    try:
        l, h = read_ExciteSweep(locate_ExciteSweep(folder))
    except:
        data.axis1.highfreq = float(params['EXC_Freq_High'])
        data.axis1.lowfreq = float(params['EXC_Freq_Low'])
    else:
        data.axis1.lowfreq, data.axis1.highfreq = l, h
    data.axis1.highmass = float(params['MW_high'])
    data.axis1.left_point = 0
    data.axis1.offset = 0.0
    data.axis1.calibA = float(params['ML1'])
    data.axis1.calibB = float(params['ML2'])
    data.axis1.calibC = float(params['ML3'])
    if not math.isclose(data.axis1.calibC, 0.0):
        print('Using 3 parameters calibration,  Warning calibB is -ML2')
        data.axis1.calibB *= -1
    else:
        data.params = params
        if outfile:
            HF = hf.HDF5File(outfile, 'w', compress=compress)
            HF.create_from_template(data)
            HF.store_internal_object(params, h5name='params')
            HF.store_internal_file(parfilename)
            HF.store_internal_file(locate_ExciteSweep(folder))
            data.hdf5file = HF
        else:
            data.buffer = np.zeros(sizeF1)
    data.adapt_size()
    with open(fname, 'rb') as (f):
        tbuf = f.read(4 * sizeF1)
        abuf = np.array(array.array(flag, tbuf))
        data.buffer[:] = abuf[:]
    if outfile:
        HF.flush()
    return data


def Import_2D(folder, outfile='', F1specwidth=None, compress=False):
    """
    Entry point to import 2D spectra
    It returns a FTICRData
    It writes a HDF5 file if an outfile is mentionned
    
    compression (compress=True) is efficient, but takes a lot of time.
    """
    if sys.maxsize == 2147483647:
        flag = 'l'
    else:
        flag = 'i'
    parfilename = locate_acquisition(folder)
    params = read_param(parfilename)
    sizeF1 = read_scan(os.path.join(folder, 'scan.xml'))
    sizeF2 = int(params['TD'])
    if os.path.isfile(os.path.join(folder, 'ser')):
        fname = os.path.join(folder, 'ser')
    else:
        raise Exception('You are dealing with 1D data, you should use Import_1D')
    data = FTICRData(dim=2)
    data.axis2.size = sizeF2
    data.axis2.specwidth = float(params['SW_h'])
    try:
        l, h = read_ExciteSweep(locate_ExciteSweep(folder))
    except:
        data.axis2.highfreq = float(params['EXC_Freq_High'])
        data.axis2.lowfreq = float(params['EXC_Freq_Low'])
    else:
        data.axis2.lowfreq, data.axis2.highfreq = l, h
    data.axis2.highmass = float(params['MW_high'])
    data.axis2.left_point = 0
    data.axis2.offset = 0.0
    data.axis2.calibA = float(params['ML1'])
    data.axis2.calibB = float(params['ML2'])
    data.axis2.calibC = float(params['ML3'])
    if not math.isclose(data.axis2.calibC, 0.0):
        print('Using 3 parameters calibration,  Warning calibB is -ML2')
        data.axis2.calibB *= -1
    else:
        data.axis1.size = sizeF1
        if F1specwidth is not None:
            data.axis1.specwidth = F1specwidth
        else:
            f1 = float(params['IN_26'])
            if f1 < 0.0001:
                data.axis1.specwidth = 1.0 / (2 * f1)
            else:
                data.axis1.specwidth = data.axis2.specwidth
        data.axis1.highfreq = data.axis2.highfreq
        data.axis1.lowfreq = data.axis2.lowfreq
        data.axis1.highmass = float(params['MW_high'])
        data.axis1.left_point = 0
        data.axis1.offset = 0.0
        data.axis1.calibA = data.axis2.calibA
        data.axis1.calibB = data.axis2.calibB
        data.axis1.calibC = data.axis2.calibC
        data.params = params
        c1 = int(sizeF1 / 8.0 + 1)
        c2 = int(sizeF2 / 8.0 + 1)
        if outfile:
            HF = hf.HDF5File(outfile, 'w')
            if compress:
                HF.set_compression(True)
            HF.create_from_template(data)
            HF.store_internal_object(params, h5name='params')
            HF.store_internal_file(parfilename)
            HF.store_internal_file(os.path.join(folder, 'scan.xml'))
            HF.store_internal_file(locate_ExciteSweep(folder))
            data.hdf5file = HF
        else:
            data.buffer = np.zeros((sizeF1, sizeF2))
    with open(fname, 'rb') as (f):
        for i1 in xrange(sizeF1 - 1):
            tbuf = f.read(4 * sizeF2)
            abuf = np.array(array.array(flag, tbuf))
            data.buffer[i1, :] = abuf[:]

    if outfile:
        HF.flush()
    return data


def read_2D(sizeF1, sizeF2, filename='ser'):
    """
    Reads in a Solarix 2D fid

    sizeF1 is the number of fid
    sizeF2 is the number of data-points in the fid
    uses array
    """
    if sys.maxsize == 2147483647:
        flag = 'l'
    else:
        flag = 'i'
    sz1, sz2 = int(sizeF1), int(sizeF2)
    fbuf = np.empty((sz1, sz2))
    with open(filename, 'rb') as (f):
        for i1 in xrange(sz1):
            tbuf = f.read(4 * sz2)
            abuf = array.array(flag, tbuf)
            fbuf[i1, 0:sz2] = abuf[0:sz2]

    return FTICRData(buffer=fbuf)


def read_3D(sizeF1, sizeF2, sizeF3, filename='ser'):
    """
    Ebauche de fonction
    
    Reads in a Apex 3D fid

    uses array
    """
    if sys.maxsize == 2147483647:
        flag = 'l'
    else:
        flag = 'i'
    sz1, sz2, sz3 = int(sizeF1), int(sizeF2), int(sizeF3)
    fbuf = np.empty((sz1, sz2, sz3))
    with open(filename, 'rb') as (f):
        for i1 in xrange(sz1):
            tbuf = f.read(4 * sz2)
            abuf = array.array(flag, tbuf)
            fbuf[i1, 0:sz2] = abuf[0:sz2]

    return FTICRData(buffer=fbuf)


def write_ser(bufferdata, filename='ser'):
    """
    Write a ser file from FTICRData
    """
    with open(filename, 'wb') as (f):
        for i in range(len(bufferdata)):
            for j in range(len(bufferdata[0])):
                f.write(bufferdata[i][j].astype('int32').tostring())


class Solarix_Tests(unittest.TestCase):

    def setUp(self):
        from ..Tests import filename, directory
        import ConfigParser
        rootfiles = os.getcwd()
        self.TestFolder = directory()
        self.DataFolder = filename('bilirubin_2D_000001.d')
        self.serfile = filename('bilirubin_2D_000001.d/ser')
        self.outHDF = filename('bilirubin_2D_000001.direct.msh5')
        self.name_write = filename('file_write')
        self.name_fticr = filename('file_fticr')
        self.name_npar = filename('file_npar')
        self.npar_fticr = filename('npar_fticr')
        self.name_chunk = filename('Chunk.hf')
        self.name_get = filename('file_fticr')
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def _test_Import_2D(self):
        """Test and time routine that import 2D from the MS-FTICR folder to the file given as second argument """
        self.announce()
        t0 = time()
        d = Import_2D(self.DataFolder, self.name_get)
        print('import', time() - t0, 'secondes')

    def _test_Import_2D_keep_mem(self):
        """Test and time routine that import 2D from the MS-FTICR folder in memory"""
        from ..Tests import filename, directory
        self.announce()
        t0 = time()
        d = filename('subP_2D_000001.d')
        print('import', time() - t0, 'secondes')

    def _test_2(self):
        """ Test and time direct processing"""
        self.announce()
        d = Import_2D(self.DataFolder)
        t0 = time()
        t00 = t0
        d.rfft(axis=2)
        print('rfft2', time() - t0, 'secondes')
        t0 = time()
        d.rfft(axis=1)
        print('rfft1', time() - t0, 'secondes')
        t0 = time()
        d.modulus()
        print('modulus', time() - t0, 'secondes')
        t0 = time()
        print('modulus', time() - t0, 'secondes')
        print('calcul', time() - t00, 'secondes')
        d.display(scale=30, show=True)
        d.fticrfile.close()

    def _test_3(self):
        """Another strategy close the file after fft on F2 and reopen everything for F1 fft"""
        from ..Tests import filename, directory
        self.announce()
        d = Import_2D(self.DataFolder, filename('essai.ap'))
        t0 = time()
        t00 = t0
        d.rfft(axis=2)
        d.fticrfile.close()
        print('rfft2', time() - t0, 'secondes')
        t0 = time()
        F = ff(filename('essai.ap'), 'rw')
        F.load()
        d2 = F.data
        d2.rfft(axis=1)
        print('rfft1', time() - t0, 'secondes')
        t0 = time()
        d2.modulus()
        print('modulus', time() - t0, 'secondes')
        t0 = time()
        print('modulus', time() - t0, 'secondes')
        print('calcul', time() - t00, 'secondes')
        d2.display(scale=5, show=True)
        F.close()
        H = ff(filename('essai.ap'), 'r')
        H.load()
        B = H.data
        H.close()


if __name__ == '__main__':
    unittest.main()