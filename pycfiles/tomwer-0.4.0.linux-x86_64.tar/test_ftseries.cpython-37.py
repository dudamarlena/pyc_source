# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/test/test_ftseries.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 7849 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/04/2019'
import shutil, tempfile, unittest
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.utils import getParametersFromParOrInfo
from reconstruction.ftseries import Ftseries
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.process.reconstruction.ftseries.params import ReconsParams
from tomwer.test.utils import UtilsTest
import os

class TestFtseriesIO(unittest.TestCase):
    __doc__ = 'Test inputs and outputs types of the handler functions'

    def setUp(self) -> None:
        self.scan_folder = tempfile.mkdtemp()
        self.scan = MockEDF.mockScan(scanID=(self.scan_folder), nRadio=10,
          nRecons=1,
          nPagRecons=4,
          dim=10)
        self.recons_params = ReconsParams()
        self.ftseries_process = Ftseries(self.recons_params)
        self.ftseries_process.setMockMode(True)

    def tearDown(self) -> None:
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self) -> None:
        """Test that io using TomoBase instance work"""
        for input_type in (dict, TomoBase):
            for _input in Ftseries.inputs:
                for return_dict in (True, False):
                    with self.subTest(handler=(_input.handler), return_dict=return_dict,
                      input_type=input_type):
                        input_obj = self.scan
                        if input_obj is dict:
                            input_obj = input_obj.to_dict()
                        else:
                            self.ftseries_process._set_return_dict(return_dict)
                            out = getattr(self.ftseries_process, _input.handler)(input_obj)
                            if return_dict:
                                self.assertTrue(isinstance(out, dict))
                            else:
                                self.assertTrue(isinstance(out, TomoBase))


class TestFtseriesAxis(unittest.TestCase):
    __doc__ = 'Test the behavior of ftseries depending on the axis parameter'

    def setUp(self) -> None:
        self.outputDir = tempfile.mkdtemp()
        self.dataSetID = 'scan_3_'
        self.dataDir = UtilsTest.getDataset(self.dataSetID)
        self.datasetDir = os.path.join(self.outputDir, self.dataSetID)
        shutil.copytree(src=(os.path.join(self.dataDir)), dst=(self.datasetDir))
        self.recons_params = ReconsParams()
        self.ftseries = Ftseries(recons_params=(self.recons_params))
        self.parFile = os.path.join(self.datasetDir, self.dataSetID + '.par')
        if os.path.exists(self.parFile):
            os.remove(self.parFile)
        self.scan = EDFTomoScan(self.datasetDir)
        self.axis_frm_tomwer_file = os.path.join(self.datasetDir, 'correct.txt')

    def tearDown(self) -> None:
        shutil.rmtree(self.outputDir)

    def testAxisCorrectionOption(self) -> None:
        """Test that the pyhst parameter 'DO_AXIS_CORRECTION' is correctly set
        """
        self.recons_params.axis.do_axis_correction = False
        self.ftseries.process(self.scan)
        self.assertTrue(os.path.exists(self.parFile))
        par_info = getParametersFromParOrInfo(self.parFile)
        self.assertTrue('DO_AXIS_CORRECTION'.lower() in par_info)
        self.assertTrue(par_info['DO_AXIS_CORRECTION'.lower()] in ('NO', '0'))
        self.recons_params.axis.do_axis_correction = True
        self.ftseries.process(self.scan)
        self.assertTrue(os.path.exists(self.parFile))
        par_info = getParametersFromParOrInfo(self.parFile)
        self.assertTrue('DO_AXIS_CORRECTION'.lower() in par_info)
        self.assertTrue(par_info['DO_AXIS_CORRECTION'.lower()] in ('YES', '1'))
        self.assertFalse(os.path.exists(self.axis_frm_tomwer_file))
        self.assertEqual(par_info['AXIS_CORRECTION_FILE'.lower()], '')

    def testLinkWithAxis(self) -> None:
        """Test ftseries process behavior with AxisProcess"""
        from tomwer.core.process.reconstruction.axis import AxisRP, AxisProcess
        axis_params = AxisRP()
        axis_params.mode = 'manual'
        axis_params.value = 2.5
        axis_process = AxisProcess(axis_params=axis_params)
        self.recons_params.axis.do_axis_correction = True
        self.recons_params.axis.use_tomwer_axis = True
        self.recons_params.axis.use_old_tomwer_axis = False
        self.ftseries.process(scan=(self.scan))
        self.assertFalse(os.path.exists(self.axis_frm_tomwer_file))
        par_info = getParametersFromParOrInfo(self.parFile)
        self.assertTrue('AXIS_CORRECTION_FILE'.lower() in par_info)
        self.assertEqual(par_info['AXIS_CORRECTION_FILE'.lower()], '')
        axis_process.process(scan=(self.scan))
        self.ftseries.process(scan=(self.scan))
        self.assertTrue(os.path.exists(self.axis_frm_tomwer_file))
        par_info = getParametersFromParOrInfo(self.parFile)
        self.assertEqual(par_info['AXIS_CORRECTION_FILE'.lower()], self.axis_frm_tomwer_file)
        with open(file=(self.axis_frm_tomwer_file), mode='r') as (f_):
            l = f_.readline()
            self.assertEqual(l, '2.5')
        scan2 = EDFTomoScan(scan=(self.datasetDir))
        os.remove(self.parFile)
        self.ftseries.process(scan=scan2)
        self.assertTrue(os.path.exists(self.parFile))
        self.recons_params.axis.use_old_tomwer_axis = True
        self.ftseries.process(scan=scan2)
        self.assertTrue(os.path.exists(self.parFile))
        self.assertTrue(os.path.exists(self.axis_frm_tomwer_file))
        with open(file=(self.axis_frm_tomwer_file), mode='r') as (f_):
            l = f_.readline()
            self.assertEqual(l, '2.5')
        axis_params.value = -1.3
        axis_process.process(scan=scan2)
        self.ftseries.process(scan=scan2)
        with open(file=(self.axis_frm_tomwer_file), mode='r') as (f_):
            l = f_.readline()
            self.assertEqual(l, '-1.3')


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestFtseriesIO,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite