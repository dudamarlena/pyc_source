# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Nora/Documents/research/TESS/planethunters/code/LATTE/tests/test_DVreport.py
# Compiled at: 2020-02-05 04:52:46
# Size of source mod 2**32: 2884 bytes
"""
A test to see whether the DV reports are generated as we would expect them to be. 
This uses previously generated input files and therfore doesn't test the generatino of the files, but only the compilation of the report. 
"""
import os, sys, time, datetime, unittest
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')
from LATTE import LATTE_DV as ldv
syspath = str(os.path.abspath(ldv.__file__))[0:-14]
indir = './test_output'
tic = '55525572'
sector = '5'
sectors = [5]
sectors_all = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
transit_list = [1454.7]
target_ra = 72.6941
target_dec = -60.9055
tessmag = 9.82
teff = 5824
srad = 1.9325
tpf_corrupt = False

class Namespace:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


args = Namespace(new_data=False, tic='no', sector='no', targetlist='no', noshow=True, o=False, auto=False, nickname='noname', FFI=False, save=True, north=False, new_path=False, mpi=False)

class TestDVreport(unittest.TestCase):

    def test_DVreport(self):
        ldv.LATTE_DV(tic, indir, syspath, transit_list, sectors_all, target_ra, target_dec, tessmag, teff, srad, [0], [0], tpf_corrupt, FFI=False, bls=False, model=False, mpi=None, test='./tests/')
        DV_path = '{}/55525572/DV_report_55525572.pdf'.format(indir)
        time_created_DV = os.path.getmtime(DV_path)
        t_create_DV = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_DV)))
        t_now = datetime.datetime.now()
        time_since_creation_DV = (t_now - t_create_DV).seconds / 60
        self.assertLess(time_since_creation_DV, 0.1, 'No full LC plot was generated in the last 60 seconds')


if __name__ == '__main__':
    unittest.main()
# global args ## Warning: Unused global