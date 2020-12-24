# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/sample/genonets_exmpl_minimal.py
# Compiled at: 2016-07-23 05:10:02
"""
    genonets_exmpl_minimal
    ~~~~~~~~~~~~~~~~~~~~~~

    Demonstrates the minimal code required to create genotype networks, perform analyses,
    and write results to files using Genonets with default settings.

    Use the following command to run the script:
    'python genonets_exmpl_minimal.py DNA true data/genonets_sample_input.txt 0.35 results_minimal'

    Output files will be generated in 'results_minimal/'

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from genonets.cmdl_handler import CmdParser
from genonets.genonets_interface import Genonets
if __name__ == '__main__':
    Genonets(CmdParser().getArgs(), process=True)
    print '\nDone.\n'