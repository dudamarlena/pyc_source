# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/test/test_tomo_workflow.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 9928 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
import os, shutil, tempfile, unittest
from tomwer.core.process.reconstruction.axis import AxisProcess
from tomwer.core.process.reconstruction.axis.params import AxisRP
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.core.process.reconstruction.ftseries import Ftseries
from tomwer.core.process.reconstruction.ftseries.params import ReconsParams
from tomwer.core.process.reconstruction.darkref.params import DKRFRP, Method
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.scanutils import MockEDF

class TestTomoReconsWorkflow(unittest.TestCase):
    __doc__ = 'Test several tomography reconstruction workflow and make sure they\n    are correctly processed. Focus on ReconsParams values'

    def setUp(self):
        self._axis_rp = AxisRP()
        self._axis_process = AxisProcess(axis_params=(self._axis_rp))
        self._axis_rp_id = id(self._axis_rp)
        self._darkref_process = DarkRefs()
        self._darkref_process.setForceSync(True)
        self._darkref_rp = DKRFRP()
        self._darkref_rp_id = id(self._darkref_rp)
        self._ftseries_process = Ftseries()
        self._ftseries_process.setForceSync(True)
        self._ftseries_process.setMockMode(True)
        self._ftseries_rp = ReconsParams()
        self._ftseries_rp_id = id(self._ftseries_rp)
        self._check_default_values()
        self._axis_rp.mode = AxisMode.near
        self._darkref_rp.dark_calc_method = Method.median
        self._ftseries_rp.dkrf.dark_calc_method = Method.median
        self._axis_process.set_recons_params(self._axis_rp)
        self._darkref_process.set_recons_params(self._darkref_rp)
        self._ftseries_process.set_recons_params(self._ftseries_rp)
        assert id(self._ftseries_rp) == self._ftseries_rp_id
        assert id(self._ftseries_process.recons_params) == self._ftseries_rp_id
        self._scans_dir = tempfile.mkdtemp()

        def create_scan(dataset):
            _folder = os.path.join(self._scans_dir, dataset)
            os.mkdir(_folder)
            MockEDF.fastMockAcquisition(_folder, n_radio=10)
            return EDFTomoScan(scan=_folder)

        self.scan_a = create_scan('scanA')
        self.scan_b = create_scan('scanB')
        self.scan_01_dft_rp = ReconsParams()
        self.scan_10_dft_rp = ReconsParams()
        self._recons_params_dft = {self.scan_a.path: self.scan_01_dft_rp, 
         self.scan_b.path: self.scan_10_dft_rp}
        self.scans = (
         self.scan_a, self.scan_b)

    def tearDown(self):
        shutil.rmtree(self._scans_dir)

    def _check_default_values(self):
        assert self._darkref_rp.dark_calc_method is Method.average
        assert self._ftseries_rp.dkrf.dark_calc_method is Method.average
        assert id(self._darkref_rp) != id(self._ftseries_rp)

    def _process_axis(self, scan, initial_recons_params):
        """execute the axis process and check results"""
        self._axis_process.process(scan=scan)
        if initial_recons_params is not None:
            self.assertTrue(id(scan.ftseries_recons_params) is id(self._recons_params_dft[scan]))
        self.assertTrue(scan.axis_params.mode is AxisMode.near)

    def _process_darkref(self, scan, initial_recons_params):
        """execute the darkref process and check results"""
        self._darkref_process.process(scan=scan)
        if initial_recons_params is not None:
            self.assertTrue(id(scan.ftseries_recons_params) is id(self._recons_params_dft[scan]))
        if initial_recons_params is None:
            self.assertTrue(scan.ftseries_recons_params.paganin is None)
        self.assertTrue(scan.ftseries_recons_params.dkrf.dark_calc_method is Method.median)

    def _process_ftseries(self, scan, initial_recons_params):
        """execute the ftseries process and check results"""
        self.assertTrue(id(self._ftseries_process.recons_params) == self._ftseries_rp_id)
        self._ftseries_process.process(scan=scan)
        if initial_recons_params is not None:
            self.assertTrue(id(scan.ftseries_recons_params) is id(self._recons_params_dft[scan]))
        if initial_recons_params is None:
            self.assertTrue(scan.ftseries_recons_params.paganin is not None)
        self.assertTrue(id(self._ftseries_process.recons_params) == self._ftseries_rp_id)
        self.assertTrue(self._ftseries_rp.dkrf.dark_calc_method == scan.ftseries_recons_params.dkrf.dark_calc_method)
        self.assertTrue(scan.ftseries_recons_params.dkrf.dark_calc_method is Method.median)

    def test_axis_darkrefs_ftseries(self):
        """Test that the workflow axis -> darkrefs -> ftseries is valid
        regarding the reconstruction parameters used"""
        for initial_recons_params in (None, ):
            with self.subTest(initial_recons_params=initial_recons_params):
                if initial_recons_params is not None:
                    for key, value in initial_recons_params.items():
                        key.ftseries_recons_params = value
                        assert id(value) is id(key.ftseries_recons_params)

                for scan in self.scans:
                    assert isinstance(scan, EDFTomoScan)
                    self._process_axis(scan=scan, initial_recons_params=initial_recons_params)
                    self._process_darkref(scan=scan, initial_recons_params=initial_recons_params)
                    self._process_ftseries(scan=scan, initial_recons_params=initial_recons_params)
                    scan.ftseries_recons_params.to_unique_recons_set()

    def test_axis_ftseries(self):
        """Test that the workflow axis -> ftseries sis valid regarding
        the reconstruction parameters used"""
        for initial_recons_params in (None, ):
            with self.subTest(initial_recons_params=initial_recons_params):
                if initial_recons_params is not None:
                    for key, value in initial_recons_params.items():
                        key.ftseries_recons_params = value
                        assert id(value) is id(key.ftseries_recons_params)

                for scan in self.scans:
                    assert isinstance(scan, EDFTomoScan)
                    self._process_axis(scan=scan, initial_recons_params=initial_recons_params)
                    self._process_ftseries(scan=scan, initial_recons_params=initial_recons_params)
                    scan.ftseries_recons_params.to_unique_recons_set()

    def test_darkrefs_ftseries(self):
        """Test that the workflow darkrefs -> ftseries sis valid regarding
        the reconstruction parameters used"""
        for initial_recons_params in (None, ):
            with self.subTest(initial_recons_params=initial_recons_params):
                if initial_recons_params is not None:
                    for key, value in initial_recons_params.items():
                        key.ftseries_recons_params = value
                        assert id(value) is id(key.ftseries_recons_params)

                for scan in self.scans:
                    assert isinstance(scan, EDFTomoScan)
                    self._process_darkref(scan=scan, initial_recons_params=initial_recons_params)
                    scan.ftseries_recons_params.to_unique_recons_set()
                    self._process_ftseries(scan=scan, initial_recons_params=initial_recons_params)
                    scan.ftseries_recons_params.to_unique_recons_set()


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestTomoReconsWorkflow,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')