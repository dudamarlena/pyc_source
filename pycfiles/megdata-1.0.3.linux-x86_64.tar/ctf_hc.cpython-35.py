# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/megdata/ctf_hc.py
# Compiled at: 2018-10-24 06:01:48
# Size of source mod 2**32: 3624 bytes
import os, re
from numpy import array
from .common import *

class CTFHCFile(object):

    @classmethod
    def from_file(cls, filename):
        """
        Read a CTF HC file from a filename
        """
        f = open(filename, 'r')
        ret = cls()
        ret.standard_nasion = None
        ret.standard_leftear = None
        ret.standard_rightear = None
        ret.dewar_nasion = None
        ret.dewar_leftear = None
        ret.dewar_rightear = None
        ret.head_nasion = None
        ret.head_leftear = None
        ret.head_rightear = None
        r = re.compile('(standard|measured) (left ear|right ear|nasion) coil position relative to (dewar|head) \\(cm\\):')
        rp = re.compile('\\s+([xyz]) = (-?\\d+.?\\d*)\\s+')
        while 1:
            txt = f.readline()
            if len(txt) == 0:
                break
            data = r.search(txt.strip())
            if data is not None and len(data.groups()) == 3:
                x = None
                y = None
                z = None
                xt = f.readline()
                yt = f.readline()
                zt = f.readline()
                xdat = rp.search(xt)
                ydat = rp.search(yt)
                zdat = rp.search(zt)
                if xdat is not None and len(xdat.groups()) == 2 and xdat.groups()[0] == 'x':
                    x = float(xdat.groups()[1])
                if ydat is not None and len(ydat.groups()) == 2 and ydat.groups()[0] == 'y':
                    y = float(ydat.groups()[1])
                if zdat is not None and len(zdat.groups()) == 2 and zdat.groups()[0] == 'z':
                    z = float(zdat.groups()[1])
                if x is None or y is None or z is None:
                    raise RuntimeError('Cannot read co-ordinates in HC file')
                coord = array([x, y, z])
                sm = data.groups()[0]
                pos = data.groups()[1]
                rel = data.groups()[2]
                if sm == 'standard' and rel == 'dewar':
                    if pos == 'nasion':
                        ret.standard_nasion = coord
                    else:
                        if pos == 'left ear':
                            ret.standard_leftear = coord
                        else:
                            if pos == 'right ear':
                                ret.standard_rightear = coord
                            else:
                                raise RuntimeError('Unknown position %s in HC file' % pos)
                else:
                    if sm == 'measured' and rel == 'dewar':
                        if pos == 'nasion':
                            ret.dewar_nasion = coord
                        else:
                            if pos == 'left ear':
                                ret.dewar_leftear = coord
                            else:
                                if pos == 'right ear':
                                    ret.dewar_rightear = coord
                                else:
                                    raise RuntimeError('Unknown position %s in HC file' % pos)
                    else:
                        if sm == 'measured' and rel == 'head':
                            if pos == 'nasion':
                                ret.head_nasion = coord
                            else:
                                if pos == 'left ear':
                                    ret.head_leftear = coord
                                else:
                                    if pos == 'right ear':
                                        ret.head_rightear = coord
                                    else:
                                        raise RuntimeError('Unknown position %s in HC file' % pos)
                        else:
                            raise RuntimeError('Unknown target %s relarive to %s in HC file' % (sm, rel))

        return ret