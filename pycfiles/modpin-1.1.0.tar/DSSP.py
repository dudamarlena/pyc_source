# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/external/DSSP/DSSP.py
# Compiled at: 2018-02-02 06:38:54
"""
DSSP

author: jbonet
date:   03/2013

@oliva's lab
"""
exposed_threshold = 2.5
from SBI.data import aminoacids3to1, aminoacids_surface

class DSSP(object):
    """
    The {DSSP} stores the dssp prediction
    """

    def __init__(self, secondary_structure, accessibility, AAtype):
        global exposed_threshold
        self._ss = secondary_structure
        self._access = int(accessibility)
        self._type = AAtype
        if AAtype in aminoacids_surface:
            self._access10 = int(10 * self._access / aminoacids_surface[AAtype])
            self._accesscode = self._codifyaccess(float(self._access) / aminoacids_surface[AAtype] * 100)
        else:
            self._access10 = 1
            self._accesscode = 1
        self._exposed = self._access10 > exposed_threshold
        self._rnhoa = None
        self._enhoa = None
        self._rohna = None
        self._eohna = None
        self._rnhob = None
        self._enhob = None
        self._rohnb = None
        self._eohnb = None
        return

    @property
    def secondary_structure(self):
        return self._ss

    @property
    def aminoacid(self):
        return self._type

    @property
    def accessibility(self):
        return self._access

    @property
    def accessibility10(self):
        return self._access10

    @property
    def accesscode(self):
        return str(self._accesscode)

    @staticmethod
    @property
    def exposition_threshold():
        return exposed_threshold

    @property
    def exposed(self):
        return self._exposed

    @property
    def nhoa(self):
        return (self._rnhoa, self._enhoa)

    @property
    def ohna(self):
        return (self._rohna, self._eohna)

    @property
    def nhob(self):
        return (self._rnhob, self._enhob)

    @property
    def ohnb(self):
        return (self._rohnb, self._eohnb)

    def add_hydrogen_links(self, nhoa, ohna, nhob, ohnb):
        self._rnhoa = int(nhoa.split(',')[0].strip())
        self._enhoa = float(nhoa.split(',')[1].strip())
        self._rohna = int(ohna.split(',')[0].strip())
        self._eohna = float(ohna.split(',')[1].strip())
        self._rnhob = int(nhob.split(',')[0].strip())
        self._enhob = float(nhob.split(',')[1].strip())
        self._rohnb = int(ohnb.split(',')[0].strip())
        self._eohnb = float(ohnb.split(',')[1].strip())

    def _codifyaccess(self, value):
        value = float(value)
        if value == 0:
            return '*'
        if value > 100:
            return '?'
        if value > 0 and value <= 10:
            return '1'
        if value > 10 and value <= 20:
            return '2'
        if value > 20 and value <= 30:
            return '3'
        if value > 30 and value <= 40:
            return '4'
        if value > 40 and value <= 50:
            return '5'
        if value > 50 and value <= 60:
            return '6'
        if value > 60 and value <= 70:
            return '7'
        if value > 70 and value <= 80:
            return '8'
        if value > 80 and value <= 90:
            return '9'
        if value > 90 and value <= 100:
            return '#'