# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/tests/integration/detection/test_AMRDetectionMLST.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 4297 bytes
import logging, tempfile, unittest
from os import path
from Bio import SeqIO
import staramr.blast.JobHandler as JobHandler
import staramr.blast.plasmidfinder.PlasmidfinderBlastDatabase as PlasmidfinderBlastDatabase
import staramr.blast.resfinder.ResfinderBlastDatabase as ResfinderBlastDatabase
import staramr.databases.AMRDatabasesManager as AMRDatabasesManager
import staramr.databases.resistance.resfinder.ARGDrugTableResfinder as ARGDrugTableResfinder
import staramr.databases.resistance.pointfinder.ARGDrugTablePointfinder as ARGDrugTablePointfinder
import staramr.detection.AMRDetectionResistance as AMRDetectionResistance
logger = logging.getLogger('AMRDetectionMLST')

class AMRDetectionMLST(unittest.TestCase):

    def setUp(self):
        blast_databases_repositories = AMRDatabasesManager.create_default_manager().get_database_repos()
        self.resfinder_dir = blast_databases_repositories.get_repo_dir('resfinder')
        self.pointfinder_dir = blast_databases_repositories.get_repo_dir('pointfinder')
        self.plasmidfinder_dir = blast_databases_repositories.get_repo_dir('plasmidfinder')
        self.resfinder_database = ResfinderBlastDatabase(self.resfinder_dir)
        self.resfinder_drug_table = ARGDrugTableResfinder()
        self.pointfinder_drug_table = ARGDrugTablePointfinder()
        self.plasmidfinder_database = PlasmidfinderBlastDatabase(self.plasmidfinder_dir)
        self.pointfinder_database = None
        self.blast_out = tempfile.TemporaryDirectory()
        self.blast_handler = JobHandler({'resfinder':self.resfinder_database, 
         'pointfinder':self.pointfinder_database,  'plasmidfinder':self.plasmidfinder_database}, 2, self.blast_out.name)
        self.outdir = tempfile.TemporaryDirectory()
        self.amr_detection = AMRDetectionResistance((self.resfinder_database), (self.resfinder_drug_table), (self.blast_handler),
          (self.pointfinder_drug_table), (self.pointfinder_database),
          output_dir=(self.outdir.name))
        self.test_data_dir = path.join(path.dirname(__file__), '..', 'data')

    def tearDown(self):
        self.blast_out.cleanup()
        self.outdir.cleanup()

    def testMLSTResults(self):
        file = path.join(self.test_data_dir, 'test-mlst-summary.fsa')
        files = [file]
        self.amr_detection.run_amr_detection(files, 99, 90, 90, 90, 0, 0, 0, 0, 0)
        mlst_results = self.amr_detection.get_mlst_results()
        self.assertEqual(len(mlst_results.index), 1, 'Wrong number of results detected')
        self.assertEqual(len(mlst_results.columns), 9, 'Wrong number of columns detected')
        self.assertEqual((mlst_results['Scheme'].iloc[0]), 'senterica', msg='Wrong Scheme')
        self.assertEqual((mlst_results['Sequence Type'].iloc[0]), '1', msg='Wrong Sequence Type')
        self.assertEqual((mlst_results['Locus 1'].iloc[0]), 'aroC(1)', msg='Wrong Locus 1 Result')
        self.assertEqual((mlst_results['Locus 2'].iloc[0]), 'dnaN(1)', msg='Wrong Locus 2 Result')
        self.assertEqual((mlst_results['Locus 3'].iloc[0]), 'hemD(1)', msg='Wrong Locus 3 Result')
        self.assertEqual((mlst_results['Locus 4'].iloc[0]), 'hisD(1)', msg='Wrong Locus 4 Result')
        self.assertEqual((mlst_results['Locus 5'].iloc[0]), 'purE(1)', msg='Wrong Locus 5 Result')
        self.assertEqual((mlst_results['Locus 6'].iloc[0]), 'sucA(1)', msg='Wrong Locus 6 Result')
        self.assertEqual((mlst_results['Locus 7'].iloc[0]), 'thrA(5)', msg='Wrong Locus 7 Result')

    def testNoMLSTResults(self):
        file = path.join(self.test_data_dir, 'gyrA-S97N.fsa')
        files = [file]
        self.amr_detection.run_amr_detection(files, 99, 90, 90, 90, 0, 0, 0, 0, 0)
        mlst_results = self.amr_detection.get_mlst_results()
        self.assertEqual(len(mlst_results.index), 1, 'Wrong number of results detected')
        self.assertEqual(len(mlst_results.columns), 2, 'Wrong number of columns detected')
        self.assertEqual((mlst_results['Scheme'].iloc[0]), '-', msg='Scheme is found, expected none')
        self.assertEqual((mlst_results['Sequence Type'].iloc[0]), '-', msg='Sequence Type is found, expected none')