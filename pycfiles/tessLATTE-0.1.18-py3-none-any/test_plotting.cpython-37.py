# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Nora/Documents/research/TESS/planethunters/code/LATTE/LATTE/tests/test_plotting.py
# Compiled at: 2020-03-04 05:25:42
# Size of source mod 2**32: 6397 bytes
"""

This test case is carried out with a pre-downloaded lighcurve file from TIC 55525572 Sector 5.

Testing whether the plots are produced as expected. 

python -m unittest tests/test_plotting.py
"""
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

class TestDataPlotting(unittest.TestCase):

    def test_plot(self):
        global args
        alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2, ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad = utils.download_data(indir, sector, tic, binfac=5, test='./LATTE/tests/tic55525572_lc.fits')
        X1_list, X4_list, oot_list, intr_list, bkg_list, apmask_list, arrshape_list, t_list, T0_list, tpf_filt_list = utils.download_tpf_mast(indir, transit_sec, transit_list, tic, test='./LATTE/tests/tic55525572_tp.fits')
        TESS_unbinned_t_l, TESS_binned_t_l, small_binned_t_l, TESS_unbinned_l, TESS_binned_l, small_binned_l, tpf_list = utils.download_tpf_lightkurve(indir, transit_list, sectors, tic, test='./LATTE/tests/tic55525572_tp.fits')
        utils.plot_full_md(tic, indir, alltime, allflux, all_md, alltimebinned, allfluxbinned, transit_list, args)
        utils.plot_centroid(tic, indir, alltime12, allx1, ally1, allx2, ally2, transit_list, args)
        utils.plot_background(tic, indir, alltime, allfbkg, transit_list, args)
        utils.plot_pixel_level_LC(tic, indir, X1_list, X4_list, oot_list, intr_list, bkg_list, apmask_list, arrshape_list, t_list, transit_list, args)
        utils.plot_aperturesize(tic, indir, TESS_unbinned_t_l, TESS_binned_t_l, small_binned_t_l, TESS_unbinned_l, TESS_binned_l, small_binned_l, transit_list, args)
        full_LC_path = '{}/55525572/55525572_fullLC_md.png'.format(indir)
        full_centroid = '{}/55525572/55525572_centroids.png'.format(indir)
        bkg_path = '{}/55525572/55525572_background.png'.format(indir)
        pixel_path = '{}/55525572/55525572_individual_pixel_LCs_0.png'.format(indir)
        ap_LC_path = '{}/55525572/55525572_aperture_size.png'.format(indir)
        apertures_path = '{}/55525572/55525572_apertures_0.png'.format(indir)
        time_created_full_LC = os.path.getmtime(full_LC_path)
        time_created_centroid = os.path.getmtime(full_centroid)
        time_created_bkg = os.path.getmtime(bkg_path)
        time_created_pixel = os.path.getmtime(pixel_path)
        time_created_ap_LC = os.path.getmtime(ap_LC_path)
        time_created_apertures = os.path.getmtime(apertures_path)
        t_create_full_LC = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_full_LC)))
        t_create_centroid = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_centroid)))
        t_create_bkg = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_bkg)))
        t_create_pixel = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_pixel)))
        t_create_ap_LC = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_ap_LC)))
        t_create_apertures = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_created_apertures)))
        t_now = datetime.datetime.now()
        time_since_creation_full_LC = (t_now - t_create_full_LC).seconds / 60
        time_since_creation_centroid = (t_now - t_create_centroid).seconds / 60
        time_since_creation_bkg = (t_now - t_create_bkg).seconds / 60
        time_since_creation_pixel = (t_now - t_create_pixel).seconds / 60
        time_since_creation_bkg = (t_now - t_create_ap_LC).seconds / 60
        time_since_creation_pixel = (t_now - t_create_apertures).seconds / 60
        self.assertLess(time_since_creation_full_LC, 1, 'No (new) full LC plot was made in the last five minutes')
        self.assertLess(time_since_creation_centroid, 1, 'No (new) centroid plot was made in the last five minutes')
        self.assertLess(time_since_creation_bkg, 1, 'No (new) background plot was made in the last five minutes')
        self.assertLess(time_since_creation_pixel, 1, 'No (new) pixel level LC plot was made in the last five minutes')
        self.assertLess(time_since_creation_bkg, 1, 'No (new) background plot was made in the last five minutes')
        self.assertLess(time_since_creation_pixel, 1, 'No (new) pixel level LC plot was made in the last five minutes')


if __name__ == '__main__':
    unittest.main()