# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: extensions/salt.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = "\n    Saltbridge extension\n\n    Find all salt bridges as determined by the cutoff distance below.\n    Uses PDB2PQR to determine atom identities and distances, and write\n    out all located salt bridges to stdout.\n    \n    NOTE:  A bond may be labeled BOTH hbond and salt-bridge if you use both\n           options in one pdb2pqr run.  Look out for double counting.\n\n    NOTE:  This extension currently does not support salt bridges with chain termini.\n\n    Author:  Mike Bradley (heavily copied from Todd Dolinsky's hbond extension)\n"
__date__ = '25 August 2006'
__author__ = 'Mike Bradley'
from src.utilities import distance
from src.routines import Cells
DIST_CUTOFF = 4.0

def usage():
    return 'Print a list of salt bridges to {output-path}.salt'


def run_extension(routines, outroot, options):
    """
        Print a list of salt bridges.

        Parameters
            routines:  A link to the routines object
            outroot:   The root of the output name
            options:   options object 
    """
    outname = outroot + '.salt'
    outfile = open(outname, 'w')
    routines.write('Printing salt bridge list...\n')
    posresList = [
     'LYS', 'ARG', 'HIP']
    negresList = ['GLU', 'ASP', 'CYM']
    posatomList = ['NE', 'NH1', 'NH2', 'NZ', 'ND1', 'NE2']
    negatomList = ['SG', 'OE1', 'OE2', 'OD1', 'OD2']
    cellsize = int(DIST_CUTOFF + 1.0 + 1.0)
    protein = routines.protein
    routines.cells = Cells(cellsize)
    routines.cells.assignCells(protein)
    for cation in protein.getAtoms():
        if cation.residue.name == 'NMET':
            print 'YES NMET'
        if cation.residue.name not in posresList:
            continue
        else:
            if cation.name not in posatomList:
                continue
            closeatoms = routines.cells.getNearCells(cation)
            for anion in closeatoms:
                if cation.residue.name == anion.residue.name:
                    continue
                if anion.residue.name not in negresList:
                    continue
                elif anion.name not in negatomList:
                    continue
                dist = distance(cation.getCoords(), anion.getCoords())
                if dist > DIST_CUTOFF:
                    continue
                outfile.write('Cation: %s %s\tAnion: %s %s\tsaltdist: %.2f\n' % (
                 cation.residue, cation.name, anion.residue, anion.name, dist))

    outfile.close()