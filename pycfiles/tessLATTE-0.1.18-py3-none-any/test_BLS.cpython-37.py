# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Nora/Documents/research/TESS/planethunters/code/LATTE/LATTE/tests/test_BLS.py
# Compiled at: 2020-03-04 05:25:43
# Size of source mod 2**32: 3811 bytes
import os, sys, time, datetime, unittest
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')
import LATTE.LATTEutils as utils
syspath = str(os.path.abspath(utils.__file__))[0:-14]
indir = './LATTE/test_output'
tic = '55525572'
sector = '5'
sectors = [5]
transit_list = [1454.7]
transit_sec = '5'

class Namespace:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


args = Namespace(new_data=False, tic='no', sector='no', targetlist='no', noshow=True,
  o=False,
  auto=False,
  nickname='noname',
  FFI=False,
  save=True,
  north=False,
  new_path=False,
  mpi=False)

class TestBoxLeastSquareTest(unittest.TestCase):
    __doc__ = '\n    Test the extraction of the information from the TP file (already on the system)\n    '

    def test_BLS(self):
        global args
        alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2, ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad = utils.download_data(indir, sector, tic, binfac=5, test='./LATTE/tests/tic55525572_lc.fits')
        bls_stats1, bls_stats2 = utils.data_bls(tic, indir, alltime, allflux, allfluxbinned, alltimebinned, args)
        BLS1_path = '{}/55525572/55525572_bls_first.png'.format(indir)
        BLS2_path = '{}/55525572/55525572_bls_second.png'.format(indir)
        time_created_BLS1 = os.path.getmtime(BLS1_path)
        time_created_BLS2 = os.path.getmtime(BLS2_path)
        t_create_BLS1 = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_BLS1)))
        t_create_BLS2 = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_BLS2)))
        t_now = datetime.datetime.now()
        time_since_creation_BLS1 = (t_now - t_create_BLS1).seconds / 60
        time_since_creation_BLS2 = (t_now - t_create_BLS2).seconds / 60
        self.assertLess(time_since_creation_BLS1, 1, 'No BLS plot generated in the last 60 seconds')
        self.assertAlmostEqual((float(bls_stats1[0])), (float(16.910000000000014)), places=5)
        self.assertAlmostEqual((float(bls_stats1[1])), (float(0.3901880448498858)), places=5)
        self.assertAlmostEqual(float(bls_stats2[0]), float(0.51))
        self.assertAlmostEqual((float(bls_stats2[1])), (float(0.305186334480843)), places=5)


if __name__ == '__main__':
    unittest.main()