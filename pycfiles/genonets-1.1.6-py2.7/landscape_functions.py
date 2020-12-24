# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/landscape_functions.py
# Compiled at: 2017-01-31 16:34:36
"""
    landscape_functions
    ~~~~~~~~~~~~~~~~~~~

    Wrapper for all landscape analysis functions.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import igraph
from peak_functions import PeakAnalyzer
from path_functions import PathAnalyzer
from epistasis_functions import EpistasisAnalyzer
from genonets_utils import Utils

class Landscape:

    def __init__(self, network, netUtils, seqToEscrDict, delta, bitManip):
        self.network = network
        self.netUtils = netUtils
        self.peakAnalyzer = PeakAnalyzer(network, netUtils, delta)
        self.pathAnalyzer = PathAnalyzer(network, netUtils, delta)
        self.epiAnalyzer = EpistasisAnalyzer(network, netUtils, seqToEscrDict, delta, bitManip)
        self.bitManip = self.netUtils.bitManip

    def getPeaks(self, recompute):
        return self.peakAnalyzer.getPeaks(recompute)

    def getAccessiblePaths(self, pathLength=0):
        return self.pathAnalyzer.getAccessiblePaths(pathLength)

    def getEpistasis(self):
        return self.epiAnalyzer.getEpiAll()

    def populateDistsToSummit(self):
        bm = self.bitManip
        summit = Utils.getSeqWithMaxScore(self.network, self.bitManip.seqLength)
        trgtVrtx = self.netUtils.getVertex(summit, self.network)
        vertices = [ self.netUtils.getVertex(seq, self.network) for seq in self.network.vs['sequences']
                   ]
        self.network.vs['Distance from Summit'] = [ len(self.network.get_shortest_paths(srcVrtx, to=trgtVrtx, weights=None, mode=igraph.OUT, output='epath')[0]) for srcVrtx in vertices
                                                  ]
        return