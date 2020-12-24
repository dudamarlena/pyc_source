# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/structure_functions.py
# Compiled at: 2017-01-31 16:34:36
"""
    structure_functions
    ~~~~~~~~~~~~~~~~~~~

    Encapsulates functions for structural analyses.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import igraph

class StructureAnalyzer:

    def __init__(self, network, netBuilder):
        self.network = network
        self.netBuilder = netBuilder
        self.giant = self.netBuilder.getGiantComponent(self.network)

    def getComponentSizes(self):
        return self.netBuilder.getComponents(self.network)

    def getNumComponents(self):
        return len(self.netBuilder.getComponents(self.network))

    def getDominantSize(self):
        return self.giant.vcount()

    def getPercentDominantSize(self):
        return float(self.giant.vcount()) / float(self.network.vcount())

    def getEdgeDensity(self):
        return self.giant.density()

    def getAvgClstrCoeff(self):
        return self.giant.transitivity_avglocal_undirected()

    def getAssortativity(self):
        return self.giant.assortativity_degree()

    def getDiameter(self):
        return self.giant.diameter()

    def getDiameterPath(self):
        diameter = self.getDiameter()
        vSeq = self.giant.vs
        for i in range(len(vSeq) - 1):
            for j in range(i + 1, len(vSeq)):
                sPath = self.giant.get_shortest_paths(vSeq[i], vSeq[j], mode=igraph.OUT, output='vpath')
                if len(sPath[0]) == diameter + 1:
                    return sPath[0]

        return []

    def getCoreness(self):
        return self.giant.coreness()

    def getClusteringCoefficients(self):
        sequences = self.giant.vs
        clstrCoeffs = self.giant.transitivity_local_undirected(sequences)
        return clstrCoeffs