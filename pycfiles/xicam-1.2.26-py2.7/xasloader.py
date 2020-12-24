# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\xas\xasloader.py
# Compiled at: 2019-03-07 15:49:41
import pandas as pd
from modpkgs.memoize import memoized_property
import numpy as np
try:
    from larch import Interpreter
    from larch_plugins.math.mathutils import index_of
    from larch_plugins.xafs import pre_edge
    mylarch = Interpreter()
except ImportError:
    print 'Larch is not installed; XAS plugin will be disabled.'

from os import path

def open(f):
    global XASclasses
    for cls in XASclasses:
        if hasattr(cls, 'validate'):
            try:
                cls.validate(f)
            except Exception as ex:
                continue
            else:
                return cls(f)

        try:
            obj = cls(f)
            return obj
        except Exception as ex:
            continue

    raise ValueError('The selected file could not be loaded with any recognized format.')


class XASSpectra(object):

    def __init__(self, f):
        self.scans = []
        self.read(f)

    def read(self, filename, frame=None):
        """
        To be overridden - fill in self.header and self.data
        """
        raise Exception('Class has not implemented read method yet')

    def normalize(self):
        for scan in self.scans:
            scan['I_norm'] = scan.Data.astype(float) / scan.Reference.astype(float)

    def pre_edge(self):
        for scan in self.scans:
            pre_edge(scan.Energy, scan.I_norm, pre1=-10, pre2=-2, group=scan, _larch=mylarch)
            scan.I_norm = scan.I_norm - scan.pre_edge

    def lowcut(self, limit=50):
        self.scans = [ scan[limit:] for scan in self.scans ]

    def treat(self):
        self.normalize()
        self.pre_edge()
        self.lowcut()


XASclasses = []

def register_xasclass(cls):
    XASclasses.append(cls)
    return cls


@register_xasclass
class BL632Spectra(XASSpectra):
    colmap = {'TEY': 'Data', 'I1': 'Reference'}

    def read(self, filename, scan=None):
        self.rawdata = pd.read_table(filename, header=1, names=['Energy', 'I1', 'TEY', 'I0'])
        self.rawdata.rename(columns=self.colmap, inplace=True)
        self.scans = [self.rawdata]
        return self

    is_stacked = False
    num_scans = 1

    @staticmethod
    def validate(filename):
        assert path.splitext(filename)[(-1)] == '.dat'
        assert not pd.read_table(filename, header=1, names=['Energy', 'I1', 'TEY', 'I0']).empty

    @memoized_property
    def num_bins(self):
        return self.rawdata.shape[0]

    def scan(self, N):
        return self.scans[N]


@register_xasclass
class BL6311Spectra(XASSpectra):
    colmap = {'Counter 3': 'Data', 'Counter 2': 'Reference'}
    skiprows = 10

    def read(self, filename, scan=None):
        """import scan file"""
        scandata_f = pd.read_csv(filename, sep='\t', skiprows=self.skiprows)
        self.rawdata = scandata_f
        self.rawdata.rename(columns=self.colmap, inplace=True)
        self.scans = [ self.scan(i) for i in range(self.num_scans) ]
        return self

    @staticmethod
    def validate(filename, skiprows=skiprows):
        assert path.splitext(filename)[(-1)] == '.txt'
        assert not pd.read_csv(filename, sep='\t', skiprows=skiprows).empty

    @memoized_property
    def is_stacked(self):
        """Determine stacked or single scan file(s) and informs user"""
        return len(self.rawdata.Energy) != len(set(self.rawdata.Energy))

    @memoized_property
    def num_scans(self):
        return len(self.rawdata.Energy) / len(set(self.rawdata.Energy))

    @memoized_property
    def num_bins(self):
        return len(set(self.rawdata.Energy))

    def scan(self, N, scan_rng=0, unstacked=pd.DataFrame(np.array([]))):
        return self.rawdata.iloc[N * self.num_bins:(N + 1) * self.num_bins, :].copy()


@register_xasclass
class BL11012Spectra(BL6311Spectra):
    colmap = {'TEY signal': 'Data', 'AI 3 Izero': 'Reference', 'Beamline Energy': 'Energy'}
    skiprows = 15

    @staticmethod
    def validate(filename, skiprows=skiprows):
        BL6311Spectra.validate(filename, skiprows)


def tests():
    files = [
     '/home/rp/data/XAS/TrajScan21930.txt',
     '/home/rp/data/XAS/TrajScan18764_0001.txt',
     '/home/rp/data/XAS/DB_Cedge_000006.dat',
     '/home/rp/data/XAS/Fe_L_DB_29733.txt',
     '/home/rp/data/XAS/O_K_DB_29726.txt']
    for s in files:
        print 'Opening:', s
        s = open(s)
        s.treat()
        for scan in s.scans:
            print len(np.array(scan.Energy)),
            print len(np.array(scan.I_norm))


if __name__ == '__main__':
    tests()