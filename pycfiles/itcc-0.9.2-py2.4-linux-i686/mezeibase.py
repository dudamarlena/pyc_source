# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/mezeibase.py
# Compiled at: 2008-04-20 13:19:45


class MezeiBase(object):
    __module__ = __name__

    def R6(self, coords, atmidx, dismat, shakedata):
        """Wrapped R6 algorithm, include R6 and shakeH"""
        shakes = [ shakedata[idx] for idx in atmidx[1:-1] ]
        for baseresult in self.__R6(coords, atmidx, dismat):
            newcoords = coords.copy()
            abs_dist = 0.0
            for (idx, newcoord) in baseresult.items():
                newcoords[idx] = newcoord
                abs_dist += sum(abs(newcoord - coords[idx]))

            if abs_dist < self.min_abs_dist:
                continue
            for (refidxs, sidechain_) in shakes:
                baseresult.update(sidechain.movesidechain(coords, newcoords, refidxs, sidechain_))

            yield baseresult