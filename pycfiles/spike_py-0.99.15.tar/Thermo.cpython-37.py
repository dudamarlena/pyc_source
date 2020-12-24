# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/File/Thermo.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 3158 bytes
"""
    Utility to Handle Thermofisher files

    Marc-André from first draft by Lionel
"""
from __future__ import print_function
__author__ = 'Marc André Delsuc'
__date__ = 'april 2014'
import os, unittest, numpy as np
from ..Orbitrap import OrbiData
import re

def read_thermo(filename):
    """
    reads a thermofisher orbitrap file
    """
    with open(filename, 'rb') as (F):
        param = read_param(F)
        if param['Storage Type'] == 'float':
            typ = 'f4'
        else:
            if param['Storage Type'] == 'double':
                typ = 'f8'
            else:
                if param['Storage Type'] == 'int':
                    typ = 'i4'
                else:
                    raise Exception('Unknown Storage type : ' + param['Storage Type'])
        data = read_data(F, typ)
        swnew = float(param['Bandwidth'])
        data.axis1.calibA = float(param['Source Coeff1'])
        data.axis1.calibB = float(param['Source Coeff2']) * 1000000.0
        data.axis1.calibC = float(param['Source Coeff3']) * 1000000000000.0
        data.axis1.specwidth = swnew
    return (param, data)


def read_param(F):
    """
        given F, an opend file , retrieve all parameters found in file header
        
        read_param returns  values in a plain dictionnary
    """
    dic = {}
    for l in F:
        if l.startswith('Data:'):
            break
        v = l.rstrip().split(':')
        if len(v) < 2:
            print(l)
        else:
            dic[v[0]] = v[1].lstrip()

    return dic


def read_data(F, typ='float'):
    """
        given F, an opened file, reads the values and 
        read_param returns  values in a dictionnary
    """
    F.seek(0)
    pos = 0
    for l in F:
        pos += len(l)
        if l.startswith('Data Points'):
            print(re.findall('\\d+', l)[0])
        if l.startswith('Data:'):
            break

    F.seek(pos)
    data_interm = np.array(np.fromfile(F, dtype=typ).tolist())
    data = OrbiData(buffer=data_interm)
    return data


def Import_1D(filename):
    """
    Entry point to import 1D spectra
    It returns an Orbitrap data
    """
    param, data = read_thermo(filename)
    data.params = param
    return data


class Thermo_Tests(unittest.TestCase):
    __doc__ = ' A FAIRE '

    def setUp(self):
        from ..Tests import filename, directory
        try:
            import ConfigParser
        except:
            import configparser as ConfigParser

        rootfiles = os.getcwd()
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')


if __name__ == '__main__':
    unittest.main()