# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: extensions/chi.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    Chi extension\n\n    Print the backbone chi angle for each residue in the structure.\n    Chi angle is determined by the coordinates of the N, CA, CB (if\n    available), and CG/OG/SG atoms (if available).\n\n    Author:  Todd Dolinsky\n'
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