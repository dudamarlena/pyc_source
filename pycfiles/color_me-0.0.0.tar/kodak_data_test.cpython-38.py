# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/kodak_data_test.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 2600 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
from color_matcher.top_level import ColorMatcher
from color_matcher.io_handler import *
from .img_downloader import download_stack
import unittest, os

class MatchKodakTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        (super(MatchKodakTester, self).__init__)(*args, **kwargs)

    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dat_path = os.path.join(self.dir_path, 'data')

    def test_kodak_images(self):
        url = 'https://www.math.purdue.edu/~lucier/PHOTO_CD/BMP_IMAGES/'
        self.fnames = ['IMG' + str(i + 1).zfill(4) + '.bmp' for i in range(24)]
        loc_path = os.path.join(self.dat_path, 'kodak')
        try:
            os.makedirs(loc_path, 493)
            os.makedirs(os.path.join(loc_path, 'results'), 493)
        except:
            pass
        else:
            if not os.path.exists(loc_path):
                download_stack(url, loc_path)
            for fn_img1 in self.fnames:
                for fn_img2 in self.fnames:
                    img1 = load_img_file(os.path.join(loc_path, fn_img1))
                    img2 = load_img_file(os.path.join(loc_path, fn_img2))
                    res = ColorMatcher(img1, img2, method='hm-mkl-hm').main()
                    val = self.avg_hist_dist(res, img2)
                    print('Avg. histogram distance %s' % val)
                    output_filename = os.path.join(loc_path, 'results', fn_img1.split('.')[0] + '_from_' + fn_img2)
                    save_img_file(res, file_path=output_filename)
                    self.assertEqual(True, val != 0)