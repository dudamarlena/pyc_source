# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/findneighbour.py
# Compiled at: 2008-04-20 13:19:45
import sys
from itcc.molecule import read
from itcc.ccs2 import loopclosure, peptide, detectloop

def main():
    mol = read.readxyz(file(sys.argv[1]))
    loop = detectloop.loopdetect(mol)[0]
    loopc = loopclosure.LoopClosure()
    shakedata = loopclosure.getshakedata(mol, loop)
    loopc.shakedata = shakedata
    loopc.forcefield = 'oplsaa'
    loopc.log_level = 0
    for r6 in peptide.Peptide(mol).getr6s(loop):
        for (mol, ene) in loopc.findneighbor(mol, r6):
            print ene


if __name__ == '__main__':
    main()