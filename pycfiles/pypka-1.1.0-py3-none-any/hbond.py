# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: extensions/hbond.py
# Compiled at: 2018-06-29 21:47:06
"""
    Hbond extension

    Find all hydrogen bonds as determined by the cutoffs specified.
    Uses PDB2PQR to determine donors and acceptors, and displays
    all available bonds to file. 
    
    The original bonding parameters were an angle of 20.0, 
    distance of 3.30, and using the old method for calculating 
    distance.
    
    The original parameters for WHAT-IF output was an angle of
    90.0, distance of 3.30, and using the old method for 
    calculating distance. 

    Authors:  Todd Dolinsky, Michael J Bradley, Julie Mitchell, and Kyle Monson
"""
__date__ = '17 February 2006'
__author__ = 'Todd Dolinsky, Michael J Bradley, Julie Mitchell, and Kyle Monson'
from src.utilities import distance, getAngle
from src.routines import Cells
from math import cos
import extensions
ANGLE_CUTOFF = 30.0
DIST_CUTOFF = 3.4

def addExtensionOptions(extensionGroup):
    """
        Add options to set output type, angle cutoff, distance cutoff, and distance calculating method.
    """
    extensionGroup.add_option('--whatif', dest='whatif', action='store_true', default=False, help='Change hbond output to WHAT-IF format.')
    extensionGroup.add_option('--angle_cutoff', dest='angle_cutoff', type='float', action='store', default=ANGLE_CUTOFF, help='Angle cutoff to use when creating hbond data (default %s)' % ANGLE_CUTOFF)
    extensionGroup.add_option('--distance_cutoff', dest='distance_cutoff', type='float', action='store', default=DIST_CUTOFF, help='Distance cutoff to use when creating hbond data (default %s)' % DIST_CUTOFF)
    extensionGroup.add_option('--old_distance_method', dest='old_distance_method', action='store_true', default=False, help='Use distance from donor hydrogen to acceptor to calculate distance used with --distance_cutoff.')


def usage():
    return 'Print a list of hydrogen bonds to {output-path}.hbond'


def _residueString(residue, name):
    return '%4d %-4s (%4d  ) %s     %-4s' % (
     residue.resSeq, residue.name, residue.resSeq, residue.chainID, name)


def create_hbond_output(routines, outfile, whatif=False, angleCutoff=ANGLE_CUTOFF, distanceCutoff=DIST_CUTOFF, oldDistanceMethod=False):
    routines.write('Printing hydrogen bond list...\n')
    output = extensions.extOutputHelper(routines, outfile)
    cellsize = int(distanceCutoff + 1.0 + 1.0)
    protein = routines.protein
    routines.setDonorsAndAcceptors()
    routines.cells = Cells(cellsize)
    routines.cells.assignCells(protein)
    for donor in protein.getAtoms():
        if not donor.hdonor:
            continue
        donorhs = []
        for bond in donor.bonds:
            if bond.isHydrogen():
                donorhs.append(bond)

        if donorhs == []:
            continue
        closeatoms = routines.cells.getNearCells(donor)
        for acc in closeatoms:
            if not acc.hacceptor:
                continue
            if donor.residue == acc.residue:
                continue
            if whatif and donor.residue.chainID == acc.residue.chainID:
                continue
            if not oldDistanceMethod:
                dist = distance(donor.getCoords(), acc.getCoords())
                if dist > distanceCutoff:
                    continue
            for donorh in donorhs:
                if oldDistanceMethod:
                    dist = distance(donorh.getCoords(), acc.getCoords())
                    if dist > distanceCutoff:
                        continue
                angle = getAngle(acc.getCoords(), donor.getCoords(), donorh.getCoords())
                if angle > angleCutoff:
                    continue
                if whatif:
                    if donor.tempFactor > 60.0:
                        continue
                    if acc.tempFactor > 60.0:
                        continue
                    thisBstring = 'B' if donor.isBackbone() else 'S'
                    thatBstring = 'B' if acc.isBackbone() else 'S'
                    score = 1.7 / dist * cos(angle * 3.142 / 180.0)
                    output.write(_residueString(donor.residue, donor.name))
                    output.write('-> ')
                    output.write(_residueString(acc.residue, acc.name))
                    output.write('Sym=   1 Val= %6.3lf  DA=%6.2f  DHA=%6.2f (%s-%s)\n' % (
                     score, dist, angle, thisBstring, thatBstring))
                else:
                    s = 'Donor: %s %s\tAcceptor: %s %s\tdist: %.2f\tAngle: %.2f\n' % (
                     donor.residue, donor.name, acc.residue, acc.name, dist, angle)
                    output.write(s)

    routines.write('\n')


def run_extension(routines, outroot, options):
    """
        Print a list of hydrogen bonds.

        Parameters
            routines:  A link to the routines object
            outroot:   The root of the output name
            options:   options object 
    """
    outname = outroot + '.hbond'
    with open(outname, 'w') as (outfile):
        create_hbond_output(routines, outfile, whatif=options.whatif, angleCutoff=options.angle_cutoff, distanceCutoff=options.distance_cutoff, oldDistanceMethod=options.old_distance_method)