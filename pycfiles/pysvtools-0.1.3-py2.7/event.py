# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pysvtools/models/event.py
# Compiled at: 2015-11-16 18:25:06
from __future__ import print_function
import hashlib
__desc__ = ''
__author__ = 'Wai Yi Leung <w.y.leung@lumc.nl>'

class Event(object):
    centerpoint_flanking = 100

    def __init__(self, chrA, chrApos, chrB, chrBpos, sv_type=None, cp_flank=None, dp=0, svmethod=''):
        (self.chrA, self.chrApos), (self.chrB, self.chrBpos) = sorted([(chrA, chrApos), (chrB, chrBpos)])
        self.chrApos = int(self.chrApos)
        self.chrBpos = int(self.chrBpos)
        self.seen = False
        self.matched_in = None
        self.svmethod = svmethod
        self.support = 0
        _vChr = [
         self.chrA, self.chrB]
        _vChr.sort()
        self.virtualChr = ('').join(_vChr)
        self.centerpoint = self.get_centerpoint
        self.sv_type = sv_type
        self.centerpointFlanking = cp_flank or self.centerpoint_flanking
        self.dp = dp
        self._hash = None
        return

    @property
    def get_centerpoint(self):
        cnt = int(self.size / 2)
        positions = [self.chrApos, self.chrBpos]
        positions.sort()
        centerpoint = positions[0] + cnt
        return centerpoint

    @property
    def size(self):
        positions = [self.chrApos, self.chrBpos]
        positions.sort()
        return abs(positions[1] - positions[0])

    def __eq__(self, other):
        if not self.virtualChr == other.virtualChr:
            return False
        if abs(self.centerpoint - other.centerpoint) > self.centerpointFlanking:
            return False
        centerpointA = self.centerpoint
        centerpointB = other.centerpoint
        lftA = centerpointA - self.centerpointFlanking
        rgtA = centerpointA + self.centerpointFlanking
        lftB = centerpointB - self.centerpointFlanking
        rgtB = centerpointB + self.centerpointFlanking
        if lftB < rgtA < rgtB:
            return True
        if lftB < lftA < rgtB:
            return True
        if lftB > lftA and rgtB < rgtA or lftB < lftA and rgtB > rgtA:
            return True
        return False

    def naiveEQ(self, other):
        pass

    @property
    def vcf_alt(self):
        if self.chrA == self.chrB and self.sv_type != 'ITX':
            return '.'
        return ('N[{}:{}[').format(self.chrB, self.chrBpos)

    @property
    def hexdigest(self):
        if not self._hash:
            self._hash = hashlib.sha1(str(self)).hexdigest()
        return self._hash

    def __repr__(self):
        return ('<Event {0}:{1}-{2}:{3}>').format(self.chrA, self.chrApos, self.chrB, self.chrBpos)

    def __str__(self):
        if self.chrA == self.chrB:
            fmtstring = '{0}:{1}-{3}'
        else:
            fmtstring = '{0}:{1}-{2}:{3}'
        return fmtstring.format(self.chrA, self.chrApos, self.chrB, self.chrBpos)

    @property
    def bedRow(self):
        if self.chrA == self.chrB:
            fmtstring = '{0}\t{1}\t{3}\tindel'
        else:
            fmtstring = '{0}\t{1}\t{4}\tctx\n{2}\t{3}\t{5}\tctx'
        return fmtstring.format(self.chrA, self.chrApos, self.chrB, self.chrBpos, self.chrApos + 100, self.chrBpos + 100)