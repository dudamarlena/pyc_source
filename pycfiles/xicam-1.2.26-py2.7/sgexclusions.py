# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\sgexclusions.py
# Compiled at: 2018-08-27 17:21:06
from collections import OrderedDict
from xicam import debugtools
iseven = lambda m: not m % 2
is6multiple = lambda m: not m % 6 and m != 0
is4multiple = lambda m: not m % 4 and m != 0
is3multiple = lambda m: not m % 3 and m != 0
is2multiple = lambda m: not m % 2 and m != 0
h = lambda h, k, l: iseven(h)
k = lambda h, k, l: iseven(k)
l = lambda h, k, l: iseven(l)
hpk = lambda h, k, l: iseven(h + k)
hpl = lambda h, k, l: iseven(h + l)
kpl = lambda h, k, l: iseven(k + l)
hpkpl = lambda h, k, l: iseven(h + k + l)
kpl4n = lambda h, k, l: is4multiple(k + l)
hpl4n = lambda h, k, l: is4multiple(h + l)
hpk4n = lambda h, k, l: is4multiple(h + k)
h4n = lambda h, k, l: is4multiple(h)
k4n = lambda h, k, l: is4multiple(k)
l4n = lambda h, k, l: is4multiple(l)
twohpl4n = lambda h, k, l: is4multiple(2 * h + l)
l3n = lambda h, k, l: is3multiple(l)
l6n = lambda h, k, l: is6multiple(l)
mhpkpl3n = lambda h, k, l: is3multiple(-h + k + l)
hpl3n = lambda h, k, l: is3multiple(h + l)
hmkpl3n = lambda h, k, l: is3multiple(h - k + l)
mhpl3n = lambda h, k, l: is3multiple(-h + l)
h2n = lambda h, k, l: is2multiple(h)
k2n = lambda h, k, l: is2multiple(k)
l2n = lambda h, k, l: is2multiple(l)
kpl2n = lambda h, k, l: is2multiple(k + l)
cache = dict()

def arezeros(*args):
    if len(args) == 4:
        zh, zk, zl = args[:3]
        mh, mk, ml = args[3]
        if bool(mh) and zh or bool(mk) and zk or bool(ml) and zl:
            return False
        return True
    if len(args) == 5:
        zh, zk, zi, zl = args[:4]
        mh, mk, mi, ml = args[4]
        if bool(mh) and zh or bool(mk) and zk or bool(mi) and zi or bool(ml) and zl:
            return False
        return True


class SGClass:
    conditions = OrderedDict([])

    def check(self, m, SG):
        """
        Get the relevant exclusion rule column and then test against it.
        """
        col, m = self.getcolumn(m)
        if type(self.conditions[SG]) is not list:
            SG = self.conditions[SG]
        return self.checkcolumn(SG, col, m)

    def getcolumn(self, m):
        """
        Determine which column of the exclusion table to test with given miller indices 'm'.
        Unique SGClass subclasses may override this if there are more columns or the column conditions are unique.
        This virtual class is overridden by each crystal system.
        """
        pass

    def checkcolumn(self, SG, col, m):
        """
        Check the exclusion rules in column 'col' with miller indices 'm'.
        """
        if col is None:
            return True
        else:
            if len(m) == 4:
                m = (
                 m[0], m[1], m[3])
            SGconditions = self.conditions[SG][col]
            if type(SGconditions) is not list:
                SGconditions = [
                 SGconditions]
            for condition in SGconditions:
                if condition is not None:
                    if not condition(*m):
                        return False

            return True


class Triclinic(SGClass):
    conditions = OrderedDict([('P1', []),
     (
      'P1̅', [])])

    def check(self, m, SG):
        return True


class Monoclinic(SGClass):
    conditions = OrderedDict([('P2', [None, None, None]),
     (
      'P2₁', [None, None, k]),
     (
      'C2', [hpk, h, k]),
     (
      'A2', [kpl, l, k]),
     (
      'I2', [hpkpl, hpl, k]),
     (
      'Pm', [None, None, None]),
     (
      'Pc', [None, l, None]),
     (
      'Pa', [None, h, None]),
     (
      'Pn', [None, hpl, None]),
     (
      'Cm', [hpk, h, k]),
     (
      'Am', [hpk, h, k]),
     (
      'Im', [hpk, h, k]),
     (
      'Cc', [hpk, [h, l], k]),
     (
      'An', [kpl, [h, l], k]),
     (
      'Ia', [hpkpl, [h, l], k]),
     (
      'P2/m', [None, None, None]),
     (
      'P2₁/m', [None, None, k]),
     (
      'C2/m', [hpk, h, k]),
     (
      'A2/m', [kpl, l, k]),
     (
      'I2/m', [hpkpl, hpl, k]),
     (
      'P2/c', [None, l, None]),
     (
      'P2/a', [None, h, None]),
     (
      'P2/n', [None, hpl, None]),
     (
      'P2₁/c', [None, l, k]),
     (
      'P2₁/a', [None, h, k]),
     (
      'P2₁/n', [None, hpl, k]),
     (
      'C2/c', [hpk, [h, l], k]),
     (
      'A2/n', [kpl, [h, l], k]),
     (
      'I2/a', [hpkpl, [h, l], k])])

    def getcolumn(self, m):
        if arezeros(1, 0, 1, m):
            column = 2
        elif arezeros(0, 1, 0, m) or arezeros(1, 1, 0, m) or arezeros(0, 1, 1, m):
            column = 1
        elif arezeros(0, 0, 0, m) or arezeros(1, 0, 0, m) or arezeros(0, 0, 1, m):
            column = 0
        else:
            debugtools.frustration()
            raise ValueError
        return (
         column, m)


class Orthorhombic(SGClass):
    conditions = OrderedDict([('P222', [None, None, None, None, None, None, None]),
     (
      'P222₁', [None, None, None, None, None, None, l]),
     (
      'P22₁2', [None, None, None, None, None, k, None]),
     (
      'P2₁22', [None, None, None, None, h, None, None]),
     (
      'P2₁2₁2', [None, None, None, None, h, k, None]),
     (
      'P22₁2₁', [None, None, None, None, None, k, l]),
     (
      'P2₁22₁', [None, None, None, None, h, None, l]),
     (
      'P2₁2₁2₁', [None, None, None, None, h, k, l]),
     (
      'C222₁', [hpk, k, h, hpk, h, k, l]),
     (
      'C222', [hpk, k, h, hpk, h, k, None]),
     (
      'F222', [[hpk, hpl, kpl], [k, l], [h, l], [h, k], h, k, l]),
     (
      'I222', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'I2₁2₁2₁', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'Pmm2', [None, None, None, None, None, None, None]),
     (
      'Pm2m', [None, None, None, None, None, None, None]),
     (
      'P2mm', [None, None, None, None, None, None, None]),
     (
      'Pmc2₁', [None, None, l, None, None, None, l]),
     (
      'P2₁ma', [None, None, None, h, h, None, None]),
     (
      'Pm2₁b', [None, None, None, k, None, k, None]),
     (
      'P2₁am', [None, None, h, None, h, None, None]),
     (
      'Pcc2', [None, l, l, None, None, None, l]),
     (
      'P2aa', [None, None, h, h, h, None, None]),
     (
      'Pma2', [None, None, h, None, h, None, None]),
     (
      'Pm2a', [None, None, None, h, h, None, None]),
     (
      'P2mb', [None, None, None, h, None, k, None]),
     (
      'P2cm', [None, None, l, None, None, None, l]),
     (
      'Pca2₁', [None, l, h, None, h, None, l]),
     (
      'P2₁ab', [None, None, h, k, h, k, None]),
     (
      'P2₁ca', [None, None, h, None, h, None, l]),
     (
      'Pnc2', [None, kpl, l, None, None, k, l]),
     (
      'Pmn2₁', [None, None, hpl, None, h, None, l]),
     (
      'Pmn2₁', [None, None, hpl, None, h, None, l]),
     (
      'P2₁nm', [None, None, None, None, None, None, None]),
     (
      'Pmnm', [None, None, None, None, None, None, None]),
     (
      'P2na', [None, None, hpl, h, h, None, l]),
     (
      'Pmna', [None, None, hpl, h, h, None, l]),
     (
      'P2na', [None, None, hpl, k, h, k, l]),
     (
      'P2nm', [None, None, hpl, hpk, h, k, l]),
     (
      'Pmnn', [None, None, hpl, hpk, h, k, l]),
     (
      'Pbm2', [None, k, None, None, None, k, None]),
     (
      'Pb2₁m', [None, None, None, None, None, None, None]),
     (
      'Pbmm', [None, None, None, None, None, None, None]),
     (
      'Pb2b', [None, k, None, k, None, k, None]),
     (
      'Pbmb', [None, k, None, k, None, k, None]),
     (
      'Pb2n', [None, k, None, hpk, h, k, None]),
     (
      'Pbmn', [None, k, None, hpk, h, k, None]),
     (
      'Pba2', [None, k, h, None, k, h, None]),
     (
      'Pbam', [None, k, h, None, k, h, None]),
     (
      'Paa', [None, k, h, h, h, k, None]),
     (
      'Pbab', [None, k, h, k, h, k, None]),
     (
      'Pan', [None, k, h, hpk, h, k, None]),
     (
      'Pbc2₁', [None, k, l, None, None, k, l]),
     (
      'Pbcm', [None, k, l, None, None, k, l]),
     (
      'Pbca', [None, k, l, h, h, k, l]),
     (
      'Pbcb', [None, k, l, k, None, k, l]),
     (
      'Pbcn', [None, k, l, hpk, h, k, l]),
     (
      'Pbn2₁', [None, k, hpl, None, h, k, l]),
     (
      'Pbnm', [None, k, hpl, None, h, k, l]),
     (
      'Pbna', [None, k, hpl, h, h, k, l]),
     (
      'Pbnb', [None, k, hpl, k, h, k, l]),
     (
      'Pbnn', [None, k, hpl, hpk, h, k, l]),
     (
      'Pcm2₁', [None, l, None, None, None, None, l]),
     (
      'Pc2m', [None, None, None, None, None, None, None]),
     (
      'Pcmm', [None, None, None, None, None, None, None]),
     (
      'Pc2a', [None, l, None, h, h, None, l]),
     (
      'Pcma', [None, l, None, h, h, None, l]),
     (
      'Pc2₁b', [None, l, None, k, None, k, l]),
     (
      'Pcmb', [None, l, None, k, None, k, l]),
     (
      'Pc2₁n', [None, l, None, hpk, h, k, l]),
     (
      'Pcmn', [None, l, None, hpk, h, k, l]),
     (
      'Pca2₁', [None, l, h, None, h, None, l]),
     (
      'Pcam', [None, l, h, None, h, None, l]),
     (
      'Pcaa', [None, l, h, h, h, None, l]),
     (
      'Pcab', [None, l, h, k, h, k, l]),
     (
      'Pcan', [None, l, h, hpk, h, k, l]),
     (
      'Pcc2', [None, l, h, None, None, None, l]),
     (
      'Pccm', [None, l, l, None, None, None, l]),
     (
      'Pcca', [None, l, l, h, h, None, l]),
     (
      'Pccb', [None, l, l, k, None, k, l]),
     (
      'Pccn', [None, l, l, hpk, h, k, l]),
     (
      'Pcn2', [None, l, hpl, None, h, None, l]),
     (
      'Pcnm', [None, l, hpl, None, h, None, l]),
     (
      'Pcna', [None, l, hpl, h, h, None, l]),
     (
      'Pcnb', [None, l, hpl, k, h, k, l]),
     (
      'Pcnn', [None, l, hpl, hpk, h, k, l]),
     (
      'Pnm2₁', [None, kpl, None, None, None, k, l]),
     (
      'Pnmm', [None, kpl, None, None, None, k, l]),
     (
      'Pn2₁m', [None, None, None, None, None, None, None]),
     (
      'Pn2₁a', [None, kpl, None, h, h, k, l]),
     (
      'Pnma', [None, kpl, None, h, h, k, l]),
     (
      'Pn2b', [None, kpl, None, k, None, k, l]),
     (
      'Pnmb', [None, kpl, None, k, None, k, l]),
     (
      'Pn2n', [None, kpl, None, hpk, h, k, l]),
     (
      'Pnmn', [None, kpl, None, hpk, h, k, l]),
     (
      'Pna2₁', [None, kpl, h, None, h, k, l]),
     (
      'Pnam', [None, kpl, h, None, h, k, l]),
     (
      'Pnaa', [None, kpl, h, h, h, k, l]),
     (
      'Pnab', [None, kpl, h, k, h, k, l]),
     (
      'Pnan', [None, kpl, h, hpk, h, k, l]),
     (
      'Pnc2', [None, kpl, l, None, None, k, l]),
     (
      'Pncm', [None, kpl, l, None, None, k, l]),
     (
      'Pnca', [None, kpl, l, h, h, k, l]),
     (
      'Pncb', [None, kpl, l, k, None, k, l]),
     (
      'Pncn', [None, kpl, l, hpk, h, k, l]),
     (
      'Pnn2', [None, kpl, hpl, None, h, k, l]),
     (
      'Pnnm', [None, kpl, hpl, None, h, k, l]),
     (
      'Pnna', [None, kpl, hpl, h, h, k, l]),
     (
      'Pnnb', [None, kpl, hpl, k, h, k, l]),
     (
      'Pnnn', [None, kpl, hpl, hpk, h, k, l]),
     (
      'C222', [hpk, k, h, hpk, h, k, None]),
     (
      'Cmm2', [hpk, k, h, hpk, h, k, None]),
     (
      'Cmmm', [hpk, k, h, hpk, h, k, None]),
     (
      'Cm2m', [hpk, k, h, hpk, h, k, None]),
     (
      'C2mm', [hpk, k, h, hpk, h, k, None]),
     (
      'C222₁', [hpk, k, h, hpk, h, k, l]),
     (
      'Cm2e', [hpk, k, h, [h, k], h, k, None]),
     (
      'Cmme', [hpk, k, h, [h, k], h, k, None]),
     (
      'C2me', [hpk, k, h, [h, k], h, k, None]),
     (
      'Cm2₁', [hpk, k, [h, l], hpk, h, k, l]),
     (
      'Cmcm', [hpk, k, [h, l], hpk, h, k, l]),
     (
      'C2cm', [hpk, k, [h, l], hpk, h, k, l]),
     (
      'C2ce', [hpk, k, [h, l], [h, k], h, k, l]),
     (
      'Cmce', [hpk, k, [h, l], [h, k], h, k, l]),
     (
      'Ccm2₁', [hpk, [k, l], h, hpk, h, k, l]),
     (
      'Ccmm', [hpk, [k, l], h, hpk, h, k, l]),
     (
      'Cc2m', [hpk, [k, l], h, hpk, h, k, l]),
     (
      'Cc2e', [hpk, [k, l], h, [h, k], h, k, l]),
     (
      'Ccme', [hpk, [k, l], h, [h, k], h, k, l]),
     (
      'Ccc2', [hpk, [k, l], [h, l], hpk, h, k, l]),
     (
      'Cccm', [hpk, [k, l], [h, l], hpk, h, k, l]),
     (
      'Ccce', [hpk, [k, l], [h, l], [h, k], h, k, l]),
     (
      'B222', [hpl, l, hpl, h, h, None, l]),
     (
      'Bmm2', [hpl, l, hpl, h, h, None, l]),
     (
      'Bmmm', [hpl, l, hpl, h, h, None, l]),
     (
      'Bm2m', [hpl, l, hpl, h, h, None, l]),
     (
      'B2mm', [hpl, l, hpl, h, h, None, l]),
     (
      'B22₁2', [hpl, l, hpl, h, h, k, l]),
     (
      'Bm2₁b', [hpl, l, hpl, [h, k], h, k, l]),
     (
      'Bmmb', [hpl, l, hpl, [h, k], h, k, l]),
     (
      'B2mb', [hpl, l, hpl, [h, k], h, k, l]),
     (
      'Bm2e', [hpl, l, [h, l], h, h, None, l]),
     (
      'Bmem', [hpl, l, [h, l], h, h, None, l]),
     (
      'B2em', [hpl, l, [h, l], h, h, None, l]),
     (
      'B2eb', [hpl, l, [h, l], [h, k], h, k, l]),
     (
      'Bmeb', [hpl, l, [h, l], [h, k], h, k, l]),
     (
      'Bbm2', [hpl, [k, l], hpl, h, h, k, l]),
     (
      'Bbmm', [hpl, [k, l], hpl, h, h, k, l]),
     (
      'Bb2₁m', [hpl, [k, l], hpl, h, h, k, l]),
     (
      'Bb2b', [hpl, [k, l], hpl, [h, k], h, k, l]),
     (
      'Bbmb', [hpl, [k, l], hpl, [h, k], h, k, l]),
     (
      'Bbe2', [hpl, [k, l], [h, l], h, h, k, l]),
     (
      'Bbem', [hpl, [k, l], [h, l], h, h, k, l]),
     (
      'Bbeb', [hpl, [k, l], [h, l], [h, k], h, k, l]),
     (
      'A222', [kpl, kpl, l, k, None, k, l]),
     (
      'Amm2', [kpl, kpl, l, k, None, k, l]),
     (
      'Ammm', [kpl, kpl, l, k, None, k, l]),
     (
      'Am2m', [kpl, kpl, l, k, None, k, l]),
     (
      'A2mm', [kpl, kpl, l, k, None, k, l]),
     (
      'A2₁22', [kpl, kpl, l, k, h, k, l]),
     (
      'Am2a', [kpl, kpl, l, [h, k], h, k, l]),
     (
      'Amma', [kpl, kpl, l, [h, k], h, k, l]),
     (
      'A2₁ma', [kpl, kpl, l, [h, k], h, k, l]),
     (
      'Ama2', [kpl, kpl, [h, l], k, h, k, l]),
     (
      'Amam', [kpl, kpl, [h, l], k, h, k, l]),
     (
      'A2aa', [kpl, kpl, [h, l], [h, k], h, k, l]),
     (
      'Amaa', [kpl, kpl, [h, l], [h, k], h, k, l]),
     (
      'Aem2', [kpl, [k, l], l, k, None, k, l]),
     (
      'Aemm', [kpl, [k, l], l, k, None, k, l]),
     (
      'Ae2m', [kpl, [k, l], l, k, None, k, l]),
     (
      'Ae2a', [kpl, [k, l], l, [h, k], h, k, l]),
     (
      'Aema', [kpl, [k, l], l, [h, k], h, k, l]),
     (
      'Aea2', [kpl, [k, l], [h, l], k, h, k, l]),
     (
      'Aeam', [kpl, [k, l], [h, l], k, h, k, l]),
     (
      'Aeaa', [kpl, [k, l], [h, l], [h, k], h, k, l]),
     (
      'I222', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'Imm2', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'Immm', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'I2₁2₁2₁', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'Im2m', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'F222', [[hpk, hpl, kpl], [k, l], [h, l], [h, k], h, k, l]),
     (
      'I2mm', [hpkpl, kpl, hpl, hpk, h, k, l]),
     (
      'Im2a', [hpkpl, kpl, hpl, [h, k], h, k, l]),
     (
      'I2mb', [hpkpl, kpl, hpl, [h, k], h, k, l]),
     (
      'Ima2', [hpkpl, kpl, [h, l], hpk, h, k, l]),
     (
      'I2cm', [hpkpl, kpl, [h, l], hpk, h, k, l]),
     (
      'I2cb', [hpkpl, kpl, [h, l], [h, k], h, k, l]),
     (
      'Iem2', [hpkpl, kpl, [h, l], [h, k], h, k, l]),
     (
      'Ic2a', [hpkpl, [k, l], hpl, [h, k], h, k, l]),
     (
      'Iba2', [hpkpl, [k, l], [h, l], hpk, h, k, l]),
     (
      'Fmm2', [[hpk, hpl, kpl], [k, l], [h, l], [h, k], h, k, l]),
     (
      'Fm2m', [[hpk, hpl, kpl], [k, l], [h, l], [h, k], h, k, l]),
     (
      'F2mm', [[hpk, hpl, kpl], [k, l], [h, l], [h, k], h, k, l]),
     (
      'F2dd', [[hpk, hpl, kpl], [k, l], [hpl4n, h, l], [hpk4n, h, k], h4n, k4n, l4n]),
     (
      'Fd2d', [[hpk, hpl, kpl], [kpl4n, k, l], [h, l], [hpk4n, h, k], h4n, k4n, l4n]),
     (
      'Fdd2', [[hpk, hpl, kpl], [kpl4n, k, l], [hpl4n, h, l], [h, k], h4n, k4n, l4n]),
     (
      'Imma', [hpkpl, kpl, hpl, [h, k], h, k, l]),
     (
      'Immb', [hpkpl, kpl, hpl, [h, k], h, k, l]),
     (
      'Imam', [hpkpl, kpl, [h, l], hpk, h, k, l]),
     (
      'Imcm', [hpkpl, kpl, [h, l], hpk, h, k, l]),
     (
      'Imcb', [hpkpl, kpl, [h, l], [h, k], h, k, l]),
     (
      'Iemm', [hpkpl, kpl, [h, l], [h, k], h, k, l]),
     (
      'Icma', [hpkpl, [k, l], hpl, [h, k], h, k, l]),
     (
      'Ibam', [hpkpl, [k, l], [h, l], hpk, h, k, l]),
     (
      'Ibca', [hpkpl, [k, l], [h, l], [h, k], h, k, l]),
     (
      'Icab', [hpkpl, [k, l], [h, l], [h, k], h, k, l]),
     (
      'Fmmm', [[hpk, hpl, kpl], [k, l], [h, l], [h, k], h, k, l]),
     (
      'Fddd', [[hpk, hpl, kpl], [kpl4n, k, l], [hpl4n, h, l], [hpk4n, h, k], h4n, k4n, l4n])])

    def getcolumn(self, m):
        if arezeros(1, 1, 0, m):
            column = 6
        elif arezeros(1, 0, 1, m):
            column = 5
        elif arezeros(0, 1, 1, m):
            column = 4
        elif arezeros(0, 0, 1, m):
            column = 3
        elif arezeros(0, 1, 0, m):
            column = 2
        elif arezeros(1, 0, 0, m):
            column = 1
        else:
            column = 0
        return (
         column, m)


class Tetragonal(SGClass):
    conditions = OrderedDict([('P4', [None, None, None, None, None, None, None]),
     ('P4̅', 'P4'),
     ('P4/m', 'P4'),
     ('P422', 'P4'),
     ('P4mm', 'P4'),
     ('P4̅2m', 'P4'),
     ('P4/mmm', 'P4'),
     ('P4̅m2', 'P4'),
     (
      'P42₁2', [None, None, None, None, None, k, None]),
     ('P4̅2₁m', 'P42₁2'),
     (
      'P4₂', [None, None, None, None, l, None, None]),
     ('P4₂/m', 'P4₂'),
     ('P4₂22', 'P4₂'),
     (
      'P4₂2₁2', [None, None, None, None, l, k, None]),
     (
      'P4₁', [None, None, None, None, l4n, None, None]),
     ('P4₃', 'P4₁'),
     ('P4₁22', 'P4₁'),
     ('P4₃22', 'P4₁'),
     (
      'P4₁2₁2', [None, None, None, None, l4n, k, None]),
     ('P4₃2₁2', 'P4₁2₁2'),
     (
      'P4₂mc', [None, None, None, l, l, None, None]),
     ('P4̅2c', 'P4₂mc'),
     ('P42/mmc', 'P4₂mc'),
     (
      'P4̅2₁c', [None, None, None, l, l, k, None]),
     (
      'P4bm', [None, None, k, None, None, k, None]),
     ('P4̅b2', 'P4bm'),
     ('P4/mbm', 'P4bm'),
     (
      'P4₂bc', [None, None, k, l, l, k, None]),
     ('P4₂/mbc', 'P4₂bc'),
     (
      'P4₂cm', [None, None, l, None, l, None, None]),
     ('P4̅c2', 'P4₂cm'),
     ('P4₂/mcm', 'P4₂cm'),
     (
      'P4cc', [None, None, l, l, l, None, None]),
     ('P4/mcc', 'P4cc'),
     (
      'P4₂nm', [None, None, kpl, None, l, k, None]),
     ('P4̅n2', 'P4₂nm'),
     ('P4₂/mnm', 'P4₂nm'),
     (
      'P4nc', [None, None, kpl, l, l, k, None]),
     ('P4/mnc', 'P4nc'),
     (
      'P4/n', [None, hpk, None, None, None, k, None]),
     ('P4/nmm', 'P4/n'),
     (
      'P4₂/n', [None, hpk, None, None, l, k]),
     (
      'P4₂/nmc', [None, hpk, None, l, l, k, None]),
     (
      'P4/nbm', [None, hpk, k, None, None, k, None]),
     (
      'P4₂/nbc', [None, hpk, k, l, l, k, None]),
     (
      'P4₂/ncm', [None, hpk, l, None, l, k, None]),
     (
      'P4/ncc', [None, hpk, l, l, l, k, None]),
     (
      'P4₂nnm', [None, hpk, kpl, None, l, k, None]),
     (
      'P4/nnc', [None, hpk, kpl, l, l, k, None]),
     (
      'I4', [hpkpl, hpk, kpl, l, l, k, None]),
     ('I4̅', 'I4'),
     ('I4/m', 'I4'),
     ('I422', 'I4'),
     ('I4mm', 'I4'),
     ('I4̅2m', 'I4'),
     ('I4/mmm', 'I4'),
     ('I4̅m2', 'I4'),
     (
      'I4₁', [hpkpl, hpk, kpl, l, l4n, k, None]),
     ('I4₁22', 'I4₁'),
     (
      'I4₁md', [hpkpl, hpk, kpl, twohpl4n, l4n, k, h]),
     ('I4̅2d', 'I4₁md'),
     (
      'I4cm', [hpk, l, hpk, [k, l], l, l, k, None]),
     ('I4̅c2', 'I4cm'),
     ('I4/mcm', 'I4cm'),
     (
      'I4₁cd', [hpkpl, hpk, [k, l], twohpl4n, l4n, k, h]),
     (
      'I4₁/a', [hpkpl, [h, k], kpl, l, l4n, k, None]),
     (
      'I4₁/amd', [hpkpl, [h, k], kpl, twohpl4n, l4n, k, h]),
     (
      'I4₁/acd', [hpkpl, [h, k], [k, l], twohpl4n, l4n, k, h])])

    def getcolumn(self, m):
        mh, mk, ml = m
        if mh == mk and arezeros(0, 0, 1, m):
            column = 6
        elif arezeros(1, 0, 1, m):
            column = 5
        elif arezeros(1, 1, 0, m):
            column = 4
        elif mh == mk:
            column = 3
        elif arezeros(1, 0, 0, m):
            column = 2
        elif arezeros(0, 0, 1, m):
            column = 1
        else:
            column = 0
        return (
         column, m)


class Trigonal(SGClass):
    conditions = OrderedDict([('R3', [None, None, None, None]),
     ('R3̅', 'R3'),
     ('R32', 'R3'),
     ('R3m', 'R3'),
     ('R3̅m', 'R3'),
     (
      'R3c', [None, None, l, h]),
     ('R3̅c', 'R3c')])

    def getcolumn(self, m):
        if len(m) == 4:
            mh, mk, mi, ml = m
            if arezeros(1, 1, 1, 0, m):
                column = 3
            elif mh == mk and mi == -2 * mh:
                column = 2
            elif mh == -mk and arezeros(0, 0, 1, 0, m):
                column = 1
            else:
                column = 0
        elif len(m) == 3:
            mh, mk, ml = m
            if mh == mk == ml:
                column = 3
            elif mh == mk:
                column = 2
            else:
                column = 1
        else:
            debugtools.frustration()
            raise ValueError
        return (
         column, m)


class Hexagonal(SGClass):
    conditions = OrderedDict([('P6', [None, None, None]),
     (
      'P6̅', [None, None, None]),
     (
      'P6/m', [None, None, None]),
     (
      'P622', [None, None, None]),
     (
      'P6mm', [None, None, None]),
     (
      'P6̅2m', [None, None, None]),
     (
      'P6/mmm', [None, None, None]),
     (
      'P6̅m2', [None, None, None]),
     (
      'P6₃', [None, None, l]),
     (
      'P6₃/m', [None, None, l]),
     (
      'P6₃22', [None, None, l]),
     (
      'P6₂', [None, None, l3n]),
     (
      'P6₂22', [None, None, l3n]),
     (
      'P6₄', [None, None, None, l3n]),
     (
      'P6₁', [None, None, l6n]),
     (
      'P6₁22', [None, None, l6n]),
     (
      'P6₃', [None, None, l6n]),
     (
      'P6₅22', [None, None, l6n]),
     (
      'P6₃mc', [None, l, l]),
     (
      'P6̅2c', [None, l, l]),
     (
      'P6₃/mmc', [None, l, l]),
     (
      'P6₃cm', [l, None, l]),
     (
      'P6̅c2', [l, None, l]),
     (
      'P6₃/mcm', [l, None, l]),
     (
      'P6cc', [l, l, l]),
     (
      'P6/mcc', [l, l, l])])

    def getcolumn(self, m):
        mh, mk, ml = m
        mi = -(mh + mk)
        hexm = (mh, mk, mi, ml)
        if arezeros(1, 1, 1, 0, hexm):
            column = 2
        elif mh == mk and mi == -2 * mh:
            column = 1
        elif arezeros(0, 0, 1, 0, hexm) and mh == -mk:
            column = 0
        else:
            column = None
        return (
         column, m)


class Cubic(SGClass):
    conditions = OrderedDict([('P23', [None, None, None, None]),
     (
      'Pm3̅', [None, None, None, None]),
     (
      'P432', [None, None, None, None]),
     (
      'P4̅3m', [None, None, None, None]),
     (
      'Pm3̅m', [None, None, None, None]),
     (
      'P2₁3', [None, None, None, l]),
     (
      'P4₂32', [None, None, None, l]),
     (
      'P4₁32', [None, None, None, l4n]),
     (
      'P4₃32', [None, None, None, l4n]),
     (
      'P4̅3n', [None, None, l, l]),
     (
      'Pm3̅n', [None, None, l, l]),
     (
      'Pa3̅', [None, k, None, l]),
     (
      'Pn3̅', [None, kpl, None, l]),
     (
      'Pn3̅m', [None, kpl, None, l]),
     (
      'Pn3̅n', [None, kpl, l, l]),
     (
      'I23', [hpkpl, kpl, l, l]),
     (
      'I2₁3', [hpkpl, kpl, l, l]),
     (
      'Im3̅', [hpkpl, kpl, l, l]),
     (
      'I432', [hpkpl, kpl, l, l]),
     (
      'I4̅3m', [hpkpl, kpl, l, l]),
     (
      'Im3̅m (BCC)', [hpkpl, kpl, l, l]),
     (
      'I4₁32', [hpkpl, kpl, l, l4n]),
     (
      'I4̅3d', [hpkpl, kpl, [twohpl4n, l], l4n]),
     (
      'Ia3̅', [hpkpl, [k, l], l, l]),
     (
      'Ia3̅d', [hpkpl, [k, l], [twohpl4n, l], l4n]),
     (
      'F23', [[hpk, hpl, kpl], [k, l], hpl, l]),
     (
      'Fm3̅', [[hpk, hpl, kpl], [k, l], hpl, l]),
     (
      'F432', [[hpk, hpl, kpl], [k, l], hpl, l]),
     (
      'F4̅3m', [[hpk, hpl, kpl], [k, l], hpl, l]),
     (
      'Fm3̅m', [[hpk, hpl, kpl], [k, l], hpl, l]),
     (
      'F4₁32', [[hpk, hpl, kpl], [k, l], hpl, l4n]),
     (
      'F4̅3c', [[hpk, hpl, kpl], [k, l], [h, l], l]),
     (
      'Fm3̅c', [[hpk, hpl, kpl], [k, l], [h, l], l]),
     (
      'Fd3̅', [[hpk, hpl, kpl], [kpl4n, k, l], hpl, l4n]),
     (
      'Fd3̅m', [[hpk, hpl, kpl], [kpl4n, k, l], hpl, l4n]),
     (
      'Fd3̅c', [[hpk, hpl, kpl], [kpl4n, k, l], [h, l], l4n])])

    def getcolumn(self, m):
        mh, mk, ml = m
        column = None
        for mh, mk, ml in [[mh, mk, ml], [mk, ml, mh], [ml, mh, mk]]:
            if arezeros(1, 1, 0, m):
                column = 3
            else:
                if mh == mk:
                    column = 2
                elif arezeros(1, 0, 0, m):
                    column = 1
                if column:
                    return (column, [mh, mk, ml])

        column = 0
        return (column, [mh, mk, ml])


Triclinic = Triclinic()
Monoclinic = Monoclinic()
Orthorhombic = Orthorhombic()
Tetragonal = Tetragonal()
Trigonal = Trigonal()
Hexagonal = Hexagonal()
Cubic = Cubic()
SGkeys = SGClass.conditions.keys()
crystalsystems = [
 Triclinic, Monoclinic, Orthorhombic, Tetragonal, Trigonal, Hexagonal, Cubic]

def check(m, SG):
    """
    This is the function intended for external use. Checks which crystal system the SG is in, then executes that
    system's check method.
    """
    key = SG + ',' + ('').join(map(str, m))
    if key in cache:
        return cache[key]
    for crystalsystem in crystalsystems:
        if SG in crystalsystem.conditions:
            reflected = crystalsystem.check(m, SG)
            cache[key] = reflected
            return reflected


if __name__ == '__main__':

    def test(m, SG):
        print SG, m, check(m, SG)


    SG = 'P2₁'
    m = (1, 2, 1)
    test(m, SG)
    m = (0, 1, 0)
    test(m, SG)
    m = (0, 2, 0)
    test(m, SG)
    m = (0, 3, 0)
    test(m, SG)
    SG = 'P2₁2₁2'
    m = (1, 1, 1)
    test(m, SG)
    m = (0, 1, 0)
    test(m, SG)

    @debugtools.timeit
    def timetest():
        for i in range(0, 300000):
            check(m, SG)


    timetest()
    m = (2, 0, 1)
    test(m, 'Pmn2₁')