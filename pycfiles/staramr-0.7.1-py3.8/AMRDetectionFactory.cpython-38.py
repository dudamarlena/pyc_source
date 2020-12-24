# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/detection/AMRDetectionFactory.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 2383 bytes
import staramr.databases.resistance.pointfinder.ARGDrugTablePointfinder as ARGDrugTablePointfinder
import staramr.databases.resistance.resfinder.ARGDrugTableResfinder as ARGDrugTableResfinder
import staramr.detection.AMRDetection as AMRDetection
import staramr.detection.AMRDetectionResistance as AMRDetectionResistance

class AMRDetectionFactory:

    def __init__(self):
        pass

    def build(self, plasmidfinder_database, resfinder_database, blast_handler, pointfinder_database, include_negatives, include_resistances=False, output_dir=None, genes_to_exclude=[]):
        """
        Builds a new AMRDetection object.
        :param plasmidfinder_database: The staramr.blast.plasmidfinder.PlasmidfinderBlastDatabase to use for the particular PlasmidFinder database.
        :param resfinder_database: The staramr.blast.resfinder.ResfinderBlastDatabase for the particular ResFinder database.
        :param blast_handler: The staramr.blast.JobHandler to use for scheduling BLAST jobs.
        :param pointfinder_database: The staramr.blast.pointfinder.PointfinderBlastDatabase to use for the particular PointFinder database.
        :param include_negatives:  If True, include files lacking AMR genes in the resulting summary table.
        :param include_resistances: If True, include predicted drug resistances in output.
        :param output_dir: The directory where output files are being written.
        :param genes_to_exclude: A list of gene IDs to exclude from the results.
        :return: A new AMRDetection object.
        """
        if include_resistances:
            return AMRDetectionResistance(resfinder_database, (ARGDrugTableResfinder()), blast_handler, (ARGDrugTablePointfinder()),
              pointfinder_database, include_negatives, output_dir=output_dir,
              genes_to_exclude=genes_to_exclude,
              plasmidfinder_database=plasmidfinder_database)
        return AMRDetection(resfinder_database, blast_handler, pointfinder_database, include_negatives, output_dir=output_dir,
          genes_to_exclude=genes_to_exclude,
          plasmidfinder_database=plasmidfinder_database)