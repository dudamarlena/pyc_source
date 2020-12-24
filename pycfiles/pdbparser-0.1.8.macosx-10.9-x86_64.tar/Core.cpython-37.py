# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/IO/Core.py
# Compiled at: 2019-02-16 11:54:43
# Size of source mod 2**32: 7859 bytes
"""
This module provides classes used in the Input-Output processes.

.. inheritance-diagram:: pdbparser.IO.Core
    :parts: 2

"""
from __future__ import print_function
from copy import copy
import os, re, struct, numpy as np
from pdbparser.log import Logger

class FortranBinaryFile(object):
    __doc__ = '\n    Sets up a Fortran binary file reader.\n    '

    def __init__(self, filename, byte_order='='):
        """
        The constructor.

        :Parameters:
            #. filename (string): the binary input file
            #. byte_order (string): the byte order to read the binary file. Must be any of '@', '=', '<', '>' or '!'.
        """
        self._FortranBinaryFile__file = file(filename, 'rb')
        self._FortranBinaryFile__byteOrder = byte_order
        self._FortranBinaryFile__fileSize = os.path.getsize(filename)

    def __iter__(self):
        return self

    @property
    def fileSize(self):
        return self._FortranBinaryFile__fileSize

    @property
    def currentPosition(self):
        return self._FortranBinaryFile__file.tell()

    def next(self):
        data = self._FortranBinaryFile__file.read(4)
        if not data:
            raise StopIteration
        reclen = struct.unpack(self._FortranBinaryFile__byteOrder + 'i', data)[0]
        data = self._FortranBinaryFile__file.read(reclen)
        reclen2 = struct.unpack(self._FortranBinaryFile__byteOrder + 'i', self._FortranBinaryFile__file.read(4))[0]
        assert reclen == reclen2, Logger.error('data format not respected')
        return data

    def skip_record(self):
        data = self._FortranBinaryFile__file.read(4)
        reclen = struct.unpack(self._FortranBinaryFile__byteOrder + 'i', data)[0]
        self._FortranBinaryFile__file.seek(reclen, 1)
        reclen2 = struct.unpack(self._FortranBinaryFile__byteOrder + 'i', self._FortranBinaryFile__file.read(4))[0]
        assert reclen == reclen2, Logger.error('data format not respected')

    def get_record(self, format, repeat=False):
        """
        Reads a record of the binary file.

        :Parameters:
            #. format (string): the format corresponding to the binray structure to read.
            #. repeat (boolean): if True, will repeat the reading.
        """
        try:
            data = self.next()
        except StopIteration:
            raise Logger.error('Unexpected end of file')

        if repeat:
            unit = struct.calcsize(self._FortranBinaryFile__byteOrder + format)
            assert len(data) % unit == 0, Logger.error('wrong data length')
            format = len(data) / unit * format
        try:
            return struct.unpack(self._FortranBinaryFile__byteOrder + format, data)
        except:
            raise Logger.error('not able to unpack data')


class DCDFile(object):
    __doc__ = '\n    sets up a DCD file reader.\n    '

    def __init__(self, filename):
        """
        The constructor.

        :Parameters:
            #. filename (string): the binary input file
        """
        self.charmmTimeToPs = 0.0488882129084
        self._DCDFile__byteOrder = None
        data = file(filename, 'rb').read(4)
        for byte_order in ('<', '>'):
            reclen = struct.unpack(byte_order + 'i', data)[0]
            if reclen == 84:
                self._DCDFile__byteOrder = byte_order
                break

        if self._DCDFile__byteOrder is None:
            raise Logger.error('%s is not a DCD file' % filename)
        self._DCDFile__binary = FortranBinaryFile(filename, self._DCDFile__byteOrder)
        header_data = self._DCDFile__binary.next()
        if header_data[:4] != 'CORD':
            raise Logger.error('%s is not a DCD file' % filename)
        self.header = struct.unpack(self._DCDFile__byteOrder + '9id9i', header_data[4:])
        self.numberOfConfigurations = self.header[0]
        self.istart = self.header[1]
        self.nsavc = self.header[2]
        self.namnf = self.header[8]
        self.charmmVersion = self.header[(-1)]
        self.has_pbc_data = False
        self.has_4d = False
        if self.charmmVersion != 0:
            self.header = struct.unpack(self._DCDFile__byteOrder + '9if10i', header_data[4:])
            if self.header[10] != 0:
                self.has_pbc_data = True
            if self.header[11] != 0:
                self.has_4d = True
        self.delta = self.header[9] * self.charmmTimeToPs
        title_data = self._DCDFile__binary.next()
        nlines = struct.unpack(self._DCDFile__byteOrder + 'i', title_data[:4])[0]
        assert len(title_data) == 80 * nlines + 4, Logger.error('%s is not a DCD file' % filename)
        title_data = title_data[4:]
        title = []
        for i in range(nlines):
            title.append(title_data[:80].rstrip())
            title_data = title_data[80:]

        self.title = '\n'.join(title)
        self.natoms = self._DCDFile__binary.get_record('i')[0]
        if self.namnf > 0:
            raise Logger.error('NAMD converter can not handle fixed atoms yet')

    @property
    def fileSize(self):
        return self._DCDFile__binary.fileSize

    @property
    def currentPosition(self):
        return self._DCDFile__binary.currentPosition

    def read_step(self):
        """
        Reads a configuration of the DCD file.
        """
        if self.has_pbc_data:
            unit_cell = np.array((self._DCDFile__binary.get_record('6d')), dtype=(np.float))
            a, gamma, b, beta, alpha, c = unit_cell
            if -1.0 < alpha < 1.0:
                if -1.0 < beta < 1.0:
                    if -1.0 < gamma < 1.0:
                        alpha = 0.5 * np.pi - np.arcsin(alpha)
                        beta = 0.5 * np.pi - np.arcsin(beta)
                        gamma = 0.5 * np.pi - np.arcsin(gamma)
            unit_cell = (
             a, b, c, alpha, beta, gamma)
        else:
            unit_cell = None
        format = '%df' % self.natoms
        x = np.array((self._DCDFile__binary.get_record(format)), dtype=(np.float32))
        y = np.array((self._DCDFile__binary.get_record(format)), dtype=(np.float32))
        z = np.array((self._DCDFile__binary.get_record(format)), dtype=(np.float32))
        if self.has_4d:
            self._DCDFile__binary.skip_record()
        return (
         unit_cell, x, y, z)

    def skip_step(self):
        """
        Skips a configuration of the DCD file.
        """
        nrecords = 3
        if self.has_pbc_data:
            nrecords += 1
        if self.has_4d:
            nrecords += 1
        for i in range(nrecords):
            self._DCDFile__binary.skip_record()

    def __iter__(self):
        return self

    def next(self):
        try:
            return self.readStep()
        except:
            raise StopIteration


class Converter(object):

    def __init__(self):
        self._Converter__previousStep = None

    def status(self, step, totalSteps, logFrequency=10):
        """
        This method is used to log converting status.

        :Parameters:
            #. step (int): The current step number
            #. logFrequency (float): the frequency of status logging. its a percent number.
        """
        if not step:
            Logger.info('%s --> converting started' % self.__class__.__name__)
        else:
            if step == totalSteps:
                Logger.info('%s --> converting finished' % self.__class__.__name__)
            else:
                actualPercent = int(float(step) / float(totalSteps) * 100)
                if self._Converter__previousStep is not None:
                    previousPercent = int(float(self._Converter__previousStep) / float(totalSteps) * 100)
                else:
                    previousPercent = -1
                if actualPercent / logFrequency != previousPercent / logFrequency:
                    Logger.info('%s --> %s%% completed. %s left out of %s' % (self.__class__.__name__, actualPercent, totalSteps - step, totalSteps))
        self._Converter__previousStep = step