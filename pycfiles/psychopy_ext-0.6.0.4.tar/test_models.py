# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/tests/test_models.py
# Compiled at: 2016-03-14 08:48:00
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest, numpy as np, skimage
from psychopy_ext import models, utils

class TestOutput(unittest.TestCase):

    def read_orig(self, m, flatten=False, suffix=b''):
        pic = b'cat-gray' if flatten else b'cat'
        path = (b'psychopy_ext/tests/{}_{}{}.txt').format(pic, m.safename, suffix)
        resps_orig = np.loadtxt(path, delimiter=b',').ravel()
        return resps_orig

    def run_model(self, name, im=None, flatten=False, size=None, layers=b'output', suffix=b''):
        if im is None:
            if flatten:
                im = b'cat-gray-32x32' if size == 32 else b'cat-gray'
            else:
                im = b'cat-32x32' if size == 32 else b'cat'
            im = b'psychopy_ext/tests/%s.png' % im
        if isinstance(name, (unicode, str)):
            m = models.Model(name)
        else:
            m = name
        resps_test = m.run(im, layers=layers, return_dict=False)
        resps_test = np.around(resps_test, decimals=5)
        resps_orig = self.read_orig(m, flatten=flatten, suffix=suffix)
        if name == b'hmax_pnas':
            rms = np.mean(np.sqrt((np.sort(resps_test) - np.sort(resps_orig)) ** 2))
        else:
            rms = np.mean(np.sqrt((resps_test - resps_orig) ** 2))
        self.assertAlmostEqual(rms, 0)
        return

    def test_px(self):
        self.run_model(b'px', flatten=False, size=32)

    def test_gaborjet_mag(self):
        stim = utils.load_image(b'psychopy_ext/tests/cat-gray.png')
        im = np.array([skimage.img_as_ubyte(stim)]).astype(float)
        self.run_model(b'gaborjet', im, flatten=True, layers=b'magnitudes', suffix=b'-mag-matlab')

    def test_gaborjet_mag(self):
        stim = utils.load_image(b'psychopy_ext/tests/cat-gray.png')
        im = np.array([skimage.img_as_ubyte(stim)]).astype(float)
        self.run_model(b'gaborjet', im, layers=b'phases', flatten=True, suffix=b'-phase-matlab')

    def test_hmax99_gabor(self):
        stim = utils.load_image(b'psychopy_ext/tests/cat-gray.png')
        im = np.array([skimage.img_as_ubyte(stim)]).astype(float)
        m = models.HMAX99(matlab=True, filter_type=b'gabor')
        self.run_model(m, im, flatten=True, suffix=b'-gabor-matlab')

    def test_hog(self):
        self.run_model(b'hog', flatten=True, size=32)

    def test_caffenet(self):
        self.run_model(b'caffenet', flatten=False, size=None)
        return

    def test_hmax_hmin(self):
        self.run_model(b'hmax_hmin', flatten=True, size=None)
        return

    def test_hmax_pnas(self):
        self.run_model(b'hmax_pnas', flatten=False, size=None)
        return

    def test_phog(self):
        self.run_model(b'phog', flatten=False, size=None)
        return

    def test_phow(self):
        self.run_model(b'phow', flatten=False, size=None)
        return

    def test_randfilt(self):
        self.run_model(b'randfilt', flatten=True, size=None)
        return


if __name__ == b'__main__':
    unittest.main()