# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/sample/genonets_exmpl_selective.py
# Compiled at: 2017-01-31 16:34:36
"""
    genonets_exmpl_selective
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Demonstrates the steps required to create genotype networks, perform analyses, and
    write results to files, for a selected subset of genotype sets from the input file
    using Genonets.

    Use the following command to run the script:
    'python genonets_exmpl_selective.py DNA true data/genonets_sample_input.txt 0.35 results_selective'

    Output files will be generated in 'results_selective/'

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from genonets.cmdl_handler import CmdParser
from genonets.genonets_interface import Genonets
from genonets.genonets_constants import AnalysisConstants as ac

def process(args):
    gn = Genonets(args)
    gn.create()
    gn.analyze(['Foxa2', 'Bbx'], analyses=[ac.ROBUSTNESS, ac.EVOLVABILITY])
    gn.save(['Foxa2', 'Bbx'])
    gn.save_network_results(['Foxa2', 'Bbx'])
    gn.save_genotype_results(['Foxa2', 'Bbx'])


if __name__ == '__main__':
    process(CmdParser().getArgs())
    print '\nDone.\n'