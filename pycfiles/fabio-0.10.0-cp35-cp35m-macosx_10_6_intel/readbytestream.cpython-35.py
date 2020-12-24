# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/readbytestream.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 3865 bytes
"""Reads a bytestream

Authors: Jon Wright    Henning O. Sorensen & Erik Knudsen
         ESRF          Risoe National Laboratory
"""
from __future__ import with_statement, print_function, division
import logging, numpy
logger = logging.getLogger(__name__)
DATATYPES = {('int', 'n', 1): numpy.uint8, 
 ('int', 'n', 2): numpy.uint16, 
 ('int', 'n', 4): numpy.uint32, 
 ('int', 'y', 1): numpy.int8, 
 ('int', 'y', 2): numpy.int16, 
 ('int', 'y', 4): numpy.int32, 
 ('float', 'y', 4): numpy.float32, 
 ('double', 'y', 4): numpy.float64}

def readbytestream(fil, offset, x, y, nbytespp, datatype='int', signed='n', swap='n', typeout=numpy.uint16):
    """
    Reads in a bytestream from a file (which may be a string indicating
    a filename, or an already opened file (should be "rb"))
    offset is the position (in bytes) where the pixel data start
    nbytespp = number of bytes per pixel
    type can be int or float (4 bytes pp) or double (8 bytes pp)
    signed: normally signed data 'y', but 'n' to try to get back the
    right numbers when unsigned data are converted to signed
    (python once had no unsigned numeric types.)
    swap, normally do not bother, but 'y' to swap bytes
    typeout is the numpy type to output, normally uint16,
    but more if overflows occurred
    x and y are the pixel dimensions

    TODO : Read in regions of interest

    PLEASE LEAVE THE STRANGE INTERFACE ALONE -
    IT IS USEFUL FOR THE BRUKER FORMAT
    """
    tin = 'dunno'
    length = nbytespp * x * y
    if datatype in ('float', 'double'):
        signed = 'y'
    key = (datatype, signed, nbytespp)
    try:
        tin = DATATYPES[key]
    except KeyError:
        logger.warning('datatype, signed, nbytespp: %s', str(key))
        raise Exception('Unknown combination of types to readbytestream')

    if hasattr(fil, 'read') and hasattr(fil, 'seek'):
        infile = fil
        opened = False
    else:
        infile = open(fil, 'rb')
        opened = True
    infile.seek(offset)
    data = numpy.frombuffer(infile.read(length), tin)
    arr = numpy.array(numpy.reshape(data, (x, y)), typeout)
    if swap == 'y':
        arr.byteswap(True)
    if opened:
        infile.close()
    return arr