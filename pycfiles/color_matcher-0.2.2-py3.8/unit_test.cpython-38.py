# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/unit_test.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 4210 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
from color_matcher.top_level import ColorMatcher, METHODS
from color_matcher.io_handler import *
import unittest, os, numpy as np
from ddt import ddt, idata, unpack

@ddt
class MatchMethodTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        (super(MatchMethodTester, self).__init__)(*args, **kwargs)

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dat_path = os.path.join(self.dir_path, 'data')

    @staticmethod
    def avg_hist_dist(img1, img2, bins=255):
        hist_a = np.histogram(img1, bins)[0]
        hist_b = np.histogram(img2, bins)[0]
        return np.sqrt(np.sum(np.square(hist_a - hist_b)))

    @idata(([m] for m in METHODS))
    @unpack
    def test_match_method(self, method=None, save=False):
        if method is None:
            self.skipTest("Type 'None' was passed and skipped")
        plain = load_img_file(os.path.join(self.dat_path, 'scotland_plain.png'))
        house = load_img_file(os.path.join(self.dat_path, 'scotland_house.png'))
        refer = load_img_file(os.path.join(self.dat_path, 'scotland_pitie.png'))
        match = ColorMatcher(src=house, ref=plain, method=method).main()
        refer_val = self.avg_hist_dist(plain, refer)
        match_val = self.avg_hist_dist(plain, match)
        print('\nAvg. histogram distance of original %s vs. %s %s' % (round(refer_val, 3), method, round(match_val, 3)))
        self.assertEqual(True, refer_val > match_val)
        if save:
            save_img_file(match, file_path=(os.path.join(self.dat_path, 'scotland_' + method)), file_type='png')

    @idata(([kw] for kw in (['-s ', '-r '], ['--src=', '--ref='])))
    @unpack
    def test_cli(self, kw):
        from color_matcher.bin.cli import main
        import sys
        sys.argv.append(kw[0] + os.path.join(self.dat_path, 'scotland_house.png'))
        sys.argv.append(kw[1] + os.path.join(self.dat_path, 'scotland_plain.png'))
        ret = main()
        self.assertEqual(True, ret)

    @unittest.skipUnless(False, 'n.a.')
    def test_match_method_imageio(self, method=None):
        import imageio
        fn_img1 = 'chelsea'
        fn_img2 = 'coffee'
        img1 = imageio.imread('imageio:' + fn_img1 + '.png')
        img2 = imageio.imread('imageio:' + fn_img2 + '.png')
        match = ColorMatcher(img1, img2, method=method).main()
        match_val = self.avg_hist_dist(match, img2)
        print('Avg. histogram distances %s vs %s' % (float('inf'), match_val))
        loc_path = './test/data'
        output_filename = os.path.join(loc_path, fn_img1.split('.')[0] + '_from_' + fn_img2)
        save_img_file(img1, file_path=(os.path.join(loc_path, fn_img1)))
        save_img_file(img2, file_path=(os.path.join(loc_path, fn_img2)))
        save_img_file(match, file_path=output_filename)
        self.assertEqual(True, float('inf') > match_val)


if __name__ == '__main__':
    unittest.main()