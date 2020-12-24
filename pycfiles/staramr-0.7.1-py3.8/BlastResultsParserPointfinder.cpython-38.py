# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/results/pointfinder/BlastResultsParserPointfinder.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 4189 bytes
import logging
from os import path
import staramr.blast.results.BlastResultsParser as BlastResultsParser
import staramr.blast.results.pointfinder.PointfinderHitHSP as PointfinderHitHSP
import staramr.blast.results.pointfinder.nucleotide.PointfinderHitHSPRNA as PointfinderHitHSPRNA
logger = logging.getLogger('BlastResultsParserPointfinder')

class BlastResultsParserPointfinder(BlastResultsParser):
    COLUMNS = [x.strip() for x in '\n    Isolate ID\n    Gene\n    Type\n    Position\n    Mutation\n    %Identity\n    %Overlap\n    HSP Length/Total Length\n    Contig\n    Start\n    End\n    '.strip().split('\n')]
    SORT_COLUMNS = ['Isolate ID', 'Gene']

    def __init__(self, file_blast_map, blast_database, pid_threshold, plength_threshold, report_all=False, output_dir=None, genes_to_exclude=[]):
        """
        Creates a new BlastResultsParserPointfinder.
        :param file_blast_map: A map/dictionary linking input files to BLAST results files.
        :param blast_database: The particular staramr.blast.AbstractBlastDatabase to use.
        :param pid_threshold: A percent identity threshold for BLAST results.
        :param plength_threshold: A percent length threshold for results.
        :param report_all: Whether or not to report all blast hits.
        :param output_dir: The directory where output files are being written.
        :param genes_to_exclude: A list of gene IDs to exclude from the results.
        """
        super().__init__(file_blast_map, blast_database, pid_threshold, plength_threshold, report_all, output_dir=output_dir,
          genes_to_exclude=genes_to_exclude)

    def _create_hit(self, file, database_name, blast_record):
        logger.debug('database_name=%s', database_name)
        if database_name == '16S_rrsD' or database_name == '23S':
            return PointfinderHitHSPRNA(file, blast_record)
        return PointfinderHitHSP(file, blast_record)

    def _get_result(self, hit, db_mutation):
        return [
         hit.get_genome_id(),
         hit.get_amr_gene_id() + ' (' + db_mutation.get_mutation_string_short() + ')',
         db_mutation.get_type(),
         db_mutation.get_mutation_position(),
         db_mutation.get_mutation_string(),
         hit.get_pid(),
         hit.get_plength(),
         str(hit.get_hsp_length()) + '/' + str(hit.get_amr_gene_length()),
         hit.get_genome_contig_id(),
         hit.get_genome_contig_start(),
         hit.get_genome_contig_end()]

    def _get_result_rows(self, hit, database_name):
        database_mutations = hit.get_mutations()
        gene = hit.get_amr_gene_name()
        for x in database_mutations:
            logger.debug('database_mutations: position=%s, mutation=%s', x.get_mutation_position(), x.get_mutation_string())
        else:
            if database_name == '16S_rrsD' or database_name == '23S':
                database_resistance_mutations = self._blast_database.get_resistance_nucleotides(gene, database_mutations)
            else:
                database_resistance_mutations = self._blast_database.get_resistance_codons(gene, database_mutations)
            logger.debug('database_resistance_mutations=%s', database_resistance_mutations)
            if len(database_resistance_mutations) == 0:
                logger.debug('No mutations for id=[%s], file=[%s]', hit.get_amr_gene_id(), hit.get_file())
            else:
                results = []
            for db_mutation in database_resistance_mutations:
                logger.debug('multiple resistance mutations for [%s]: mutations=[%s], file=[%s]', hit.get_amr_gene_id(), database_resistance_mutations, hit.get_file())
                results.append(self._get_result(hit, db_mutation))
            else:
                return results

    def _get_out_file_name(self, in_file):
        if self._output_dir:
            return path.join(self._output_dir, 'pointfinder_' + path.basename(in_file))
        raise Exception('output_dir is None')