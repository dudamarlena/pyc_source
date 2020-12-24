# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/peak_functions.py
# Compiled at: 2017-01-31 16:34:36
"""
    peaks_functions
    ~~~~~~~~~~~~~~~

    Contains functions used for computation of peaks.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from genonets_utils import Utils

class PeakAnalyzer:

    def __init__(self, network, netUtils, delta):
        self.network = network
        self.netUtils = netUtils
        self.bitManip = netUtils.bitManip
        self.delta = delta
        self.peaks = None
        return

    def getPeakWithSeq(self, seq):
        peaks = self.getPeaks()
        for peakId in peaks.keys():
            peak = peaks[peakId]
            if seq in peak['sequences']:
                return peak

        print 'Error: Count not find ' + seq + ' in any peak!!!!'
        return

    def getPeaks(self, recompute=False):
        if not self.peaks or recompute:
            sortedArr = Utils.getSortedSeqEscArr(self.network, self.bitManip.seqLength, sortOrder='descending')
            self.peaks = self.buildPeaks(sortedArr)
        return self.peaks

    def buildPeaks(self, elements):
        peaks = {}
        processed = []
        for i in range(len(elements)):
            if elements[i] in processed:
                continue
            binMembers = self.getBin(i, elements)
            neutralZone, nonNeighs = self.getNeutralZone(elements[i], binMembers)
            neutralZone.append(elements[i])
            peakNonNeighs = self.getPeaksNonNeighs(elements[i], peaks)
            neighboringPeaks = self.getNeighPeaks(neutralZone, peakNonNeighs, peaks)
            if neighboringPeaks:
                self.appendToPeaks(neutralZone, neighboringPeaks, peaks)
                if len(neutralZone) > 1:
                    processed.extend(neutralZone)
            else:
                peakId = len(peaks)
                peaks[peakId] = self.createPeak(neutralZone, nonNeighs)
                if len(neutralZone) > 1:
                    processed.extend(neutralZone)

        return peaks

    def getBin(self, index, elements):
        elBin = []
        focalElement = elements[index]
        for i in range(index + 1, len(elements)):
            if elements[i]['escore'] >= focalElement['escore'] - self.delta:
                elBin.append(elements[i])
            else:
                break

        return elBin

    def getNeutralZone(self, focalElement, binMembers):
        neighSeqs = self.getNeighSeqs(focalElement)
        neutralZone = [ item for item in binMembers if item['sequence'] in neighSeqs ]
        nonNeighs = [ binMembers[i] for i in range(len(binMembers)) if binMembers[i] not in neutralZone
                    ]
        neutralZone, nonNeighs = self.bfsNeutralZone(neutralZone, nonNeighs)
        return (
         neutralZone, nonNeighs)

    def bfsNeutralZone(self, neutralZone, nonNeighs):
        i = 0
        while i < len(neutralZone):
            removeList = []
            for nonNeigh in nonNeighs:
                if self.netUtils.areConnected(nonNeigh['sequence'], neutralZone[i]['sequence']):
                    neutralZone.append(nonNeigh)
                    removeList.append(nonNeigh)

            nonNeighs = [ item for item in nonNeighs if item not in removeList ]
            i += 1

        return (neutralZone, nonNeighs)

    def getPeaksNonNeighs(self, focalElement, peaks):
        return [ peakId for peakId in peaks.keys() if focalElement in peaks[peakId]['non-neighbors']
               ]

    def getNeighPeaks(self, neutralZone, peakNonNeighs, peaks):
        neighboringPeaks = []
        for element in neutralZone:
            peaksAsNeighs = self.getNeighPeaksFor(element, peakNonNeighs, peaks)
            if peaksAsNeighs:
                neighboringPeaks.extend(peaksAsNeighs)

        neighboringPeaks = list(set(neighboringPeaks))
        return neighboringPeaks

    def getNeighPeaksFor(self, element, peakNonNeighs, peaks):
        peakIds = []
        for peakId in peaks.keys():
            if peakId in peakNonNeighs:
                continue
            pathList = peaks[peakId]['list']
            for item in pathList:
                if self.netUtils.areConnected(item['sequence'], element['sequence']):
                    peakIds.append(peakId)
                    break

        return peakIds

    def createPeak(self, neutralZone, nonNeighs):
        peak = {}
        neutralZone.reverse()
        peak['sequences'] = [ neutralZone[i][0] for i in range(len(neutralZone))
                            ]
        peak['list'] = neutralZone
        peak['non-neighbors'] = nonNeighs
        return peak

    def appendToPeaks(self, neutralZone, neighboringPeaks, peaks):
        for peakId in neighboringPeaks:
            peaks[peakId]['list'].extend(neutralZone)

    def getNeighSeqs(self, element):
        return [ self.network.vs[neighbor]['sequences'] for neighbor in self.netUtils.getNeighbors(element['sequence'], self.network)
               ]