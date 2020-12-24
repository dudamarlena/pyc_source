# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/analysis_handler.py
# Compiled at: 2017-02-02 12:52:39
"""
    analysis_handler
    ~~~~~~~~~~~~~~~~

    Exposes wrapper functions, one per analysis type. Serves as a collective
    interface to handler classes for all analysis types.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import sys, json
from genonets_writer import Writer
from genonets_filters import WriterFilter
from path_functions import PathAnalyzer
from landscape_functions import Landscape
from overlap_functions import OverlapAnalyzer
from structure_functions import StructureAnalyzer
from robustness_functions import RobustnessAnalyzer
from evolvability_functions import EvolvabilityAnalyzer
from accessibility_functions import AccessibilityAnalyzer
from genonets_constants import AnalysisConstants as Ac
from genonets_constants import EpistasisConstants as Epi

class AnalysisHandler:

    def __init__(self, caller, analyses=Ac.ALL, parallel=False):
        self.caller = caller
        self.parallel = parallel
        self.repToNetDict = self.caller.repToNetDict
        self.repToGiantDict = self.caller.repToGiantDict
        self.netBuilder = self.caller.netBuilder
        self.bitManip = self.caller.bitManip
        self.inDataDict = self.caller.inDataDict
        self.deltaDict = self.caller.deltaDict
        self.seqToRepDict = self.caller.seqToRepDict
        self.VERBOSE = self.caller.VERBOSE
        self.analysisToFunc = {Ac.PEAKS: self.peaks, 
           Ac.PATHS: self.paths, 
           Ac.PATHS_RATIOS: self.paths_ratios, 
           Ac.EPISTASIS: self.epistasis, 
           Ac.ROBUSTNESS: self.robustness, 
           Ac.EVOLVABILITY: self.evolvability, 
           Ac.ACCESSIBILITY: self.accessibility, 
           Ac.NEIGHBOR_ABUNDANCE: self.neighborAbundance, 
           Ac.PHENOTYPIC_DIVERSITY: self.phenotypicDiversity, 
           Ac.STRUCTURE: self.structure, 
           Ac.OVERLAP: self.overlap}
        self.isDoubleStranded = self.caller.cmdArgs.use_reverse_complements
        if analyses == Ac.ALL or Ac.EVOLVABILITY in analyses:
            self.seqToRepDict_evo = None
            self.rcToSeqDict = None
            self.bitsToSeqDict = None
            self.init_evolvability()
        self.overlapMatrix = None
        return

    def getFuncsFor(self, analysis):
        try:
            funcs = self.analysisToFunc[analysis]
            if type(funcs) == list:
                return funcs
            return [funcs]
        except KeyError:
            return

        return

    def analyze(self, repertoire, analyses=Ac.ALL):
        if analyses == Ac.ALL:
            analyses = self.analysisToFunc.keys()
        for analysis in analyses:
            if self.VERBOSE and not self.parallel:
                sys.stdout.write(Ac.analysisToDesc[analysis] + ' ... ')
            functions = self.getFuncsFor(analysis)
            for function in functions:
                function(repertoire)

        if self.VERBOSE and not self.parallel:
            sys.stdout.write('Done.')

    def getLandscapeObj(self, giant, repertoire):
        lscape = Landscape(giant, self.netBuilder, self.inDataDict[repertoire], self.deltaDict[repertoire], self.bitManip)
        return lscape

    def peaks(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        lscape = self.getLandscapeObj(giant, repertoire)
        peaks = lscape.getPeaks(recompute=True)
        giant['Number_of_peaks'] = len(peaks)
        giant['Peaks'] = {peakId:peaks[peakId]['sequences'] for peakId in peaks.keys()}
        lscape.populateDistsToSummit()

    def paths(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        lscape = self.getLandscapeObj(giant, repertoire)
        lscape.getAccessiblePaths(0)
        giant['Summit'] = lscape.pathAnalyzer.getSummitId()
        allPathsToPeak = lscape.pathAnalyzer.getAllPathsToPeak()
        giant.vs['pathsToSummit'] = [ allPathsToPeak[i] for i in range(len(allPathsToPeak))
                                    ]
        giant.vs['Accessible_paths_through'] = lscape.pathAnalyzer.getPathsThruVtxs()

    def paths_ratios(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        path_analyzer = PathAnalyzer(giant, self.netBuilder, self.deltaDict[repertoire])
        path_analyzer.getAccessiblePaths()
        max_path_length = path_analyzer.max_path_length
        giant['Ratio_of_accessible_mutational_paths'] = {i:path_analyzer.getAccessiblePaths(i) for i in xrange(2, max_path_length + 1)}

    def epistasis(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        lscape = self.getLandscapeObj(giant, repertoire)
        epistasis = lscape.getEpistasis()
        vtxToSqrs, squares = lscape.epiAnalyzer.getVertexToSquaresDict()
        giant['Squares_list'] = json.dumps(squares)
        giant['SqrEpi_list'] = json.dumps(lscape.epiAnalyzer.getSqrEpi())
        giant['Number_of_squares'] = len(lscape.epiAnalyzer.squares)
        giant['Magnitude_epistasis'] = epistasis[Epi.MAGNITUDE]
        giant['Simple_sign_epistasis'] = epistasis[Epi.SIGN]
        giant['Reciprocal_sign_epistasis'] = epistasis[Epi.RECIPROCAL_SIGN]
        if len(vtxToSqrs) > 0:
            giant.vs['VtxToSqrs'] = [ vtxToSqrs[i] for i in range(len(vtxToSqrs)) ]
        else:
            giant.vs['VtxToSqrs'] = [[]]

    def robustness(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        robAnalyzer = RobustnessAnalyzer(giant, self.netBuilder, self.isDoubleStranded)
        giant['Robustness'] = robAnalyzer.getAvgRobustness()
        giant.vs['Robustness'] = robAnalyzer.getRobustnessAll()

    def init_evolvability(self):
        self.seqToRepDict_evo = EvolvabilityAnalyzer.updateSeqToRepDict(self.seqToRepDict, self.repToGiantDict)
        if self.isDoubleStranded:
            self.rcToSeqDict = EvolvabilityAnalyzer.buildRcToSeqDict(self.seqToRepDict_evo, self.bitManip)
        self.bitsToSeqDict = EvolvabilityAnalyzer.buildBitsToSeqDict(self.seqToRepDict_evo, self.rcToSeqDict, self.bitManip, self.isDoubleStranded)

    def evolvability(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        evoAnalyzer = EvolvabilityAnalyzer(giant, self.inDataDict, self.seqToRepDict_evo, self.repToGiantDict, self.rcToSeqDict, self.bitsToSeqDict, self.netBuilder, self.isDoubleStranded)
        repertoireEvo, targetRepertoires = evoAnalyzer.getReportoireEvo()
        giant['Evolvability'] = repertoireEvo
        giant['Evolvability_targets'] = json.dumps(targetRepertoires)
        evoTuples = evoAnalyzer.getEvoAll()
        evoScores = [ evoTuples[i][0] for i in range(len(evoTuples)) ]
        evoTargets = [ evoTuples[i][1] for i in range(len(evoTuples)) ]
        giant.vs['Evolvability'] = evoScores
        giant.vs['Evolves_to_genotypes_in'] = [ evoTargets[i].keys() for i in range(len(evoTargets))
                                              ]
        giant.vs['Evolvability_targets'] = evoTargets

    def accessibility(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        accAnalyzer = AccessibilityAnalyzer(repertoire, giant, self.repToGiantDict, self.inDataDict, self.netBuilder, self.bitManip, self.isDoubleStranded)
        giant['Accessibility'] = accAnalyzer.getAccessibility()

    def neighborAbundance(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        accAnalyzer = AccessibilityAnalyzer(repertoire, giant, self.repToGiantDict, self.inDataDict, self.netBuilder, self.bitManip, self.isDoubleStranded)
        giant['Neighbor_abundance'] = accAnalyzer.getNeighborAbundance()

    def phenotypicDiversity(self, repertoire):
        giant = self.caller.dominant_network(repertoire)
        accAnalyzer = AccessibilityAnalyzer(repertoire, giant, self.repToGiantDict, self.inDataDict, self.netBuilder, self.bitManip, self.isDoubleStranded)
        giant['Diversity_index'] = accAnalyzer.getPhenotypicDivesity()

    def structure(self, repertoire):
        network = self.caller.genotype_network(repertoire)
        giant = self.caller.dominant_network(repertoire)
        structAnalyzer = StructureAnalyzer(network, self.netBuilder)
        network['Genotype_network_sizes'] = str(structAnalyzer.getComponentSizes())
        network['Number_of_genotype_networks'] = structAnalyzer.getNumComponents()
        network['Size_of_dominant_genotype_network'] = structAnalyzer.getDominantSize()
        network['Proportional_size_of_dominant_genotype_network'] = structAnalyzer.getPercentDominantSize()
        giant['Edge_density'] = structAnalyzer.getEdgeDensity()
        giant['Diameter'] = structAnalyzer.getDiameter()
        giant['Average_clustering_coefficient_of_dominant_genotype_network'] = structAnalyzer.getAvgClstrCoeff()
        giant['Assortativity'] = structAnalyzer.getAssortativity()
        giant['diameterPath_list'] = json.dumps(structAnalyzer.getDiameterPath())
        giant.vs['Coreness'] = structAnalyzer.getCoreness()
        giant.vs['Clustering_coefficient'] = structAnalyzer.getClusteringCoefficients()

    def overlap(self, r=None):
        if self.parallel:
            return
        if not self.overlapMatrix:
            overlapAnalyzer = OverlapAnalyzer(self.repToGiantDict, self.caller.genotype_sets(), self.bitManip, self.isDoubleStranded, WriterFilter.genotype_set_to_order)
            self.overlapMatrix, repertoires, overlapDict = overlapAnalyzer.getOverlapData()
            if overlapDict:
                for repertoire in self.caller.genotype_sets():
                    giant = self.repToGiantDict[repertoire]
                    giant['Overlapping_genotype_sets'] = set()
                    seqDict = overlapDict[repertoire]
                    for sequence in seqDict.keys():
                        vertex = self.netBuilder.getVertex(sequence, giant)
                        overlapping_seqs = seqDict[sequence]
                        giant.vs[vertex.index]['Overlaps_with_genotypes_in'] = overlapping_seqs
                        giant['Overlapping_genotype_sets'] |= set(overlapping_seqs)

                    giant['Overlapping_genotype_sets'] = list(giant['Overlapping_genotype_sets'])
                    try:
                        ratio = float(len(giant['Overlapping_genotype_sets'])) / (float(len(self.caller.genotype_sets())) - 1)
                    except ZeroDivisionError:
                        ratio = 0

                    giant['Ratio_of_overlapping_genotype_sets'] = ratio

            if self.overlapMatrix:
                Writer.writeOverlapToFile(self.overlapMatrix, repertoires, self.caller.cmdArgs.outPath)