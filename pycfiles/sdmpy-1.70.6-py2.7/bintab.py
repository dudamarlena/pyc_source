# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdmpy/bintab.py
# Compiled at: 2019-04-03 11:16:08
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import struct, numpy

def unpacker(sdmtable):
    """Return an appropriate unpacker given an SDMBinaryTable object."""
    if sdmtable.name == b'SysPower':
        return SysPowerUnpacker(sdmtable)
    if sdmtable.name == b'Pointing':
        return PointingUnpacker(sdmtable)
    raise RuntimeError(b"Unknown binary table type: '%s'" % sdmtable.name)


class BinaryTableUnpacker(object):
    """Base class for SDM binary table unpackers.  This should not be called
    directly, because it needs a column data structure definition in order
    to be useful.  This is implemented in derived classes, e.g.
    SysPowerUnpacker for the SysPower table."""
    _unpack_byte = struct.Struct(b'>b')
    _unpack_int = struct.Struct(b'>i')
    _unpack_long = struct.Struct(b'>q')
    _unpack_float = struct.Struct(b'>f')
    _unpack_double = struct.Struct(b'>d')
    columns = []

    def __init__(self, sdmtable):
        self._sdmtable = sdmtable
        self._pos = 0
        self.table_entity = tuple(self._get_val(b'S') for i in range(5))
        self.container_entity = tuple(self._get_val(b'S') for i in range(5))
        self.nrows = self._get_val(b'i4')
        self._pos0 = self._pos
        self.row = []

    def _readtab(self, nbytes):
        result = self._sdmtable.get_bytes(self._pos, nbytes)
        if len(result) != nbytes:
            return None
        else:
            self._pos += nbytes
            return result

    def _get_val(self, dtype, optional=False, arraydims=()):
        string_val = False
        if dtype == b'i4':
            unpack = self._unpack_int
        else:
            if dtype == b'i8':
                unpack = self._unpack_long
            elif dtype == b'f4':
                unpack = self._unpack_float
            elif dtype == b'f8':
                unpack = self._unpack_double
            elif dtype == b'b':
                unpack = self._unpack_byte
            elif dtype[0] == b'S':
                unpack = None
                string_val = True
            else:
                raise RuntimeError(b"Unknown data dtype (dtype='%s')" % dtype)
            try:
                if optional:
                    has_data = self._readtab(1) != b'\x00'
                    if not has_data:
                        if string_val:
                            return b''
                        else:
                            return 0

                ndim = len(arraydims)
                if string_val:
                    ndim = 1
                dims = []
                for i in range(ndim):
                    nval = self._unpack_int.unpack_from(self._readtab(4))[0]
                    dims.append(nval)

                if string_val:
                    return self._readtab(dims[0])
                dsize = unpack.size
                if ndim:
                    ntot = numpy.product(dims)
                    return numpy.array([ unpack.unpack_from(self._readtab(dsize))[0] for i in range(ntot)
                                       ]).reshape(dims)
                return unpack.unpack_from(self._readtab(dsize))[0]
            except struct.error:
                return

        return

    @property
    def record_dtype(self):
        return [ (str(col[0]), col[2], col[3]) for col in self.columns ]

    def _blank_row(self, nrows=1):
        return numpy.zeros(nrows, dtype=self.record_dtype)

    def _unpack_row(self):
        row = self._blank_row()
        for col in self.columns:
            colname = col[0]
            isoptional = col[1]
            coldtype = col[2]
            arraydims = col[3]
            val = self._get_val(coldtype, isoptional, arraydims)
            if val is None:
                return
            if arraydims != ():
                row[0][colname][:] = val
            else:
                row[0][colname] = val

        return row

    def iterrows(self):
        self._pos = self._pos0
        more_data = True
        while more_data:
            row = self._unpack_row()
            if row is None:
                more_data = False
            else:
                yield row

        return

    def unpack(self):
        self.row = numpy.recarray(1000, dtype=self.record_dtype)
        irow = 0
        for row in self.iterrows():
            if irow == len(self.row):
                self.row = numpy.rec.array(numpy.resize(self.row, int(len(self.row) * 1.2)))
            self.row[irow] = row
            irow += 1

        self.row = numpy.rec.array(numpy.resize(self.row, irow))


class SysPowerUnpacker(BinaryTableUnpacker):
    """Unpacker for the SysPower binary table.  Currently makes some
    assumptions like there never being more than 2 measurements in
    the array-valued columns.  This is true for now for the VLA.
    """
    columns = [
     (
      b'antennaId', False, b'S32', ()),
     (
      b'spectralWindowId', False, b'S32', ()),
     (
      b'feedId', False, b'i4', ()),
     (
      b'timeMid', False, b'i8', ()),
     (
      b'interval', False, b'i8', ()),
     (
      b'numReceptor', False, b'i4', ()),
     (
      b'switchedPowerDifference', True, b'f4', (2, )),
     (
      b'switchedPowerSum', True, b'f4', (2, )),
     (
      b'requantizerGain', True, b'f4', (2, ))]


class PointingUnpacker(BinaryTableUnpacker):
    """Unpacker for binary Pointing table.  Most angle params are specified
    as 2-D arrays of angles but assumes VLA data only ever comes with 1x2 arrays
    for these."""
    columns = [
     (
      b'antennaId', False, b'S32', ()),
     (
      b'timeMid', False, b'i8', ()),
     (
      b'interval', False, b'i8', ()),
     (
      b'numSample', False, b'i4', ()),
     (
      b'encoder', False, b'f8', (1, 2)),
     (
      b'pointingTracking', False, b'b', ()),
     (
      b'usePolynomials', False, b'b', ()),
     (
      b'timeOrigin', False, b'i8', ()),
     (
      b'numTerm', False, b'i4', ()),
     (
      b'pointingDirection', False, b'f8', (1, 2)),
     (
      b'target', False, b'f8', (1, 2)),
     (
      b'offset', False, b'f8', (1, 2)),
     (
      b'pointingModelId', False, b'i4', ()),
     (
      b'overTheTop', True, b'b', ()),
     (
      b'sourceOffset', True, b'f8', (1, 2)),
     (
      b'sourceOffsetReferenceCode', True, b'i4', ()),
     (
      b'sourceOffsetEquinox', True, b'i4', ()),
     (
      b'sampledTimeInterval', True, b'i4', ()),
     (
      b'atmosphericCorrection', True, b'f8', (1, 2))]