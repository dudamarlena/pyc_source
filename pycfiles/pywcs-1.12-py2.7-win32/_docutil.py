# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywcs\_docutil.py
# Compiled at: 2014-03-13 12:23:51
"""
pywcs-specific utilities for generating boilerplate in docstrings.
"""
from __future__ import division

def _fix(content, indent=0):
    lines = content.split('\n')
    indent = '\n' + ' ' * indent
    return indent.join(lines)


def TWO_OR_THREE_ARGS(out_type, naxis, indent=0):
    return _fix('Either two or three arguments may be provided.\n\n    - 2 arguments: An *N* x *%s* array of *x*- and *y*-coordinates, and\n      an *origin*.\n\n    - 3 arguments: 2 one-dimensional arrays of *x* and *y*\n      coordinates, and an *origin*.\n\nHere, *origin* is the coordinate in the upper left corner of the\nimage.  In FITS and Fortran standards, this is 1.  In Numpy and C\nstandards this is 0.\n\nReturns the %s.  If the input was a single array and\norigin, a single array is returned, otherwise a tuple of arrays is\nreturned.' % (naxis, out_type), indent)


def ORIGIN(indent=0):
    return _fix('\n- *origin*: int. Specifies the origin of pixel values.  The Fortran and\n  FITS standards use an origin of 1.  Numpy and C use array indexing\n  with origin at 0.\n', indent)


def RA_DEC_ORDER(indent=0):
    return _fix('\nAn optional keyword argument, *ra_dec_order*, may be provided, that\nwhen `True` will ensure that sky coordinates are always given and\nreturned in as (*ra*, *dec*) pairs, regardless of the order of the\naxes specified by the in the ``CTYPE`` keywords.\n', indent)