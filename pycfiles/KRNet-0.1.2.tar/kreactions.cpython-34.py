# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: krnet/kreactions.py
# Compiled at: 2015-07-06 23:46:09
# Size of source mod 2**32: 1062 bytes
import os.path, sys
from kreaction import KReaction

class KReactions:

    def __init__(self, fn=None):
        self.reacts = []
        if fn != None and os.path.exists(fn):
            fi = open(fn, 'r')
            rec = []
            for ln in fi:
                if ln.startswith('///'):
                    rec.append(ln.strip())
                    kr = KReaction(rec)
                    self.reacts.append(kr)
                    del rec[:]
                else:
                    rec.append(ln.strip())

        else:
            print('File does not exist!!')
            sys.exit()

    def __len__(self):
        return len(self.reacts)

    def __getitem__(self, i):
        return self.reacts[i]

    def __setitem__(self, i, j):
        self.reacts[i] = j

    def set_reactions(self, li):
        self.reacts = li

    def uniq_reactions(self):
        urids = []
        ureacts = []
        rids = []
        for i in range(len(self.reacts)):
            rids.append(self.reacts[i].id())

        if len(rids) < 1:
            return ureacts
        urids.append(rids[0])
        for r in rids:
            if r not in urids:
                urids.append(r)
                continue

        for ur in urids:
            ureacts.append(self.reacts[rids.index(ur)])

        return ureacts