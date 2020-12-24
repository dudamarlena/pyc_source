# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/genonets_interface.py
# Compiled at: 2017-01-24 10:41:05
"""
    Public interface to Genonets functions.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import sys, copy
from multiprocessing import Process, Queue
from cmdl_handler import CmdArgs
from genonets_writer import Writer
from genonets_reader import InReader
from graph_utils import NetworkBuilder
from seq_bit_impl import BitManipFactory
from genonets_filters import WriterFilter
from analysis_handler import AnalysisHandler
from genonets_constants import ErrorCodes
from genonets_exceptions import GenonetsError
from genonets_constants import GenonetsConstants as Gc
from genonets_constants import AnalysisConstants as Ac

class Genonets:
    """
    Encapsulates the Genonets public API.
    """
    ALL = 0

    def __init__(self, args, process=False, parallel=False):
        """
        Initiate parsing of the input file, and load the parsed data into a `Genonets` object.

        A simple way to create a `Genonets` object is the following::

            gn = Genonets(CmdParser(args).getArgs())

        where, `CmdParser` can be imported as follows::

            from genonets.cmdl_handler import CmdParser

        The `args` variable is a list of command line arguments. Please see the `genonets` package
        documentation for the list and descriptions of all available command line arguments.

        :param args: A populated `CmdArgs` object.
        :param process: If 'True', in addition to creating the object, initiates complete processing, i,e., creates
                        genotype networks for all genotype sets in the input data, performs all available analyses on
                        all genotype networks, and generates all result files.
        :param parallel: Flag to indicate whether or not parallel processing should be used. This parameter is only
                         useful with 'process=True'.
        """
        self.cmdArgs = CmdArgs(args)
        self.inDataDict, self.deltaDict, self.seqToRepDict, self.seqLength, self.ordered_genotype_sets = self._build_data_dicts(self.cmdArgs.inFilePath)
        WriterFilter.ORDERED_GENOTYPE_SETS = self.ordered_genotype_sets
        self.bitManip = self._bit_manipulator()
        self.netBuilder = NetworkBuilder(self.bitManip, self.cmdArgs.use_reverse_complements)
        self.repToNetDict = {}
        self.repToGiantDict = {}
        self.pheno_net = None
        self.analyzer = None
        self.VERBOSE = True if self.cmdArgs.verbose else False
        if process:
            self._process_all(parallel)
        return

    def create(self, genotype_sets=Gc.ALL, parallel=False):
        """
        Create genotype networks for the given list of genotype set names.

        :param genotype_sets: List of names of the genotype sets for which the genotype
                             networks should be created. If a value is not explicitly
                             specified for this parameter, genotype networks are
                             constructed for all genotype sets available in the parsed
                             data.
        :param parallel: Flag to indicate whether or not parallel processing should
                         be used.
        :return: No return value
        """
        if self.VERBOSE:
            print 'Creating genotype networks:'
        genotype_sets = [genotype_sets] if type(genotype_sets) == str else genotype_sets
        if genotype_sets == Gc.ALL:
            genotype_sets = self.genotype_sets()
        if parallel:
            self._create_networks_parallel(genotype_sets)
        else:
            self._create_networks(genotype_sets)
        if self.VERBOSE:
            sys.stdout.write('Done.\n')

    def analyze(self, genotype_sets=Gc.ALL, analyses=Gc.ALL, parallel=False):
        """
        Performs all analyses provided in the list of analysis types, on the given genotype sets.

        This method can only be used if `create` has already been called on the same `Genonets`
        object.

        :param genotype_sets: List of names of the genotype sets for which the genotype
                            networks should be created. If a value is not explicitly
                            specified for this parameter, genotype networks are
                            constructed for all genotype sets available in the parsed
                            data.
        :param analyses: List of analysis type constants. These constants are defined in the class
                         `genonets.genonets_constants.AnalysisConstants`. If the value for this
                         parameter is not explicitly set, all available analyses are performed.
        :param parallel: Flag to indicate whether or not parallel processing should
                         be used.
        :return: No return value.
        """
        if self.VERBOSE:
            sys.stdout.write('\nPerforming analyses:')
        if genotype_sets == Gc.ALL:
            genotype_sets = self.genotype_sets()
        genotype_sets = [genotype_sets] if type(genotype_sets) == str else genotype_sets
        if analyses == Gc.ALL or Ac.OVERLAP in analyses:
            if len(genotype_sets) < 2:
                print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.NOT_ENOUGH_REPS_OLAP) + ': Tau=' + str(self.cmdArgs.tau)
                raise GenonetsError(ErrorCodes.NOT_ENOUGH_REPS_OLAP, 'Tau=' + str(self.cmdArgs.tau))
        if parallel:
            self._analyze_networks_parallel(genotype_sets, analyses)
            if analyses == Gc.ALL or Ac.OVERLAP in analyses:
                del self.analyzer
                self.analyzer = AnalysisHandler(self)
                self._analyze_networks(genotype_sets, [Ac.OVERLAP])
        else:
            self._analyze_networks(genotype_sets, analyses)

    def phenotype_network(self, collection_name='phenotype_network', genotype_sets=Gc.ALL):
        """
        Create the phenotype network from the given list of genotype sets.

        :param collection_name: The name to be assigned to the phenotype network.
        :param genotype_sets: List of names of the genotype sets for which the phenotype
                              network should be created. If a value is not explicitly
                              specified for this parameter, all available genotype sets
                              are considered.
        :return: `igraph.Graph` object representing the phenotype network.
        """
        genotype_sets = [genotype_sets] if type(genotype_sets) == str else genotype_sets
        if genotype_sets == Gc.ALL:
            genotype_sets = self.genotype_sets()
        giants = [ self.repToGiantDict[repertoire] for repertoire in genotype_sets ]
        self.pheno_net = self.netBuilder.createEvoNet(collection_name, giants)
        return self.pheno_net

    def genotype_sets(self):
        """
        Get a list of names of all genotype sets for which genotype networks have been created.

        :return: List of names of genotype sets.
        """
        repertoires = self.inDataDict.keys()
        repertoires = [repertoires] if type(repertoires) == str else repertoires
        return repertoires

    def genotype_network(self, genotype_set):
        """target="_blank"
        Get the `igraph` object for the network corresponding to the given genotype set name.

        The `igraph` object in this case refers to the entire network, i.e., all connected
        components.

        Note: This method can only be used if the genotype network corresponding to the requested
        genotype set name has already been created.

        :param genotype_set: Name of the genotype set for which the genotype network is
                             requested.
        :return: Object of type `igraph.Graph`.
        """
        try:
            return self.repToNetDict[genotype_set]
        except KeyError:
            return

        return

    def dominant_network(self, genotype_set):
        """
        Get the `igraph` object for the *dominant* network corresponding to the given genotype set name.

        The dominant network refers to the giant component in the network.

        Note: This method can only be used if the genotype network corresponding to the requested
        genotype set name has already been created.

        :param genotype_set: Name of the genotype set for which the genotype network is
                             requested.
        :return: Object of type `igraph.Graph`.
        """
        try:
            return self.repToGiantDict[genotype_set]
        except KeyError:
            return

        return

    def save(self, genotype_sets=Gc.ALL):
        """
        Write the genotype networks corresponding to the given genotype sets to file.

        The networks are saved in GML format. For networks with more than one
        components, separate files are generated for the entire network and the
        dominant network.

        Note: This method can be used only after `analyze()` has been called on the
        given genotype sets.

        :param genotype_sets: List of names of genotype sets for which the genotype
                              should be written to file. If a value is not explicitly specified
                              for this parameter, result files are written for all
                              genotype sets.
        :return: No return value.
        """
        if self.VERBOSE:
            sys.stdout.write('\nWriting GML files for genotype networks ... ')
        genotype_sets = [genotype_sets] if type(genotype_sets) == str else genotype_sets
        Writer.writeNetsToFile(self.repToNetDict, self.repToGiantDict, self.netBuilder, self.cmdArgs.outPath, WriterFilter.gmlAttribsToIgnore, genotype_sets)
        if self.VERBOSE:
            sys.stdout.write('Done.\n')

    def save_network_results(self, genotype_sets=Gc.ALL):
        """
        Write the genotype set level results to file.

        A file named 'Genotype_set_measures.txt' is generated in the output directory
        specified at the time of the `Genonets` object creation.

        Note: This method can be used only after `analyze()` has been called on the
        given genotype sets.

        :param genotype_sets: List of names of genotype sets for which to generate the
                              result files. If a value is not explicitly specified
                              for this parameter, result files are written for all
                              genotype sets.
        :return: No return value.
        """
        if self.VERBOSE:
            sys.stdout.write('\nWriting genotype set level results ... ')
        genotype_sets = [genotype_sets] if type(genotype_sets) == str else genotype_sets
        Writer.writeNetAttribs(self.repToNetDict, self.repToGiantDict, self.netBuilder, self.cmdArgs.outPath, WriterFilter.netAttribsToIgnore, WriterFilter.net_attribute_to_order, WriterFilter.genotype_set_to_order, genotype_sets)
        if self.VERBOSE:
            sys.stdout.write('Done.\n')

    def save_genotype_results(self, genotype_sets=Gc.ALL):
        """
        Write the genotype level results to files.

        A results file is generated for each genotype set.

        Note: This method can be used only after `analyze()` has been called on the
        given genotype sets.

        :param genotype_sets: List of names of genotype sets for which to generate the
                              result files. If a value is not explicitly specified
                              for this parameter, result files are written for all
                              genotype sets.
        :return: No return value.
        """
        if self.VERBOSE:
            sys.stdout.write('\nWriting genotype level results ... ')
        genotype_sets = [genotype_sets] if type(genotype_sets) == str else genotype_sets
        Writer.writeSeqAttribs(self.repToGiantDict, self.cmdArgs.outPath, WriterFilter.seqAttribsToIgnore, WriterFilter.seq_attribute_to_order, genotype_sets)
        if self.VERBOSE:
            sys.stdout.write('Done.\n')

    def save_phenotype_network(self):
        """
        Write the phenotype network to file in GML format.

        Note: This method can only be used after the phenotype network has been created.

        :return: No return value.
        """
        if self.VERBOSE:
            sys.stdout.write('\nWriting GML file for phenotype network ... ')
        Writer.writeNetToFile(self.pheno_net, self.cmdArgs.outPath, WriterFilter.gmlAttribsToIgnore)
        if self.VERBOSE:
            sys.stdout.write('Done.\n')

    def plot(self, network, layout='auto'):
        self.netBuilder.plotNetwork(network, layout, self.cmdArgs.outPath)

    def _build_data_dicts(self, inFilePath):
        return InReader.build_data_dicts(inFilePath, self.cmdArgs.tau, self.cmdArgs.moleculeType)

    def _bit_manipulator(self):
        return BitManipFactory.getBitSeqManip(self.cmdArgs.moleculeType, self.seqLength, self.cmdArgs.useIndels, self.cmdArgs.use_reverse_complements)

    def _bitseqs_and_scores(self, repertoire):
        sequences = self.inDataDict[repertoire].keys()
        scores = [ self.inDataDict[repertoire][seq] for seq in sequences ]
        return (
         sequences, scores)

    def _process_all(self, parallel):
        self.create(parallel=parallel)
        self.analyze(parallel=parallel)
        self.save()
        self.save_network_results()
        self.save_genotype_results()
        self.phenotype_network()
        self.save_phenotype_network()

    def _create_networks(self, repertoires):
        for repertoire in repertoires:
            if self.VERBOSE:
                sys.stdout.write(repertoire + ' ... ')
            seqs, scores = self._bitseqs_and_scores(repertoire)
            self.repToNetDict[repertoire] = self.netBuilder.createGenoNet(repertoire, seqs, scores)
            numComponents = len(self.netBuilder.getComponents(self.repToNetDict[repertoire]))
            if numComponents > 1:
                giant = self.netBuilder.getGiantComponent(self.repToNetDict[repertoire])
                giant['name'] = repertoire + '_dominant'
                self.repToGiantDict[repertoire] = giant
            else:
                self.repToGiantDict[repertoire] = self.repToNetDict[repertoire]

    def _create_networks_parallel(self, repertoires):
        resultsQueue = Queue()
        indices = Genonets._process_blocks(len(repertoires), self.cmdArgs.num_procs)
        for i in indices:
            processes = [ Process(target=Genonets._create_gn, args=(self.inDataDict[repertoires[j]], self.cmdArgs, self.seqLength, resultsQueue, repertoires[j])) for j in range(i - 1, Genonets._len_finished_reps(i, len(repertoires), self.cmdArgs.num_procs))
                        ]
            for p in processes:
                p.start()

            while len(self.repToNetDict) != Genonets._len_finished_reps(i, len(repertoires), self.cmdArgs.num_procs):
                result = resultsQueue.get()
                if self.VERBOSE:
                    sys.stdout.write(result[0] + ' ... ')
                self.repToNetDict[result[0]] = result[1][0]
                self.repToGiantDict[result[0]] = result[1][1]

    @staticmethod
    def _create_gn(seqScrDict, args, seqLength, resultsQueue, repertoire):
        bitManip = BitManipFactory.getBitSeqManip(args.moleculeType, seqLength, args.useIndels, args.use_reverse_complements)
        sequences = seqScrDict.keys()
        scores = [ seqScrDict[sequence] for sequence in sequences ]
        netBuilder = NetworkBuilder(bitManip, args.use_reverse_complements)
        network = netBuilder.createGenoNet(repertoire, sequences, scores)
        numComponents = len(netBuilder.getComponents(network))
        if numComponents > 1:
            giant = netBuilder.getGiantComponent(network)
            giant['name'] = repertoire + '_dominant'
        else:
            giant = network
        netTuple = (
         repertoire, (network, giant))
        resultsQueue.put(netTuple)
        resultsQueue.close()

    def _analyze_networks(self, repertoires, analyses):
        self.analyzer = AnalysisHandler(self, analyses)
        for repertoire in repertoires:
            if self.VERBOSE:
                sys.stdout.write('\n' + repertoire + ':')
                sys.stdout.write('\n\t')
            self.analyzer.analyze(repertoire, analyses)

        if self.VERBOSE:
            print

    def _analyze_networks_parallel(self, repertoires, analyses):
        if self.VERBOSE:
            print
        self_copy = copy.deepcopy(self)
        del self.repToNetDict
        del self.repToGiantDict
        self.repToNetDict = {}
        self.repToGiantDict = {}
        resultsQueue = Queue()
        indices = Genonets._process_blocks(len(repertoires), self.cmdArgs.num_procs)
        for i in indices:
            processes = [ Process(target=Genonets._analyze_gn, args=(copy.deepcopy(self_copy), analyses, resultsQueue, repertoires[j])) for j in range(i - 1, Genonets._len_finished_reps(i, len(repertoires), self.cmdArgs.num_procs))
                        ]
            for p in processes:
                p.start()

            while len(self.repToNetDict) != Genonets._len_finished_reps(i, len(repertoires), self.cmdArgs.num_procs):
                result = resultsQueue.get()
                if self.VERBOSE:
                    print '\tAnalysis results received for: ' + result[0]
                self.repToNetDict[result[0]] = result[1][0]
                self.repToGiantDict[result[0]] = result[1][1]

    @staticmethod
    def _process_blocks(num_repertoires, num_processes):
        if num_repertoires <= num_processes:
            indices = [1]
        else:
            num_full_iters = num_repertoires / num_processes
            incr_last = num_repertoires % num_processes
            index_incrs = [ num_processes for _ in range(num_full_iters) ] if num_full_iters != 0 else []
            if incr_last != 0:
                index_incrs.append(incr_last)
            indices = [
             1]
            for i in range(0, len(index_incrs) - 1):
                indices.append(index_incrs[i] + indices[i])

        return indices

    @staticmethod
    def _len_finished_reps(cur_index, len_repertoires, max_procs):
        return min(len_repertoires, cur_index - 1 + max_procs)

    def analyzeNets_parallel_old(self, repertoires, analyses):
        resultsQueue = Queue()
        processes = [ Process(target=Genonets._analyze_gn, args=(copy.deepcopy(self), analyses, resultsQueue, repertoire)) for repertoire in repertoires
                    ]
        for p in processes:
            p.start()

        del self.repToNetDict
        del self.repToGiantDict
        self.repToNetDict = {}
        self.repToGiantDict = {}
        while len(self.repToNetDict) != len(repertoires):
            result = resultsQueue.get()
            print 'Analysis results received for: ' + result[0]
            self.repToNetDict[result[0]] = result[1][0]
            self.repToGiantDict[result[0]] = result[1][1]

    @staticmethod
    def _analyze_gn(genonetsCopy, analyses, resultsQueue, repertoire):
        analyzer = AnalysisHandler(genonetsCopy, parallel=True)
        analyzer.analyze(repertoire, analyses)
        resultTuple = (
         repertoire,
         (
          genonetsCopy.genotype_network(repertoire),
          genonetsCopy.dominant_network(repertoire)))
        resultsQueue.put(resultTuple)
        resultsQueue.close()

    def _overlap_matrix(self):
        if len(self.repToGiantDict) == 0:
            print 'Overlap matrix cannot be computed before network creation.'
            return
        else:
            if self.analyzer.overlapMatrix:
                return self.analyzer.overlapMatrix
            else:
                self.analyzer.overlap()
                return self.analyzer.overlapMatrix

            return