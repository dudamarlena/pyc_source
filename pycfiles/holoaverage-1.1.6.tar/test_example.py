# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/niermann/PycharmProjects/holoaverage/tests/test_example.py
# Compiled at: 2020-01-06 09:57:42
import unittest, os, tempfile, h5py, numpy as np, warnings
warnings.filterwarnings('error', category=DeprecationWarning)
warnings.filterwarnings('error', category=PendingDeprecationWarning)
from holoaverage.main import holoaverage, rescale_fourier
EXAMPLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../example/GaN_holographic_focal_series'))
EXAMPLE_MTF = [
 [
  'CONSTANT', -0.0225536738],
 [
  'LORENTZIAN', 1.02543658e-05, 0.000115367655],
 [
  'LORENTZIAN', 0.0249224357, 0.0535262063],
 [
  'GAUSSIAN', 0.460461599, 436.84256]]

class TestExamples(unittest.TestCase):
    """Test whether the examples run."""
    GAN_DATA_CONVERGENCE_256 = 58546370.75
    GAN_DATA_CONVERGENCE_256_FOCUS = 54679070.0
    GAN_EMPTY_CONVERGENCE_384 = 32088254000.0
    VERBOSE = 0
    DELETE_OUTPUT = True

    def setUp(self):
        self.temp_outputs = []

    def tearDown(self):
        if self.DELETE_OUTPUT:
            while len(self.temp_outputs) > 0:
                filename = self.temp_outputs.pop()
                os.unlink(filename)

    def touch_temp_output(self, suffix='.hdf5'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as (tmpfile):
            filename = tmpfile.name
        self.temp_outputs.append(filename)
        return filename

    def default_GaN_param(self):
        param = {'object_names': os.path.join(EXAMPLE_PATH, 'a1_%03d.dm3'), 
           'object_first': 1, 
           'object_last': 20, 
           'object_size': 384, 
           'empty_names': os.path.join(EXAMPLE_PATH, 'empty_%03d.dm3'), 
           'empty_first': 1, 
           'empty_last': 20, 
           'empty_size': 512, 
           'sampling': 0.00519824, 
           'defocus_first': 20.0, 
           'defocus_step': -2.0, 
           'sideband_pos': [
                          1136, 1304], 
           'roi': [
                 128, 128, 1920, 1920], 
           'output_name': self.touch_temp_output(), 
           'filter_func': [
                         'BUTTERWORTH', 14], 
           'cut_off': 12.0, 
           'mtf': EXAMPLE_MTF}
        return param

    def test_GaN_example(self):
        param = self.default_GaN_param()
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
            empty_convergence = output['empty'].attrs['convergence']
        self.assertTrue(np.allclose(empty_convergence[(-1)], self.GAN_EMPTY_CONVERGENCE_384, rtol=0.0001))
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        self.assertTrue(np.allclose(data_convergence[(-1)], self.GAN_DATA_CONVERGENCE_256, rtol=0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_example_other_sizes(self):
        param = self.default_GaN_param()
        param['object_size'] = 384
        param['empty_size'] = 512
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
            empty_convergence = output['empty'].attrs['convergence']
        self.assertTrue(np.allclose(empty_convergence[(-1)], self.GAN_EMPTY_CONVERGENCE_384, rtol=0.1))
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        self.assertTrue(np.allclose(data_convergence[(-1)], self.GAN_DATA_CONVERGENCE_256, rtol=0.1))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_example_disabled_pyfftw(self):
        from holoaverage.fft import pyfftw_present, disable_pyfftw
        if not pyfftw_present():
            return
        disable_pyfftw()
        param = self.default_GaN_param()
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
            empty_convergence = output['empty'].attrs['convergence']
        self.assertTrue(np.allclose(empty_convergence[(-1)], self.GAN_EMPTY_CONVERGENCE_384, rtol=0.0001))
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        self.assertTrue(np.allclose(data_convergence[(-1)], self.GAN_DATA_CONVERGENCE_256, rtol=0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_focus_and_tilt_alignment(self):
        param = self.default_GaN_param()
        param['adjust_defocus'] = True
        param['adjust_tilt'] = True
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
            empty_convergence = output['empty'].attrs['convergence']
        self.assertTrue(np.allclose(empty_convergence[(-1)], self.GAN_EMPTY_CONVERGENCE_384, rtol=0.1))
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        self.assertTrue(np.allclose(data_convergence[(-1)], self.GAN_DATA_CONVERGENCE_256_FOCUS, rtol=0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_no_mtf(self):
        param = self.default_GaN_param()
        param['object_last'] = 5
        param['empty_last'] = 5
        del param['mtf']
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
            empty_convergence = output['empty'].attrs['convergence']
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_no_objects(self):
        param = self.default_GaN_param()
        del param['object_names']
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            self.assertFalse('data' in output)
            self.assertFalse('variance' in output)
            empty_convergence = output['empty'].attrs['convergence']
        self.assertTrue(np.allclose(empty_convergence[(-1)], self.GAN_EMPTY_CONVERGENCE_384, rtol=0.0001))
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_no_empty(self):
        param = self.default_GaN_param()
        del param['empty_names']
        del param['empty_size']
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            self.assertFalse('empty' in output)
            data_convergence = output['data'].attrs['convergence']
        self.assertTrue(np.allclose(data_convergence[(-1)], 48852072300000.0, rtol=0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_empty_from_raw(self):
        param = self.default_GaN_param()
        empty_raw = self.touch_temp_output(suffix='.dat')
        with open(empty_raw, 'wb') as (file):
            np.zeros(100000, dtype=np.uint8).tofile(file)
            np.ones(65536, dtype=np.complex64).tofile(file)
        del param['empty_names']
        del param['empty_size']
        param['empty_override'] = '%s?type=raw&xsize=256&ysize=256&dtype=complex64&offset=100000' % empty_raw
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            self.assertFalse('empty' in output)
            data_convergence = output['data'].attrs['convergence']
        self.assertTrue(np.allclose(data_convergence[(-1)], 247313565000000.0, rtol=0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_separate_empty_and_object(self):
        empty_param = self.default_GaN_param()
        del empty_param['object_names']
        holoaverage(empty_param, verbose=self.VERBOSE)
        with h5py.File(empty_param['output_name'], 'r') as (output):
            empty_convergence = output['empty'].attrs['convergence']
        self.assertTrue(np.allclose(empty_convergence[(-1)], self.GAN_EMPTY_CONVERGENCE_384, rtol=0.0001))
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        object_param = self.default_GaN_param()
        object_param['empty_names'] = '/dev/null/some_invalid_filename'
        object_param['empty_override'] = empty_param['output_name'] + '?dataset=empty'
        holoaverage(object_param, verbose=self.VERBOSE)
        with h5py.File(object_param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
        self.assertTrue(np.allclose(data_convergence[(-1)], self.GAN_DATA_CONVERGENCE_256, rtol=0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_single_empty_and_object(self):
        param = self.default_GaN_param()
        param['object_last'] = 1
        param['empty_last'] = 1
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data = output['data'][...]
            empty = output['empty'][...]
        self.assertEqual(data.shape, (param['object_size'],) * 2)
        self.assertEqual(empty.shape, (param['empty_size'],) * 2)

    def test_GaN_single_empty_and_object_without_indexing(self):
        param = self.default_GaN_param()
        param['object_last'] = 1
        param['object_names'] = param['object_names'] % 1
        param['empty_last'] = 1
        param['empty_names'] = param['empty_names'] % 1
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data = output['data'][...]
            empty = output['empty'][...]
        self.assertEqual(data.shape, (param['object_size'],) * 2)
        self.assertEqual(empty.shape, (param['empty_size'],) * 2)

    def test_GaN_full_size(self):
        param = self.default_GaN_param()
        param['object_last'] = 1
        param['empty_last'] = 1
        param['object_size'] = 2048
        param['empty_size'] = 2048
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data = output['data'][...]
            empty = output['empty'][...]
        self.assertEqual(data.shape, (param['object_size'],) * 2)
        self.assertEqual(empty.shape, (param['empty_size'],) * 2)

    def test_GaN_synthetic_empty(self):
        empty_param = self.default_GaN_param()
        del empty_param['object_names']
        carrier = (np.array(empty_param['sideband_pos'], dtype=float) - 1024) / 2048
        carrier /= np.dot(carrier, carrier)
        holoaverage(empty_param, verbose=self.VERBOSE)
        with h5py.File(empty_param['output_name'], 'r') as (output):
            empty = output['empty'][...]
        shift = np.angle(rescale_fourier(empty, (2048, 2048))) / 2.0 / np.pi
        displacement_file = self.touch_temp_output()
        with h5py.File(displacement_file, 'w') as (output):
            output.create_dataset('dx', data=shift * carrier[0])
            output.create_dataset('dy', data=shift * carrier[1])
        object_param = self.default_GaN_param()
        object_param['empty_names'] = '/dev/null/some_invalid_filename'
        object_param['empty_override'] = '/dev/null/some_invalid_filename'
        object_param['synthesize_empty'] = True
        object_param['camera_distortions'] = [displacement_file + '?dataset=dx', displacement_file + '?dataset=dy']
        holoaverage(object_param, verbose=self.VERBOSE)
        with h5py.File(object_param['output_name'], 'r') as (output):
            new_empty = output['empty'][...]
            data_convergence = output['data'].attrs['convergence']
        np.testing.assert_allclose(np.angle(empty / new_empty)[10:-10, 10:-10], 0.0, atol=0.1)
        self.assertTrue(np.allclose(data_convergence[(-1)], 225341306000.0, rtol=0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_non_square_roi(self):
        param = self.default_GaN_param()
        param['object_last'] = 5
        param['empty_last'] = 5
        param['roi'] = [256, 640, 1792, 1408]
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
            empty_convergence = output['empty'].attrs['convergence']
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))

    def test_GaN_filename_list(self):
        param = self.default_GaN_param()
        object_names = param['object_names']
        empty_names = param['empty_names']
        param['object_names'] = [ object_names % n for n in range(1, 12, 2) ]
        param['empty_names'] = [ empty_names % n for n in range(1, 12, 2) ]
        holoaverage(param, verbose=self.VERBOSE)
        with h5py.File(param['output_name'], 'r') as (output):
            data_convergence = output['data'].attrs['convergence']
            empty_convergence = output['empty'].attrs['convergence']
        delta = (empty_convergence[1:] - empty_convergence[:-1]) / empty_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))
        delta = (data_convergence[1:] - data_convergence[:-1]) / data_convergence[:-1]
        self.assertTrue(np.all(delta < +0.0001))


if __name__ == '__main__':
    unittest.main()