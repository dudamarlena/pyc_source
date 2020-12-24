# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/test/test_scanstages.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 7119 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '30/09/2019'
import unittest, tempfile, os, shutil, glob
from collections import namedtuple
from tomwer.test.utils import UtilsTest
from tomwer.synctools.utils.scanstages import ScanStages
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.test.utils import skip_gui_test
if skip_gui_test() is False:
    from tomwer.synctools.rsyncmanager import RSyncManager
_stage_desc = namedtuple('_stage_desc', [
 'n_par_file', 'n_edf_file', 'n_info_file',
 'n_xml_file', 'n_vol', 'folder_should_exists'])

@unittest.skipIf(RSyncManager().canUseRSync() is False, 'Rsync is missing')
@unittest.skipIf((skip_gui_test()), reason='skip gui test')
class TestScanStagesEDF(unittest.TestCase):
    __doc__ = '\n    test the ScanStages class for edf scans\n    '

    def setUp(self) -> None:
        self.output_dir = tempfile.mkdtemp()
        dataset = 'D2_H2_T2_h_'
        self.data_test_dir = UtilsTest.getDataset(dataset)
        self.target_dir = os.path.join(self.output_dir, dataset)
        self.scan_stages = ScanStages(scan=(ScanFactory.create_scan_object(self.data_test_dir)))

    def tearDown(self) -> None:
        shutil.rmtree(self.output_dir)

    def testRSyncUntil(self):
        """test the rsync_until function"""
        tomo_n = 3605
        stage_res = {ScanStages.AcquisitionStage.ACQUI_NOT_STARTED: _stage_desc(n_par_file=0, n_edf_file=0,
                                                          n_info_file=0,
                                                          n_xml_file=0,
                                                          n_vol=0,
                                                          folder_should_exists=False), 
         
         ScanStages.AcquisitionStage.ACQUI_STARTED: _stage_desc(n_par_file=0, n_edf_file=0,
                                                      n_info_file=1,
                                                      n_xml_file=0,
                                                      n_vol=0,
                                                      folder_should_exists=True), 
         
         ScanStages.AcquisitionStage.ACQUI_ON_GOING: _stage_desc(n_par_file=0, n_edf_file=(tomo_n // 2),
                                                       n_info_file=1,
                                                       n_xml_file=0,
                                                       n_vol=0,
                                                       folder_should_exists=True), 
         
         ScanStages.AcquisitionStage.ACQUI_ENDED: _stage_desc(n_par_file=0, n_edf_file=tomo_n,
                                                    n_info_file=1,
                                                    n_xml_file=1,
                                                    n_vol=0,
                                                    folder_should_exists=True), 
         
         ScanStages.AcquisitionStage.RECONSTRUCTION_ADDED: _stage_desc(n_par_file=6, n_edf_file=tomo_n,
                                                             n_info_file=2,
                                                             n_xml_file=2,
                                                             n_vol=1,
                                                             folder_should_exists=True), 
         
         ScanStages.AcquisitionStage.COMPLETE: _stage_desc(n_par_file=6, n_edf_file=3719,
                                                 n_info_file=2,
                                                 n_xml_file=2,
                                                 n_vol=1,
                                                 folder_should_exists=True)}
        for stage, th_results in stage_res.items():
            with self.subTest(stage=stage):
                self.scan_stages.rsync_until(stage=stage, dest_dir=(self.output_dir))
                self.assertEqual(os.path.exists(self.target_dir), th_results.folder_should_exists)
                self.assertEqual(len(glob.glob(os.path.join(self.target_dir, '*.par'))), th_results.n_par_file)
                self.assertEqual(len(glob.glob(os.path.join(self.target_dir, '*.edf'))), th_results.n_edf_file)
                self.assertEqual(len(glob.glob(os.path.join(self.target_dir, '*.xml'))), th_results.n_xml_file)
                self.assertEqual(len(glob.glob(os.path.join(self.target_dir, '*.vol'))), th_results.n_vol)
                self.assertEqual(len(glob.glob(os.path.join(self.target_dir, '*.info'))), th_results.n_info_file)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScanStagesEDF,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')