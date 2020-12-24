# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: extensions/summary.py
# Compiled at: 2018-06-29 21:47:06
"""
    Summary extension

    Print protein summary file. 
    Currently prints a list of all residue in protein.
"""
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