# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/File/GifaFile.py
# Compiled at: 2020-01-29 13:53:28
# Size of source mod 2**32: 28931 bytes
"""
GifaFile.py

Created by Marc-André on 2010-03-17.
Copyright (c) 2010 IGBMC. All rights reserved.

This module provides a simple access to NMR files in the Gifa format.

"""
from __future__ import print_function, division
import re, numpy as np
from .. import NPKData as npkd
from .. import NMR
from ..NPKError import NPKError
import unittest, os, sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range
HEADERSIZE = 4096
BLOCKIO = 4096
__version__ = '0.3'

class GifaFile(object):
    __doc__ = '\n    defines the interface to simply (read/write) acces Gifa v4 files\n    standard methods are load() and save()\n    \n    standard sequence to read is\n    F = GifaFile(filename,"r")\n    B = F.get_data()      # B is a NPKdata\n    F.close()\n\n    or\n    F = GifaFile(filename,"r")\n    F.load()\n    B = F.data      # B is a NPKdata\n    F.close()\n    \n\n    and to write\n    F = GifaFile(filename,"w")\n    F.set_data(B)         # where B is a NPKdata; do not use    F.data = B\n    F.save()\n    F.close()\n\n    The file consists of a header (of size headersize) and data\n    The header is handled as a dictionnary  self.header\n    data is handled as a NPKdata    self.data\n        so numpy ndarray are in                self.data.buffer\n    '

    def __init__(self, fname, access='r', debug=0):
        self.debug = debug
        if isinstance(fname, str):
            self.fname = fname
            if access not in ('w', 'r'):
                raise Exception(access + ' : acces key not valid')
            self.file = open(fname, access)
            if access == 'r':
                self.fileB = open(fname, 'rb')
        else:
            try:
                self.fname = fname.name
            except AttributeError:
                self.fname = 'internal_buffer'
            else:
                self.file = fname
                self.fileB = fname
        if access == 'r':
            l = self.fileB.readline(32)
            hsz = re.match('HeaderSize\\s*=\\s*(\\d+)', l.decode())
            if not hsz:
                self.file.close()
                raise Exception('file %s not valid' % fname)
            self.headersize = int(hsz.group(1))
            self.fileB.seek(0)
        if access == 'w':
            self.headersize = HEADERSIZE
        self.header = None
        self.header_valid = False
        self.data = None
        self.data_valid = False

    def report(self):
        """prints a little debugging report"""
        print('Dim', self.dim)
        print('header_valid', self.header_valid)
        print('data_valid', self.data_valid)
        print('header', self.header)

    def get_data(self):
        """returns the NPKdata attached to the (read) file"""
        if not self.data_valid:
            self.load()
            self.data_valid = True
        return self.data

    def set_data(self, buff):
        """sets the NPKdata attached to the (to be written) file"""
        self.data = buff
        self.setup_header()
        self.data_valid = True
        self.header_valid = True

    def copyaxesfromheader(self, n_axis):
        """
        get values from axis "n_axis" from header, and creates and returns a new (NMRAxis) axis with this values
        itype is not handled (not coded per axis in header)
        used internally
        """
        axis = NMR.NMRAxis()
        axis.size = int(self.header[('Dim%d' % n_axis)])
        axis.specwidth = float(self.header[('Specw%d' % n_axis)])
        axis.offset = float(self.header[('Offset%d' % n_axis)])
        axis.frequency = float(self.header[('Freq%d' % n_axis)])
        return axis

    def copydiffaxesfromheader(self):
        """
        get values from axis "n" from header, and creates and returns a new (LaplaceAxis) axis with this values
        used internally
        """
        axis = npkd.LaplaceAxis()
        axis.size = int(self.header['Dim1'])
        if self.header['Dmin'] != 'NaN':
            axis.dmin = float(self.header['Dmin'])
            axis.dmax = float(self.header['Dmax'])
            axis.dfactor = float(self.header['Dfactor'])
        else:
            axis.dmin = 1.0
            axis.dmax = 10.0
            axis.dfactor = 1.0
        return axis

    def load(self):
        """creates a NPKdata loaded with the file content"""
        if not self.header_valid:
            self.load_header()
        if not self.data_valid:
            ndata = NMR.NMRData(buffer=(self.readc()), dim=(self.dim))
            ndata.axis1 = self.copyaxesfromheader(1)
            if ndata.dim >= 2:
                ndata.axis2 = self.copyaxesfromheader(2)
            else:
                if ndata.dim >= 3:
                    ndata.axis3 = self.copyaxesfromheader(3)
                if ndata.dim == 1:
                    ndata.axis1.itype = self.itype
                else:
                    if ndata.dim == 2:
                        ndata.axis1.itype = self.itype // 2
                        ndata.axis2.itype = self.itype % 2
            if ndata.dim == 3:
                ndata.axis1.itype = self.itype // 4
                ndata.axis2.itype = self.itype // 2 % 2
                ndata.axis3.itype = self.itype % 4
            ndata.diffaxis = self.copydiffaxesfromheader()
            self.data = ndata
            self.data_valid = True

    def save(self):
        """save the NPKdata to the file"""
        if not self.header_valid:
            raise Exception('header not set')
        if not self.data_valid:
            raise Exception('buffer data not set')
        self.file = open(self.fname, 'w')
        self.fileB = open(self.fname, 'wb')
        self.writec()
        self.close()

    def read_header(self):
        """
        return a dictionnary of the file header
        internal use
        """
        self.fileB.seek(0)
        buf = self.fileB.read(self.headersize).decode()
        self.fileB.seek(0)
        dic = {}
        for line in buf.split('\n'):
            lsp = re.split('(?<!\\\\)=', line, 1)
            if len(lsp) == 2:
                dkey = re.sub('\\\\=', '=', lsp[0])
                fval = re.sub('\\\\=', '=', lsp[1])
                dic[dkey.strip()] = fval.strip()
            return dic

    def write_header_line(self, key):
        """
        write into the header the entry key
        returns the number of byte written
        internal use
        """
        l = '%-12s = %s\n' % (key, self.header[key])
        self.fileB.write(l.encode())
        if self.debug > 0:
            print(l, end=' ')
        return len(l)

    def setup_header(self):
        """setup file header, from self.data"""
        h = {}
        h['Cacheversion'] = '2'
        h['Cacherelease'] = '0'
        h['Byteorder'] = 'big_endian'
        h['Dim'] = '%d' % self.data.dim
        h['Freq'] = '%f' % self.data.frequency
        it = 0
        for ax in range(self.data.dim):
            try:
                axis = self.data.axes(ax + 1)
                it = it + axis.itype * 2 ** (self.data.dim - ax - 1)
                if self.debug > 0:
                    print('ICI', ax, axis.itype * 2 ** (self.data.dim - ax - 1), it)
            except:
                print("we don't have data axis")
                axis = None
            else:
                if axis:
                    for key, param, def_val in (('Dim', 'size', 64), ('Offset', 'offset', 0.0),
                                                ('Freq', 'frequency', 1.0), ('Specw', 'specwidth', 1.0)):
                        val = getattr(axis, param, def_val)
                        h['%s%d' % (key, ax + 1)] = val

        else:
            try:
                h['Dmin'] = '%f' % self.data.diffaxis.dmin
                h['Dmax'] = '%f' % self.data.diffaxis.dmax
                h['Dfactor'] = '%f' % self.data.diffaxis.dfactor
            except:
                h['Dmin'] = 1.0
                h['Dmax'] = 10.0
                h['Dfactor'] = 1.0
            else:
                h['Type'] = '%d' % it

        if self.data.dim == 1:
            h['Szblk1'] = '1024'
            h['Nbblock1'] = '%d' % (self.data.axis1.size // 1024)
        else:
            if self.data.dim == 2:
                sz12 = float(self.data.axis2.size) / self.data.axis1.size
                n2 = 1
                n1 = BLOCKIO // 4
                while float(n2) // n1 < sz12:
                    if n1 > 1:
                        n1 = n1 // 2
                        n2 = n2 * 2

                if self.debug > 0:
                    print('si1 x si2 : %d %d   n1 x n2 : %d %d' % (self.data.axis1.size, self.data.axis2.size, n1, n2))
                h['Szblk1'] = '%d' % n1
                h['Szblk2'] = '%d' % n2
                h['Nbblock1'] = '%d' % (1 + (self.data.axis1.size - 1) // n1)
                h['Nbblock2'] = '%d' % (1 + (self.data.axis2.size - 1) // n2)
            else:
                if self.data.dim == 3:
                    sz12 = float(self.data.axis2.size * self.data.axis3.size) // (self.data.axis1.size * self.data.axis1.size)
                    n1 = BLOCKIO // 4
                    n2 = 1
                    n3 = 1
                    while float(n2 * n3) / (n1 * n1) < sz12:
                        if n1 > 1:
                            n1 = n1 // 2
                            n2 = n2 * 2

                    sz12 = float(self.data.axis3.size) / self.data.axis1.size
                    while float(n3) / n2 < sz12:
                        if n2 > 1:
                            n2 = n2 // 2
                            n3 = n3 * 2

                    if self.debug > 0:
                        print('si1 x si2 x si3: %d %d %d   n1 x n2 x n3 : %d %d %d' % (self.data.axis1.size, self.data.axis2.size, self.data.axis3.size, n1, n2, n3))
                    h['Szblk1'] = '%d' % n1
                    h['Szblk2'] = '%d' % n2
                    h['Szblk3'] = '%d' % n3
                    h['Nbblock1'] = '%d' % (1 + (self.data.axis1.size - 1) // n1)
                    h['Nbblock2'] = '%d' % (1 + (self.data.axis2.size - 1) // n2)
                    h['Nbblock3'] = '%d' % (1 + (self.data.axis3.size - 1) // n3)
                self.header = h

    def write_header(self):
        """
        write file header
        setup_header() should have been called first
        """
        self.fileB.seek(0)
        len_so_far = 0
        l = 'HeaderSize   = %d\n' % HEADERSIZE
        self.fileB.write(l.encode())
        len_so_far = len_so_far + len(l)
        for k in self.header.keys():
            len_so_far = len_so_far + self.write_header_line(k)
        else:
            self.fileB.write(b'0' * (HEADERSIZE - len_so_far))

    def load_header(self):
        """load the header from file and set-up every thing"""
        if not self.header_valid:
            self.header = self.read_header()
            self.header_valid = True

    def close(self):
        """ closes the associated file"""
        self.file.close()
        self.fileB.close()

    @property
    def dim(self):
        """dimensionality of the dataset 1 2 or 3"""
        return int(self.header['Dim'])

    @property
    def size1(self):
        """size along the F1 axis (either 1D, or slowest varyong axis in nD)"""
        return int(self.header['Dim1'])

    @property
    def size2(self):
        """size along the F2 axis (fastest varying in 2D)"""
        return int(self.header['Dim2'])

    @property
    def size3(self):
        """size along the F3 axis (fastest varying in 3D)"""
        return int(self.header['Dim3'])

    @property
    def szblock1(self):
        """size of data block on disk along F1 axis"""
        return int(self.header['Szblk1'])

    @property
    def szblock2(self):
        """size of data block on disk along F2 axis"""
        return int(self.header['Szblk2'])

    @property
    def szblock3(self):
        """size of data block on disk along F3 axis"""
        return int(self.header['Szblk3'])

    @property
    def nblock1(self):
        """number of data block on disk along F1 axis"""
        return int(self.header['Nbblock1'])

    @property
    def nblock2(self):
        """number of data block on disk along F2 axis"""
        return int(self.header['Nbblock2'])

    @property
    def nblock3(self):
        """number of data block on disk along F3 axis"""
        return int(self.header['Nbblock3'])

    @property
    def itype(self):
        """
        Real/complex type of the dataset
        in 1D :     0 : real  1: complex
        in 2D :     0 : real on both; 
                    1 : complex on F2
                    2 : complex on F1
                    3 : complex on both
        in 3D :     0 : real on all; 
                    1 : complex on F3
                    2 : complex on F2
                    3 : complex on F3-F2
                    4 : complex on F1
                    5 : complex on F1-F3
                    6 : complex on F1-F2
                    7 : complex on all
        """
        return int(self.header['Type'])

    @property
    def byte_order(self):
        """pour intel"""
        try:
            if self.header['Byteorder'] == 'big_endian':
                r = False
            else:
                r = True
        except KeyError:
            r = True
        else:
            return r

    def readc(self):
        """
        read a file in Gifa format, and returns the binary buffer as a numpy array
        internal use - use load()
        """
        import array
        self.load_header()
        self.fileB.seek(self.headersize)
        if self.dim == 1:
            print('loading 1D')
            sz = self.size1
            fbuf = self.fileB.read(4 * sz)
            abuf = array.array('f', fbuf)
            if self.byte_order:
                abuf.byteswap()
            fbuf = np.empty((sz,), dtype='float_')
            fbuf[:] = abuf[:]
        else:
            if self.dim == 2:
                print('loading 2D')
                sz1 = self.size1
                sz2 = self.size2
                if self.debug > 0:
                    print('2D', sz1, sz2)
                fbuf = np.empty((sz1, sz2))
                i1 = 0
                i2 = 0
                if self.debug > 0:
                    print('sz', self.szblock1, self.szblock2)
                    print('nb', self.nblock1, self.nblock2)
                for b1 in xrange(self.nblock1):
                    for b2 in xrange(self.nblock2):
                        tbuf = self.fileB.read(4 * self.szblock1 * self.szblock2)
                        abuf = array.array('f', tbuf)
                        if self.byte_order:
                            abuf.byteswap()
                        imax = min(i1 + self.szblock1, sz1) - i1
                        for i in xrange(imax):
                            jmax = min(i2 + self.szblock2, sz2) - i2
                            fbuf[i1 + i, i2:i2 + jmax] = abuf[i * self.szblock2:i * self.szblock2 + jmax]
                        else:
                            i2 = i2 + self.szblock2

                    else:
                        i2 = 0
                        i1 = i1 + self.szblock1

            else:
                if self.dim == 3:
                    print('reading 3D')
                    print(' A VERIFIER')
                    sz1 = self.size1
                    sz2 = self.size2
                    sz3 = self.size3
                    fbuf = np.empty((sz1, sz2, sz3))
                    print('3D:', sz1, sz2, sz3)
                    i1 = 0
                    i2 = 0
                    i3 = 0
                    if self.debug > 0:
                        print('3D:', sz1, sz2, sz3)
                    for b1 in xrange(self.nblock1):
                        for b2 in xrange(self.nblock2):
                            for b3 in xrange(self.nblock3):
                                tbuf = self.fileB.read(4 * self.szblock1 * self.szblock2 * self.szblock3)
                                abuf = array.array('f', tbuf)
                                if self.byte_order:
                                    abuf.byteswap()
                                imax = min(i1 + self.szblock1, sz1) - i1
                                for i in xrange(imax):
                                    jmax = min(i2 + self.szblock2, sz2) - i2
                                    for j in xrange(jmax):
                                        kmax = min(i3 + self.szblock3, sz3) - i3
                                        fbuf[i1 + i, i2 + i, i3:i3 + kmax] = abuf[i * self.szblock3:i * self.szblock3 + kmax]
                                    else:
                                        i3 = i3 + self.szblock3

                                else:
                                    i3 = 0
                                    i1 = i1 + self.szblock1
                                    i2 = i2 + self.szblock2

                return fbuf

    def writec(self):
        """
        write a file in Gifa format
        internal use - use save()
        """
        self.write_header()
        self.fileB.seek(self.headersize)
        if self.dim == 1:
            self.fileB.write(self.data.buffer.astype('float32').tostring())
        else:
            if self.dim == 2:
                print('writing 2D')
                sz1 = self.size1
                sz2 = self.size2
                if self.debug > 0:
                    print('2D:', sz1, sz2)
                i1 = 0
                i2 = 0
                fbuf = np.zeros((BLOCKIO // 4,), dtype='float32')
                for b1 in xrange(self.nblock1):
                    for b2 in xrange(self.nblock2):
                        imax = min(i1 + self.szblock1, sz1) - i1
                        for i in xrange(imax):
                            jmax = min(i2 + self.szblock2, sz2) - i2
                            fbuf[i * self.szblock2:i * self.szblock2 + jmax] = self.data.buffer[i1 + i, i2:i2 + jmax]
                        else:
                            self.fileB.write(fbuf.tostring())
                            i2 = i2 + self.szblock2

                    else:
                        i2 = 0
                        i1 = i1 + self.szblock1

            else:
                if self.dim == 3:
                    print('writing 3D')
                    print(' A VERIFIER')
                    sz1 = self.size1
                    sz2 = self.size2
                    sz3 = self.size3
                    if self.debug > 0:
                        print('3D:', sz1, sz2, sz3)
                    i1 = 0
                    i2 = 0
                    i3 = 0
                    fbuf = np.zeros((BLOCKIO // 4,), dtype='float32')
                    print(self.nblock1, self.nblock2, self.nblock3)
                    for b1 in xrange(self.nblock1):
                        for b2 in xrange(self.nblock2):
                            for b3 in xrange(self.nblock3):
                                imax = min(i1 + self.szblock1, sz1) - i1
                                for i in xrange(imax):
                                    jmax = min(i2 + self.szblock2, sz2) - i2
                                    for j in xrange(jmax):
                                        kmax = min(i3 + self.szblock3, sz3) - i3
                                        fbuf[i * self.szblock2 + j * self.szblock3:i * self.szblock2 + j * self.szblock3 + kmax] = self.data.buffer[i1 + i, i2 + 1, i3:i3 + kmax]
                                    else:
                                        self.fileB.write(fbuf.tostring())
                                        i3 = i3 + self.szblock3

                                else:
                                    i3 = 0
                                    i1 = i1 + self.szblock1
                                    i2 = i2 + self.szblock2


class GifaFileTests(unittest.TestCase):
    __doc__ = '  - Testing GifaFile on various 1D and 2D files - '
    verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def test_read(self):
        """ - testing read capacities - """
        from ..Tests import filename, directory
        self.announce()
        name1D = filename('proj.gs1')
        name2D = filename('dosy-cluster2.gs2')
        name2D_little_endian = filename('dosy-cluster2-corr.gs2')
        G = GifaFile(name1D, 'r')
        G.load_header()
        self.assertEqual(G.dim, 1)
        self.assertEqual(G.header['Spec_date'], '2006-05-06')
        G.load()
        B = G.get_data()
        self.assertAlmostEqual(B.buffer[0], 1869.4309082)
        self.assertAlmostEqual(B.buffer.max(), 603306.75)
        G.close()
        G = GifaFile(name2D, 'r')
        G.load_header()
        self.assertEqual(G.dim, 2)
        G.load()
        B = G.get_data()
        G.close()
        self.assertEqual(B.buffer[(0, 0)], 0.0)
        self.assertAlmostEqual(B.buffer[(133, 1101)], 5164615.5)
        self.assertAlmostEqual(B.buffer.max(), 6831767.0)
        G = GifaFile(name2D_little_endian, 'r')
        G.load_header()
        self.assertEqual(G.dim, 2)
        G.load()
        B = G.get_data()
        G.close()
        self.assertEqual(B.buffer[(0, 0)], 0.0)
        self.assertAlmostEqual(B.buffer[(133, 1101)], 5164615.5)
        self.assertAlmostEqual(B.buffer.max(), 6831767.0)

    def test_write1D(self):
        """ - test 1D write capacities -"""
        import os
        from ..Tests import filename
        self.announce()
        nameout = filename('test_write.gs1')
        G = GifaFile(nameout, 'w')
        x = np.arange(1024) / 1000.0
        fid = np.zeros_like(x)
        LB = 5.0
        for i in range(1, 6):
            fid = fid + i * 20 * np.exp(2 * i * complex(0.0, 432.1) * x) * np.exp(-LB * x)
        else:
            print('***', fid[10])
            B = NMR.NMRData(buffer=fid)
            B.axis1 = NMR.NMRAxis(size=2048, specwidth=1000, offset=0.0, frequency=400.0, itype=1)
            G.set_data(B)
            G.save()
            G.close()
            G2 = GifaFile(nameout, 'r')
            B2 = G2.get_data()
            G2.close()
            print('===============\n', B2.report())
            self.assertEqual(B2.axis1.itype, 1)
            self.assertAlmostEqual((B2.buffer[20]), 18.7938525625, places=5)
            self.assertAlmostEqual((B2.buffer[21]), (-51.1309912819), places=5)

    def test_write2D(self):
        """ - testing 2D read/write capacities - """
        from ..Tests import filename
        self.announce()
        G = GifaFile(filename('dosy-cluster2.gs2'), 'r')
        G.load()
        A = G.get_data()
        A.buffer *= 3
        print(type(A))
        G.close()
        del G
        nameout = filename('test_write2D2.gs2')
        H = GifaFile(nameout, 'w')
        H.set_data(A)
        H.save()
        H.close()
        GG = GifaFile(nameout, 'r')
        GG.load()
        GG.close()
        B = GG.get_data()
        os.unlink(nameout)

    def base(self):
        """test basic function"""
        from ..Tests import filename
        nameout = filename('toto.gs2')
        try:
            os.unlink(nameout)
        except:
            pass
        else:
            dd = 2 * np.ones((508, 2000))
            print(dd.shape)
            H = GifaFile(nameout, 'w')
            A = npkd.NPKData(buffer=dd)
            H.set_data(A)
            H.save()
            H.close()
            GG = GifaFile(nameout, 'r')
            GG.debug = 2
            GG.load()
            GG.close()
            B = GG.get_data()
            print(A.buffer.min(), B.buffer.min(), B.buffer.argmin())
            print(A.buffer.max(), B.buffer.max())
            print(A.buffer.shape, B.buffer.shape)
            os.unlink(nameout)


if __name__ == '__main__':
    unittest.main()