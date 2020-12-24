# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/sample/genonets_exmpl_parallel.py
# Compiled at: 2016-07-23 05:10:02
"""
    genonets_exmpl_parallel
    ~~~~~~~~~~~~~~~~~~~~~~~

    Demonstrates the steps required to create genotype networks, perform analyses, 
    and write results to files using Genonets with multiprocessing enabled.

    Use the following command to run the script:
    'python genonets_exmpl_parallel.py DNA true data/genonets_sample_input.txt 0.35 results_parallel'

    Output files will be generated in 'results_parallel/'

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from genonets.cmdl_handler import CmdParser
from genonets.genonets_interface import Genonets

def process(args):
    gn = Genonets(args)
    gn.create(parallel=True)
    gn.analyze(parallel=True)
    gn.save()
    gn.save_network_results()
    gn.save_genotype_results()


if __name__ == '__main__':
    process(CmdParser().getArgs())
    print '\nDone.\n'