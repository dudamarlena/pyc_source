# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/DH/prosodic/lib/MeterPosition.py
# Compiled at: 2019-06-07 00:03:27
import string
from copy import copy
from Parse import Parse

class MeterPosition(Parse):

    def __init__(self, meter, meterVal):
        self.slots = []
        self.children = self.slots
        self.meter = meter
        self.constraintScores = {}
        for constraint in meter.constraints:
            self.constraintScores[constraint] = 0

        self.meterVal = meterVal
        for slot in self.slots:
            slot.meter = meterVal

        self.feat('prom.meter', meterVal == 's')

    def __copy__(self):
        other = MeterPosition(self.meter, self.meterVal)
        other.slots = self.slots[:]
        for k, v in list(self.constraintScores.items()):
            other.constraintScores[k] = copy(v)

        return other

    @property
    def has_viol(self):
        return bool(sum(self.constraintScores.values()))

    @property
    def violated(self):
        viold = []
        for c, viol in list(self.constraintScores.items()):
            if viol:
                viold += [c]

        return viold

    @property
    def isStrong(self):
        return self.meterVal.startswith('s')

    def append(self, slot):
        self.slots.append(slot)

    @property
    def meterVal2(self):
        return ('').join([ self.meterVal for x in self.slots ])

    @property
    def mstr(self):
        return ('').join([ self.meterVal for n in range(len(self.slots)) ])

    def posfeats(self):
        posfeats = {'prom.meter': []}
        for slot in self.slots:
            for k, v in list(slot.feats.items()):
                if k not in posfeats:
                    posfeats[k] = []
                posfeats[k] += [v]

            posfeats['prom.meter'] += [self.meterVal]

        for k, v in list(posfeats.items()):
            posfeats[k] = tuple(v)

        return posfeats

    def __repr__(self):
        return self.token

    @property
    def token(self):
        if not hasattr(self, '_token') or not self._token:
            token = ('.').join([ slot.token for slot in self.slots ])
            token = token.upper() if self.meterVal == 's' else token.lower()
            self._token = token
        return self._token