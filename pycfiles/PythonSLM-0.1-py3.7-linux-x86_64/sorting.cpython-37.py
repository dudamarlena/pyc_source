# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslm/hatching/sorting.py
# Compiled at: 2020-04-27 14:14:30
# Size of source mod 2**32: 8682 bytes
import numpy as np, networkx as nx, abc

class BaseSort(abc.ABC):

    def __init__(self):
        pass

    def __str__(self):
        return 'BaseSorter Feature'

    @abc.abstractmethod
    def sort(self, vectors: np.ndarray) -> np.ndarray:
        """
        Sorts the scan vectors in a particular order

        :param vectors: The un-sorted array of scan vectors
        :return: The sorted array of scan vectors
        """
        raise NotImplementedError('Sort method must be implemented')


class AlternateSort(BaseSort):
    __doc__ = '\n    Sort method flips pairs of scan vectors so that their direction alternates across adjacent vectors.\n    '

    def __init__(self):
        pass

    def __str__(self):
        return 'Alternating Hatch Sort'

    def sort(self, scanVectors: np.ndarray) -> np.ndarray:
        linePart = scanVectors[1:-1:2]
        flippedVectors = np.flip(linePart, 1)
        vectorCopy = scanVectors.copy()
        vectorCopy[1:-1:2] = flippedVectors
        return vectorCopy


class LinearSort(BaseSort):
    __doc__ = '\n    A linear sort approaches to sorting the scan vectors based on the current hatch angle specified in\n    :attribute:`pyslm.hatching.sorting.LinearSort.hatchAngle`. The approach takes the dot product of the hatch mid-point\n    and the projection along the X-axis is sorted in ascending order (+ve X direction).\n    '

    def __init__(self):
        self._hatchAngle = 0.0

    @property
    def hatchAngle(self) -> float:
        """
        The hatch angle reference across the scan vectors to be sorted
        """
        return self._hatchAngle

    @hatchAngle.setter
    def hatchAngle(self, angle: float):
        self._hatchAngle = angle

    def sort(self, scanVectors: np.ndarray) -> np.ndarray:
        theta_h = np.deg2rad(self._hatchAngle)
        norm = np.array([np.cos(theta_h), np.sin(theta_h)])
        midPoints = np.mean(scanVectors, axis=1)
        idx2 = norm.dot(midPoints.T)
        idx3 = np.argsort(idx2)
        sortIdx = np.arange(len(midPoints))[idx3]
        return scanVectors[sortIdx]


class GreedySort(BaseSort):
    __doc__ = '\n    The greedy sort approach is a heuristic approach to sorting the scan vectors based on the current hatch angle specified in\n    :attribute:`pyslm.hatching.sorting.LinearSort.hatchAngle` and clustering vectors together based on the hatch group\n     distance - :attribute:`pyslm.hatching.sorting.LinearSort.hatchTol`. Typically the\n\n     The approach finds clusters of scan vectors based on their connectivity based on a threshold\n    '

    def __init__(self, hatchAngle=0.0, hatchTol=None):
        self._hatchAngle = hatchAngle
        self._sortY = False
        self._clusterDistance = 5
        if hatchTol:
            self._hatchTol = hatchTol
        else:
            self._hatchTol = 0.5

    def __str__(self):
        return 'GreedySort Feature'

    @property
    def hatchAngle(self) -> float:
        """
        The hatch angle reference across the scan vectors to be sorted
        """
        return self._hatchAngle

    @hatchAngle.setter
    def hatchAngle(self, angle: float):
        self._hatchAngle = angle

    @property
    def hatchTol(self):
        """  The hatch group tolerance specifies the abritrary distance used for grouping the scan vectors into
        'scanning clusters'"""
        return self._hatchTol

    @hatchTol.setter
    def hatchTol(self, tolerance):
        self._hatchTol = tolerance

    @property
    def sortY(self) -> bool:
        """ Used to set the sorting mode (default sort along x)"""
        return self._sortY

    @sortY.setter
    def sortY(self, state: bool):
        self._sortY = state

    def sort(self, scanVectors):
        """
        Sorts the scan vectors
        """
        from scipy.spatial import distance_matrix
        theta_h = np.deg2rad(self._hatchAngle)
        midPoints = np.mean(scanVectors, axis=1)
        distMap = distance_matrix(midPoints, midPoints)
        distMap += np.eye(distMap.shape[0]) * 10000000.0
        G = nx.from_numpy_matrix(distMap < self._hatchTol)
        graphs = [G.subgraph(c) for c in nx.algorithms.connected_components(G)]
        clusterPaths = []
        for i in range(len(graphs)):
            gNodes = np.array([n for n in graphs[i]])
            norm = np.array([np.cos(theta_h), np.sin(theta_h)])
            idx2 = norm.dot(midPoints[gNodes].T)
            idx3 = np.argsort(idx2)
            shortPath = gNodes[idx3]
            clusterPaths.append(shortPath)

        scanVectorList = []
        lastScanIdx = [
         0] * len(clusterPaths)
        dPos = 0
        maxMove = dPos
        complete = False
        grpId = 0
        grp = []
        firstPnts = midPoints[[path[0] for path in clusterPaths]]
        if self._sortY:
            clusterPaths = [clusterPaths[i] for i in np.argsort(firstPnts[:, 1])]
        else:
            clusterPaths = [clusterPaths[i] for i in np.argsort(firstPnts[:, 0])]
        advancePos = True
        while not complete:
            if advancePos:
                maxMove += self._clusterDistance
            advancePos = True
            for i in range(len(clusterPaths)):
                innerDist = 0
                clusterNodes = np.array(clusterPaths[i])
                if lastScanIdx[i] == len(clusterNodes):
                    continue
                pnt = midPoints[clusterNodes[lastScanIdx[i]]]
                if self._sortY:
                    if pnt[1] > maxMove:
                        continue
                elif pnt[0] > maxMove:
                    continue
                while innerDist < self._clusterDistance:
                    if lastScanIdx[i] < len(clusterNodes):
                        scanVectorList.append(clusterNodes[lastScanIdx[i]])
                        grp.append(grpId)
                        lastScanIdx[i] += 1
                    if lastScanIdx[i] == len(clusterNodes):
                        break
                    pntCur = midPoints[clusterNodes[lastScanIdx[i]]]
                    pntPrev = midPoints[clusterNodes[(lastScanIdx[i] - 1)]]
                    delta = pntCur - pntPrev
                    if self._sortY:
                        innerDist += delta[1]
                        dPos = np.max([dPos, pntCur[1]])
                    else:
                        innerDist += delta[0]
                        dPos = np.max([dPos, pntCur[0]])

                grpId += 1
                advancePos = False
                break

            clusterLen = [len(path) for path in clusterPaths]
            complete = np.sum(np.array(lastScanIdx) - clusterLen) == 0

        idx6 = np.arange(len(midPoints))[scanVectorList]
        return scanVectors[idx6]