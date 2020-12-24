# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Networks/Tools.py
# Compiled at: 2007-08-31 18:49:25
"""This package contains the function to generate mac addresses """
__revision__ = '$Revision$'

def MacGenerator(first, last=0, jump=1, max=16777215):
    if not isinstance(first, str):
        raise TypeError, "ERROR: macaddr must be initialized with 3 octets as first, like '52:54:00'"
    while last <= max:
        tmplast = '%6.6x' % last
        yield '%s:%0.2s:%0.2s:%0.2s' % (first,
         tmplast[0:2],
         tmplast[2:4],
         tmplast[4:6])
        last += jump


def MacSplit(macaddr):
    tmpmacaddr = macaddr.split(':')
    return ((':').join(tmpmacaddr[0:3]), (':').join(tmpmacaddr[3:6]))


def MacToInt(macaddr):
    tmpmacaddr = ('').join(macaddr.split(':'))
    return int(tmpmacaddr, 16)