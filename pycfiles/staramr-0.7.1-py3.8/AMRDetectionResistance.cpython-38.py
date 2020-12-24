# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/detection/AMRDetectionResistance.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 5948 bytes
from typing import List, Optional
from pandas import DataFrame
import staramr.blast.results.plasmidfinder.BlastResultsParserPlasmidfinderResistance as BlastResultsParserPlasmidfinderResistance
import staramr.blast.results.pointfinder.BlastResultsParserPointfinder as BlastResultsParserPointfinder
import staramr.blast.results.pointfinder.BlastResultsParserPointfinderResistance as BlastResultsParserPointfinderResistance
import staramr.blast.results.resfinder.BlastResultsParserResfinderResistance as BlastResultsParserResfinderResistance
import staramr.detection.AMRDetection as AMRDetection
import staramr.results.AMRDetectionSummaryResistance as AMRDetectionSummaryResistance

class AMRDetectionResistance(AMRDetection):

    def __init__(self, resfinder_database, arg_drug_table_resfinder, amr_detection_handler, arg_drug_table_pointfinder, pointfinder_database=None, include_negative_results=False, output_dir=None, genes_to_exclude=[], plasmidfinder_database=None):
        """
        Builds a new AMRDetectionResistance.
        :param resfinder_database: The staramr.blast.resfinder.ResfinderBlastDatabase for the particular ResFinder database.
        :param arg_drug_table_resfinder: The staramr.databases.resistance.ARGDrugTable for searching for resfinder resistances.
        :param amr_detection_handler: The staramr.blast.JobHandler to use for scheduling BLAST jobs.
        :param arg_drug_table_pointfinder: The staramr.databases.resistance.ARGDrugTable for searching for pointfinder resistances.
        :param pointfinder_database: The staramr.blast.pointfinder.PointfinderBlastDatabase to use for the particular PointFinder database.
        :param include_negative_results:  If True, include files lacking AMR genes in the resulting summary table.
        :param output_dir: The directory where output fasta files are to be written into (None for no output fasta files).
        :param genes_to_exclude: A list of gene IDs to exclude from the results.
        """
        super().__init__(resfinder_database, amr_detection_handler, pointfinder_database, include_negative_results, output_dir=output_dir,
          genes_to_exclude=genes_to_exclude,
          plasmidfinder_database=plasmidfinder_database)
        self._arg_drug_table_resfinder = arg_drug_table_resfinder
        self._arg_drug_table_pointfinder = arg_drug_table_pointfinder

    def _create_resfinder_dataframe(self, resfinder_blast_map, pid_threshold, plength_threshold, report_all):
        resfinder_parser = BlastResultsParserResfinderResistance(resfinder_blast_map, (self._arg_drug_table_resfinder), (self._resfinder_database),
          pid_threshold, plength_threshold,
          report_all, output_dir=(self._output_dir),
          genes_to_exclude=(self._genes_to_exclude))
        return resfinder_parser.parse_results()

    def _create_pointfinder_dataframe(self, pointfinder_blast_map, pid_threshold, plength_threshold, report_all):
        pointfinder_parser = BlastResultsParserPointfinderResistance(pointfinder_blast_map, (self._arg_drug_table_pointfinder),
          (self._pointfinder_database),
          pid_threshold,
          plength_threshold, report_all, output_dir=(self._output_dir),
          genes_to_exclude=(self._genes_to_exclude))
        return pointfinder_parser.parse_results()

    def _create_plasmidfinder_dataframe(self, plasmidfinder_blast_map, pid_threshold, plength_threshold, report_all):
        plasmidfinder_parser = BlastResultsParserPlasmidfinderResistance(plasmidfinder_blast_map, (self._plasmidfinder_database),
          pid_threshold,
          plength_threshold,
          report_all, output_dir=(self._output_dir),
          genes_to_exclude=(self._genes_to_exclude))
        return plasmidfinder_parser.parse_results()

    def _create_amr_summary(self, files, resfinder_dataframe, quality_module_dataframe, pointfinder_dataframe, plasmidfinder_dataframe, mlst_dataframe):
        amr_detection_summary = AMRDetectionSummaryResistance(files, resfinder_dataframe, quality_module_dataframe, pointfinder_dataframe, plasmidfinder_dataframe, mlst_dataframe)
        return amr_detection_summary.create_summary(self._include_negative_results)

    def _create_detailed_amr_summary(self, files: List[str], resfinder_dataframe: DataFrame, quality_module_dataframe: DataFrame, pointfinder_dataframe: Optional[BlastResultsParserPointfinder], plasmidfinder_dataframe: DataFrame, mlst_dataframe) -> DataFrame:
        amr_detection_summary = AMRDetectionSummaryResistance(files, resfinder_dataframe, quality_module_dataframe, pointfinder_dataframe, plasmidfinder_dataframe, mlst_dataframe)
        return amr_detection_summary.create_detailed_summary(self._include_negative_results)