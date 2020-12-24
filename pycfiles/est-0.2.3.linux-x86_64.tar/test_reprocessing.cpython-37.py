# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/app/test/test_reprocessing.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 6022 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/26/2019'
import os, shutil, tempfile, unittest, numpy
from est.core.io import XASWriter
from est.core.types import XASObject
import est.core.utils as spectra_utils
import urllib.request
from est.core.types import Spectrum
from ..reprocessing import exec_
try:
    import PyMca5
except ImportError:
    has_pymca = False
else:
    has_pymca = True
    from est.core.process.pymca.exafs import PyMca_exafs
    from est.core.process.pymca.ft import PyMca_ft
    from est.core.process.pymca.k_weight import PyMca_k_weight
    from est.core.process.pymca.normalization import PyMca_normalization
    from est.io.utils.pymca import read_spectrum
    from PyMca5.PyMcaDataDir import PYMCA_DATA_DIR
try:
    import larch
except ImportError:
    has_larch = False
else:
    has_larch = True
    from est.core.process.larch.pre_edge import Larch_pre_edge
    from est.core.process.larch.xftf import Larch_xftf
    from est.core.process.larch.autobk import Larch_autobk
    from est.io.utils.larch import read_ascii

@unittest.skipIf(has_pymca is False, 'PyMca5 is not installed')
class TestReprocessingPyMca(unittest.TestCase):
    __doc__ = 'test reprocessing work for some pymca process'

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        data_file = os.path.join(PYMCA_DATA_DIR, 'EXAFS_Cu.dat')
        energy, mu = read_spectrum(data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        self.xas_obj_ref = XASObject(spectra=(self.spectrum,), energy=energy, dim1=1,
          dim2=1)
        self.h5_file = os.path.join(self.output_dir, 'output_file.h5')
        out = PyMca_normalization()(xas_obj=(self.xas_obj_ref))
        out = PyMca_exafs()(xas_obj=out)
        out = PyMca_k_weight()(xas_obj=out)
        out = PyMca_ft()(xas_obj=out)
        out = PyMca_normalization()(xas_obj=out)
        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(out)
        assert out.spectra[0].ft.intensity is not None
        assert len(out.get_process_flow()) is 5

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test(self):
        res_xas_obj = exec_(self.h5_file)
        self.assertEqual(res_xas_obj, self.xas_obj_ref)
        numpy.testing.assert_allclose(res_xas_obj.spectra[0].ft.intensity, self.xas_obj_ref.spectra[0].ft.intensity)


@unittest.skipIf(has_larch is False, 'Larch is not installed')
class TestReprocessingLarch(unittest.TestCase):
    __doc__ = 'test reprocessing work for some larch process'

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        xmu_url = 'https://raw.githubusercontent.com/xraypy/xraylarch/master/examples/xafs/cu_rt01.xmu'
        self.data_file = os.path.join(self.output_dir, 'cu_rt01.xmu')
        with urllib.request.urlopen(xmu_url) as (response):
            with open(self.data_file, 'wb') as (out_file):
                data = response.read()
                out_file.write(data)
        assert os.path.exists(self.data_file)
        energy, mu = read_ascii(self.data_file)
        self.spectrum = Spectrum(energy=energy, mu=mu)
        spectra = (self.spectrum,)
        self.xas_obj_ref = XASObject(spectra=spectra, energy=energy, dim1=1, dim2=1)
        self.h5_file = os.path.join(self.output_dir, 'output_file.h5')
        pre_edge_process = Larch_pre_edge()
        pre_edge_process.setProperties({'rbkg':1.0,  'kweight':2})
        autobk_process = Larch_autobk()
        autobk_process.setProperties({'kmin':2,  'kmax':16,  'dk':3,  'window':'hanning', 
         'kweight':2})
        xftf_process = Larch_xftf()
        xftf_process.setProperties({'kweight': 2})
        out = pre_edge_process(xas_obj=(self.xas_obj_ref))
        out = autobk_process(xas_obj=out)
        out = xftf_process(xas_obj=out)
        writer = XASWriter()
        writer.output_file = self.h5_file
        writer(out)
        assert len(out.get_process_flow()) is 3

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test(self):
        res_xas_obj = exec_(self.h5_file)
        self.assertEqual(res_xas_obj, self.xas_obj_ref)
        numpy.testing.assert_allclose(res_xas_obj.spectra[0].chir_mag, self.xas_obj_ref.spectra[0].chir_mag)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestReprocessingPyMca, TestReprocessingLarch):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))

    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')