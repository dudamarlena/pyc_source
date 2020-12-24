# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/dlg.py
# Compiled at: 2008-04-20 13:19:45


class DlgItem(object):
    __module__ = __name__

    def __init__(self, ifile):
        self.good = False
        self.rank = None
        for line in ifile:
            if line.startswith('USER    Cluster Rank ='):
                self.rank = int(line.split()[(-1)])
                break

        if self.rank is None:
            return
        for line in ifile:
            if line.startswith('USER    RMSD from reference structure       ='):
                self.rmsd = float(line.split()[(-2)])
                break

        for line in ifile:
            if line.startswith('USER    Estimated Free Energy of Binding    ='):
                self.ene = float(line.split()[(-3)])
                break

        self.mol = ''
        for line in ifile:
            if line.split()[:1] == ['ATOM']:
                self.mol += line
            elif line.split()[:1] == ['TER']:
                break

        self.good = True
        return

    def __nonzero__(self):
        return self.good


class Dlg(object):
    __module__ = __name__

    def __init__(self, ifile):
        self.ifile = ifile

    def __iter__(self):
        return self

    def next(self):
        res = DlgItem(self.ifile)
        if res:
            return res
        else:
            raise StopIteration