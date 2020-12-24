# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Nora/Documents/research/TESS/planethunters/code/LATTE/tests/test_server_response.py
# Compiled at: 2020-02-05 04:47:18
# Size of source mod 2**32: 2351 bytes
"""

This script is designed to test the LATTE python code to ensure that the server response is working. 

NOTE: requires connection to the internet and to the archive database. If these tests fail, first check that these connections 
are working by accessing the website: https://archive.stsci.edu/missions/tess/download_scripts/ in a browser.

"""
import os, unittest, requests, warnings
warnings.filterwarnings('ignore')
import sys, LATTE.LATTEutils as utils
syspath = str(os.path.abspath(utils.__file__))[0:-14]
with open('{}/_config.txt'.format(syspath), 'r') as (f):
    indir = str(f.readlines()[(-1)])

def download_LC_data():
    LC_url = 'https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_1_lc.sh'
    r_LC = requests.get(LC_url)
    return r_LC.status_code


def download_TP_data():
    TP_url = 'https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_1_tp.sh'
    r_TP = requests.get(TP_url)
    return r_TP.status_code


def download_target_list():
    target_list = 'https://tess.mit.edu/wp-content/uploads/all_targets_S001_v1.txt'
    r_target_list = requests.get(target_list)
    return r_target_list.status_code


class TestServerResponse(unittest.TestCase):

    def test_LC_request_response(self):
        responseLC = download_LC_data()
        responseTP = download_TP_data()
        responseTL = download_target_list()
        self.assertEqual(responseLC, 200, "LC data Download link does not work - can't connect to the server")
        self.assertEqual(responseTP, 200, "TP data Download link does not work - can't connect to the server")
        self.assertEqual(responseTL, 200, "Target list data Download link does not work - can't connect to the server")


if __name__ == '__main__':
    unittest.main()