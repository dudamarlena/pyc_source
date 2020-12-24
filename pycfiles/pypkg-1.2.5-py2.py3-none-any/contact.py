# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: extensions/contact.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    Contact extension\n\n    Find all hydrogen bonds as determined by the DISTANCE cutoff below.\n    Uses PDB2PQR to determine donors and acceptors, and displays\n    all available bonds to stdout in a WHATIF-like format.\n\n    Author:  Julie C. Mitchell\n'
__date__ = 'April 2007'
__author__ = 'Julie C. Mitchell'
from src.utilities import distance
from src.routines import Cells
DIST_CUTOFF = 3.5

def usage():
    return 'Print a list of contacts to {output-path}.con\n'


def run_extension(routines, outroot, options):
    """
        Print a list of contacts.

        Parameters
            routines:  A link to the routines object
            outroot:   The root of the output name
            options:   options object 
    """
    outname = outroot + '.con'
    outfile = open(outname, 'w')
    cellsize = int(DIST_CUTOFF + 1.0 + 1.0)
    protein = routines.protein
    routines.setDonorsAndAcceptors()
    routines.cells = Cells(cellsize)
    routines.cells.assignCells(protein)
    for thisatom in protein.getAtoms():
        if not thisatom.hdonor:
            continue
        thisatomhs = []
        for bond in thisatom.bonds:
            if bond.isHydrogen():
                thisatomhs.append(bond)

        if thisatomhs == []:
            continue
        count = 0
        closeatoms = routines.cells.getNearCells(thisatom)
        for thatatom in closeatoms:
            if thisatom.residue == thatatom.residue:
                continue
            if thatatom.isHydrogen():
                continue
            thisdist = distance(thisatom.getCoords(), thatatom.getCoords())
            if thisdist <= DIST_CUTOFF:
                count = count + 1
                thisBstring = 'S'
                thatBstring = 'S'
                hscore = 0.0
                if thisatom.hdonor & thatatom.hacceptor:
                    hscore = 1.0
                if thisatom.hacceptor & thatatom.hdonor:
                    hscore = 1.0
                if thisatom.isBackbone():
                    thisBstring = 'B'
                if thatatom.isBackbone():
                    thatBstring = 'B'
                outfile.write('%4d %4d %-4s (%4d  ) %s     %-4s<>%4d %-4s (%4d  ) %s     %-4s D=%6.2f  H-ene=%6.2f  Sym=  (%s-%s)\n' % (
                 count, thisatom.residue.resSeq, thisatom.residue.name, thisatom.residue.resSeq, thisatom.residue.chainID, thisatom.name, thatatom.residue.resSeq, thatatom.residue.name, thatatom.residue.resSeq, thatatom.residue.chainID, thatatom.name, thisdist, hscore, thisBstring, thatBstring))

    routines.write('\n')
    outfile.close()