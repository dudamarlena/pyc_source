# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/blast/results/plasmidfinder/BlastResultsParserPlasmidfinderResistance.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 2439 bytes
from typing import Dict
from typing import List
import staramr.blast.plasmidfinder.PlasmidfinderBlastDatabase as PlasmidfinderBlastDatabase
import staramr.blast.results.BlastResultsParser as BlastResultsParser
import staramr.blast.results.plasmidfinder.BlastResultsParserPlasmidfinder as BlastResultsParserPlasmidfinder
import staramr.blast.results.plasmidfinder.PlasmidfinderHitHSP as PlasmidfinderHitHSP

class BlastResultsParserPlasmidfinderResistance(BlastResultsParserPlasmidfinder):
    COLUMNS = [x.strip() for x in '\n    Isolate ID\n    Gene\n    %Identity\n    %Overlap\n    HSP Length/Total Length\n    Contig\n    Start\n    End\n    Accession\n    '.strip().split('\n')]

    def __init__(self, file_blast_map, blast_database, pid_threshold, plength_threshold, report_all=False, output_dir=None, genes_to_exclude=[]):
        """
        Creates a new BlastResultsParserPlasmidfinderResistance.
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

    def _get_result_rows(self, hit: PlasmidfinderHitHSP, database_name: str) -> list:
        return [
         [hit.get_genome_id(),
          hit.get_amr_gene_name(),
          hit.get_pid(),
          hit.get_plength(),
          str(hit.get_hsp_length()) + '/' + str(hit.get_amr_gene_length()),
          hit.get_genome_contig_id(),
          hit.get_genome_contig_start(),
          hit.get_genome_contig_end(),
          hit.get_amr_gene_accession()]]