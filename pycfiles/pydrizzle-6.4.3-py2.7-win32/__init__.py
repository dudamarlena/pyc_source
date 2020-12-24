# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pydrizzle\__init__.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
from stsci.tools import numerixenv
numerixenv.check()
yes = True
no = False
from .drutil import DEFAULT_IDCDIR
from math import *
from .version import *

def PyDrizzle(input, output=None, field=None, units=None, section=None, kernel=None, pixfrac=None, bits_final=0, bits_single=0, wt_scl='exptime', fillval=0.0, idckey='', in_units='counts', idcdir=DEFAULT_IDCDIR, memmap=0, dqsuffix=None, prodonly=False, shiftfile=None, updatewcs=True):
    import pydrizzle, process_input
    asndict, ivmlist, output = process_input.process_input(input, output=output, prodonly=prodonly, updatewcs=updatewcs, shiftfile=shiftfile)
    if not asndict:
        return
    else:
        p = pydrizzle._PyDrizzle(asndict, output=output, field=field, units=units, idckey=idckey, section=section, kernel=kernel, pixfrac=pixfrac, bits_single=bits_single, bits_final=bits_final, wt_scl=wt_scl, fillval=fillval, in_units=in_units, idcdir=idcdir, memmap=memmap, dqsuffix=dqsuffix)
        return p


def help():
    import pydrizzle
    print pydrizzle._PyDrizzle.__doc__