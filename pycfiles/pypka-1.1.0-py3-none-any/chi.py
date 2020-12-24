# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: extensions/chi.py
# Compiled at: 2018-06-29 21:47:06
"""
    Chi extension

    Print the backbone chi angle for each residue in the structure.
    Chi angle is determined by the coordinates of the N, CA, CB (if
    available), and CG/OG/SG atoms (if available).

    Author:  Todd Dolinsky
"""
__date__ = '17 February 2006'
__author__ = 'Todd Dolinsky'
from src.utilities import getDihedral

def usage():
    return 'Print the per-residue backbone chi angle to {output-path}.chi'


def run_extension(routines, outroot, options):
    """
        Print the list of psi angles

        Parameters
            routines:  A link to the routines object
            outroot:   The root of the output name
            options:   options object 
    """
    outname = outroot + '.chi'
    outfile = open(outname, 'w')
    routines.write('\nPrinting chi angles for each residue...\n')
    routines.write('Residue     chi\n')
    routines.write('----------------\n')
    protein = routines.protein
    for residue in protein.getResidues():
        if residue.hasAtom('N'):
            ncoords = residue.getAtom('N').getCoords()
        else:
            continue
        if residue.hasAtom('CA'):
            cacoords = residue.getAtom('CA').getCoords()
        else:
            continue
        if residue.hasAtom('CB'):
            cbcoords = residue.getAtom('CB').getCoords()
        else:
            continue
        if residue.hasAtom('CG'):
            gcoords = residue.getAtom('CG').getCoords()
        elif residue.hasAtom('OG'):
            gcoords = residue.getAtom('OG').getCoords()
        elif residue.hasAtom('SG'):
            gcoords = residue.getAtom('SG').getCoords()
        else:
            continue
        chi = getDihedral(ncoords, cacoords, cbcoords, gcoords)
        routines.write('%s\t%.4f\n' % (residue, chi))
        outfile.write('%s\t%.4f\n' % (residue, chi))

    routines.write('\n')
    outfile.close()