# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: extensions/summary.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    Summary extension\n\n    Print protein summary file. \n    Currently prints a list of all residue in protein.\n'
__date__ = '21 October 2011'
__author__ = 'Kyle Monson'
import extensions

def usage():
    """
    Returns usage text for summary.
    """
    return 'Print protein summary information to {output-path}.summary.'


def create_summary_output(routines, outfile):
    """
    Output the interaction energy between each possible residue pair.
    """
    routines.write('Printing protein summary...\n')
    output = extensions.extOutputHelper(routines, outfile)
    output.write(routines.protein.getSummary() + '\n')
    for residue in routines.protein.getResidues():
        output.write(str(residue) + '\n')


def run_extension(routines, outroot, options):
    outname = outroot + '.summary'
    with open(outname, 'w') as (outfile):
        create_summary_output(routines, outfile)