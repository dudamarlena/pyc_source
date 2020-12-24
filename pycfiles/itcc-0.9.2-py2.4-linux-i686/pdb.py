# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/pdb.py
# Compiled at: 2008-04-20 13:19:45
import numpy

class Pdb(object):
    __module__ = __name__

    def __init__(self, ifile):
        self.idxs = []
        self.atoms = []
        self.symbols = []
        self.coords = []
        for line in ifile:
            words = line.split()
            if words[:1] == ['ATOM']:
                self.idxs.append(int(line[7:11]))
                self.symbols.append(line[12:16].strip())
                atom = self.symbols[(-1)]
                while '0' <= atom[0] <= '9':
                    atom = atom[1:]

                self.atoms.append(atom)
                self.coords.append([ float(line[x:x + 8]) for x in range(30, 54, 8) ])

        self.idxs = numpy.array(self.idxs)
        self.coords = numpy.array(self.coords)

    def connect(self):
        if self.hasattr('connect_data'):
            return self.connect_data
        self.connect_data = [ [] for i in range(len(self.atoms)) ]