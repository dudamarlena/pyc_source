# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/sample/genonets_exmpl_custom.py
# Compiled at: 2016-07-23 05:10:02
"""
    genonets_exmpl_custom
    ~~~~~~~~~~~~~~~~~~~~~

    Illustrates the process of customizing the output by adding information to the
    result file that would not be added by Genonets by default.

    The 'Peaks' analysis is used as an example. By default, the 'Peaks' analysis 
    stores results in a dictionary of the form:
    {key=peakID : value=[genotypes in the peak]}. The sample code in this file
    customizes this dictionary by adding the score value corresponding to each
    genotype in the list. The resulting dictionary is of the format:
    {key=peakID : value=[(genotype1, score1), ..., (genotypeN, scoreN)]},
    i.e., it is a list of tuples.

    Use the following command to run the script:
    'python genonets_exmpl_custom.py DNA true data/genonets_sample_input.txt 0.35 results_custom'

    Output files will be generated in 'results_custom/'

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from genonets.cmdl_handler import CmdParser
from genonets.genonets_interface import Genonets
from genonets.genonets_constants import AnalysisConstants as ac

def process(args):
    gn = Genonets(args)
    gn.create()
    gn.analyze(analyses=[ac.PEAKS])
    for genotypeSet in gn.genotype_sets():
        giant = gn.dominant_network(genotypeSet)
        peaks = giant['Peaks']
        newPeaks = {}
        for peak in peaks:
            seqScrTuples = []
            for sequence in peaks[peak]:
                try:
                    vertex = giant.vs.find(sequences=sequence)
                except ValueError:
                    print "Oops! can't find " + sequence + ' in giant.'

                score = giant.vs[vertex.index]['escores']
                seqScrTuples.append((sequence, score))

            newPeaks[peak] = seqScrTuples

        giant['Peaks'] = newPeaks

    gn.save()
    gn.save_network_results()


if __name__ == '__main__':
    process(CmdParser().getArgs())
    print '\nDone.\n'