# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/lib/primers.py
# Compiled at: 2017-03-26 21:20:45
from Probe import ProbeSet
from Probe import Probe
from Bio import SeqIO
from warnings import simplefilter
from Bio import BiopythonWarning
import os.path as op
from os import makedirs
import logging
from sys import exit
from Report import ReportGenerator
simplefilter('ignore', BiopythonWarning)

class PrimersGenerator:
    """Describes the entire pipeline to generate primers

    Parameters:
    -----------
    args: ArgParse object
          Settings to run the pipeline
    """

    def __init__(self, args):
        self.args = args
        if not op.exists(self.args.output_prefix):
            makedirs(self.args.output_prefix)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-8s' + ' %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename=op.join(self.args.output_prefix, self.args.output_prefix + '.log'), filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-3s:%(levelname)-3s:' + ' %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        self.targets_names = []
        for target in self.args.targets_ids:
            self.targets_names.append(target.rstrip('\n'))

        self.print_parameters()

    def print_parameters(self):
        """Prints the pipeline settings

        Returns:
        Void

        """
        logger = logging.getLogger('gp.conf')
        logger.info("Universe's FASTA file:")
        logger.info('  ' + self.args.fasta_indx)
        logger.info('Targets IDs:')
        for target in self.targets_names:
            logger.info('  ' + target)

        logger.info('Primer filtering options')
        logger.info('\tMinimum primer size: ' + str(self.args.min_prim_size) + ' bp')
        logger.info('\tMaximum primer size: ' + str(self.args.max_prim_size) + ' bp')
        logger.info('\tMinimum local composition complexity: ' + str(self.args.lcc))
        logger.info('\tMinimum GC percentage: ' + str(self.args.min_gc) + '%')
        logger.info('\tMaximum GC percentage: ' + str(self.args.max_gc) + '%')
        logger.info('\tMinimum melting temperature: ' + str(self.args.min_melt) + ' C')
        logger.info('\tMaximum melting temperature: ' + str(self.args.max_melt) + ' C')
        logger.info('\tMinimum energy for hairpir formation: ' + str(self.args.dgss) + ' kcal/mol')
        logger.info('\tMinimum energy for homodimer formation: ' + str(self.args.dghm) + ' kcal/mol')
        logger.info('\tEdit distance for alignment: ' + str(self.args.edit_distance))
        logger.info('Primers pairs options')
        logger.info('\tMinimum amplicon size: ' + str(self.args.min_amp_size) + ' bp')
        logger.info('\tMaximum amplicon size: ' + str(self.args.max_amp_size) + ' bp')
        logger.info('\tMinimum energy for heterodimer formation: ' + str(self.args.ppdghm) + ' kcal/mol')
        logger.info('\tTarget fraction: ' + str(self.args.target_frac))
        logger.info('Output options')
        logger.info('\tOutput prefix: ' + self.args.output_prefix)
        logger.info('\tPrimers prefix: ' + self.args.primers_prefix)
        logger.info('\tMaximum number of pairs reported: ' + str(self.args.records))

    def run_pipeline(self):
        """Executes each step of the pipeline

        Returns:
        --------
        Void

        """
        fasta_indx = self.args.fasta_indx
        min_prim_size = self.args.min_prim_size
        max_prim_size = self.args.max_prim_size
        na = self.args.na
        mg = self.args.mg
        op_temp = self.args.op_temp
        lcc = self.args.lcc
        min_melt = self.args.min_melt
        max_melt = self.args.max_melt
        min_gc = self.args.min_gc
        max_gc = self.args.max_gc
        dgss = self.args.dgss
        dghm = self.args.dghm
        sdss = self.args.sdss
        nmiss = self.args.edit_distance
        sdss = self.args.sdss
        prim_con = self.args.prim_con
        targets_frac = self.args.target_frac
        min_amp_size = self.args.min_amp_size
        max_amp_size = self.args.max_amp_size
        max_pairs = self.args.records
        ppdghm = self.args.ppdghm
        p_prefix = self.args.primers_prefix
        targets_records = self.__get_targets_sequences__(fasta_indx, self.targets_names)
        raw_probes = self.__generate_raw_probes__(targets_records, min_prim_size, max_prim_size, p_prefix)
        ps = ProbeSet(raw_probes)
        ps.filter_probes(na, mg, op_temp, lcc, min_melt, max_melt, min_gc, max_gc, dgss, dghm, prim_con)
        ps.get_sdss_regions(op_temp, na, sdss, prim_con)
        ps.assign_coords(fasta_indx, nmiss)
        ps.def_primers_pairs(targets_records, targets_frac, min_amp_size, max_amp_size, ppdghm, na, mg, prim_con, op_temp, max_pairs)
        rg = ReportGenerator(self.args, ps, targets_records)
        rg.generate_report()

    def __get_targets_sequences__(self, fasta_file, targets_names):
        """Retrieves target sequences

        Args:
        -----
        fasta_file: String
                    Path to the indexed FASTA file containing the set of all
                    sequneces

        targets_names: List<String>
                       List with the IDs of the targets sequences to be
                       retrieved

        Return:
        -------
        dict(seq_id: SeqRecord): Python dictionary with the SeqRecords of the
        target sequence

        Notes:
        ------
        Targets sequences are those sequences that the users wants to amplify

        """
        logger = logging.getLogger('gp.target.seqs')
        logger.info('Retrieving target sequences')
        univ_dict = SeqIO.index(fasta_file, 'fasta')
        target_records = []
        for target in targets_names:
            record = univ_dict[target]
            if record is not None:
                target_records.append(record)
            else:
                logger.warning('Target sequence ' + target + ' could not be found in the universe')

        n_targets_ret = len(target_records)
        if n_targets_ret == 0:
            logger.error('No targets could be retrieved, quiting ..')
            exit()
        else:
            logger.info(str(n_targets_ret) + ' target were retrieved')
        return target_records

    def __generate_raw_probes__(self, sequences, lmin, lmax, p_prefix):
        """Given a list of Biopython SeqRecords, generates all the posible probes

        Args:
        -----
        sequences: dict(seq_id: SeqRecord)
                   Python dict with the BioPython SeqRecords of the sequences
        lmin      : Integer
                    Minimum subsequence size
        lmax      : Integer
                    Maximum subsequence size
        Return:
        -------
        dict(Probe_id: Probe): Python dictionary containing a set of
                               instances of the Probe class that represent
                               all the posible probes that can be generated
                               from the sequences
        Notes:
        ------
        All the posible probes are extracted searching for all the
        kmers between lmin and lmax that can be retrieved for the set of
        sequences
        """
        logger = logging.getLogger('gp.raw.primers')
        logger.info('Generating raw primers')
        probes_freq = dict()
        probes_set = dict()
        for ksize in range(lmin, lmax + 1):
            for record in sequences:
                seq_len = len(record.seq)
                for i in range(0, seq_len - ksize):
                    tmp_kmer = record.seq[i:i + ksize]
                    probes_freq[tmp_kmer] = probes_freq.get(tmp_kmer, 0) + 1

        tmp_freq = probes_freq.copy()
        for probe in tmp_freq:
            tmp_kmer_rev = probe.reverse_complement()
            probes_freq[tmp_kmer_rev] = probes_freq.get(tmp_kmer_rev, 0) + 1

        n_probes = len(probes_freq)
        n_digits = len(str(n_probes))
        cont = 1
        for probe in probes_freq:
            probe_id = p_prefix + str(cont).zfill(n_digits)
            cont += 1
            probes_set[probe_id] = Probe(probe_id, probe)

        logger.info(str(len(probes_set)) + ' raw primers were generated')
        return probes_set