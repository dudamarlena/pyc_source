# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Nora/Documents/research/TESS/planethunters/code/LATTE/tests/test_pyaneti.py
# Compiled at: 2020-02-05 04:50:51
# Size of source mod 2**32: 2154 bytes
"""
Test whether the pyaneti modeling is working correctly. Pyaneti is not available in the current verison of the code. 

-- NOTE: this is testing whether it is working for single transit events and not multi transit

-- requires pyaneti to be installed.

-- this test is not complete as pyaneti is not included in the first release of the data.
"""
import os, sys, time, datetime, unittest, numpy as np
from dateutil import parser
import warnings
warnings.filterwarnings('ignore')
import LATTE.LATTEutils as utils
syspath = str(os.path.abspath(utils.__file__))[0:-14]
indir = './test_output'
tic = '55525572'
sector = '5'
sectors = [5]
transit_list = [1454.7]
transit_sec = '5'
mstar = 1
teff = 5824
srad = 1.9325

class TestPyaneti(unittest.TestCase):
    __doc__ = '\n    Test the extraction of the information from the TP file (already on the system)\n    '

    def test_pyaneti(self):
        if os.path.exists('{}/pyaneti_LATTE.py'.format(syspath)):
            print('Running Pyaneti modelling - this could take a while so be patient...')
            transit_list_model = '{}'.format(str(np.asarray(transit_list)))[1:-1]
            os.system('python3 {}/pyaneti_LATTE.py {} {} {} {} {} {} {}'.format(syspath, tic, indir, syspath, mstar, teff, srad, transit_list_model))
        else:
            print("Pyaneti has not been installed so you can't model anything yet. Contact Nora or Oscar for the LATTE version of the Pyaneti code.")


if __name__ == '__main__':
    unittest.main()