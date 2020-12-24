# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/path_functions.py
# Compiled at: 2017-01-24 10:33:28
"""
    path_functions
    ~~~~~~~~~~~~~~

    Contains functions used for computation of accessible mutational paths.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import igraph
from genonets_utils import Utils

class PathAnalyzer:

    def __init__(self, network, netUtils, delta):
        self.network = network
        self.netUtils = netUtils
        self.bitManip = netUtils.bitManip
        self.delta = delta
        self.summitId = None
        self.max_path_length = 0
        self.allPathsToPeak = self.initPathsToPeak()
        return

    def initPathsToPeak(self):
        return {vId:[] for vId in range(len(self.network.vs['sequences']))}

    def getSummitId(self):
        return self.summitId

    def getAllPathsToPeak(self):
        return self.allPathsToPeak

    def getPathsThruVtxs(self):
        pathsThruVtx = [ 0 for i in range(self.network.vcount()) ]
        for vtxId in range(self.network.vcount()):
            vtxPaths = self.network.vs[vtxId]['pathsToSummit']
            for path in vtxPaths:
                for vtx in path:
                    pathsThruVtx[vtx] += 1

        return pathsThruVtx

    def getAccessiblePaths(self, pathLength=0):
        totalPaths = 0
        allAccPaths = 0
        summit = Utils.getSeqWithMaxScore(self.network, self.bitManip.seqLength)
        trgtVrtx = self.netUtils.getVertex(summit, self.network)
        self.summitId = trgtVrtx.index
        sequences = self.network.vs['sequences']
        sequences.remove(summit)
        for source in sequences:
            if pathLength == 0:
                self.getShortestAccPaths(source, trgtVrtx, pathLength)
            else:
                shrtPaths, accPaths = self.getShortestAccPaths(source, trgtVrtx, pathLength + 1)
                if shrtPaths:
                    totalPaths += float(len(shrtPaths))
                    allAccPaths += float(len(accPaths))

        try:
            return float(allAccPaths) / float(totalPaths)
        except ZeroDivisionError:
            return 0

    def getShortestAccPaths(self, source, trgtVrtx, pathLength):
        srcVrtx = self.netUtils.getVertex(source, self.network)
        allShrtPaths = self.network.get_all_shortest_paths(srcVrtx, trgtVrtx, mode=igraph.OUT)
        if pathLength == 0:
            shrtAccPaths = [ self.network.vs[path].indices for path in allShrtPaths if self.isAccessible(path)
                           ]
            self.allPathsToPeak[srcVrtx.index].extend(shrtAccPaths)
            if len(allShrtPaths[0]) > self.max_path_length:
                self.max_path_length = len(allShrtPaths[0])
            return (None, None)
        if len(allShrtPaths[0]) == pathLength:
            allShrtAccPaths = [ self.network.vs[path]['sequences'] for path in allShrtPaths if self.isAccessible(path)
                              ]
        else:
            allShrtPaths = None
            allShrtAccPaths = None
        return (allShrtPaths, allShrtAccPaths)
        return

    def isAccessible(self, path):
        isAcc = True
        escores = self.network.vs[path]['escores']
        maxYet = -0.5
        for i in range(len(escores) - 1):
            if escores[i] > maxYet:
                maxYet = escores[i]
            if maxYet - self.delta > escores[(i + 1)]:
                isAcc = False
                break

        return isAcc