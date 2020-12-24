# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_recip.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 6123 bytes
from __future__ import absolute_import, division, print_function
import six, numpy as np, numpy.testing as npt
from nose.tools import raises
from skxray.core import recip

def test_process_to_q():
    detector_size = (256, 256)
    pixel_size = (0.108, 0.108)
    calibrated_center = (128.0, 128.0)
    dist_sample = 355.0
    energy = 640
    hc_over_e = 12398.4
    wavelength = hc_over_e / energy
    ub_mat = np.array([[-0.01231028454, 0.7405370482, 0.06323870032],
     [
      0.4450897473, 0.04166852402, -0.9509449389],
     [
      -0.7449130975, 0.01265920962, -0.5692399963]])
    setting_angles = np.array([[40.0, 15.0, 30.0, 25.0, 10.0, 5.0],
     [
      90.0, 60.0, 0.0, 30.0, 10.0, 5.0]])
    pdict = {}
    pdict['setting_angles'] = setting_angles
    pdict['detector_size'] = detector_size
    pdict['pixel_size'] = pixel_size
    pdict['calibrated_center'] = calibrated_center
    pdict['dist_sample'] = dist_sample
    pdict['wavelength'] = wavelength
    pdict['ub'] = ub_mat
    hkl = recip.process_to_q(**pdict)
    known_hkl = [
     (
      32896, np.array([-0.15471196, 0.19673939, -0.11440936])),
     (
      98432, np.array([0.10205953, 0.45624416, -0.27200778]))]
    for pixel, kn_hkl in known_hkl:
        npt.assert_array_almost_equal(hkl[pixel], kn_hkl, decimal=8)

    pass_list = recip.process_to_q.frame_mode
    pass_list.append(None)
    for passes in pass_list:
        recip.process_to_q(frame_mode=passes, **pdict)


@raises(KeyError)
def _process_to_q_exception(param_dict, frame_mode):
    recip.process_to_q(frame_mode=frame_mode, **param_dict)


def test_frame_mode_fail():
    detector_size = (256, 256)
    pixel_size = (0.108, 0.108)
    calibrated_center = (128.0, 128.0)
    dist_sample = 355.0
    energy = 640
    hc_over_e = 12398.4
    wavelength = hc_over_e / energy
    ub_mat = np.array([[-0.01231028454, 0.7405370482, 0.06323870032],
     [
      0.4450897473, 0.04166852402, -0.9509449389],
     [
      -0.7449130975, 0.01265920962, -0.5692399963]])
    setting_angles = np.array([[40.0, 15.0, 30.0, 25.0, 10.0, 5.0],
     [
      90.0, 60.0, 0.0, 30.0, 10.0, 5.0]])
    pdict = {}
    pdict['setting_angles'] = setting_angles
    pdict['detector_size'] = detector_size
    pdict['pixel_size'] = pixel_size
    pdict['calibrated_center'] = calibrated_center
    pdict['dist_sample'] = dist_sample
    pdict['wavelength'] = wavelength
    pdict['ub'] = ub_mat
    for fails in [0, 5, 'cat']:
        yield (_process_to_q_exception, pdict, fails)


def test_hkl_to_q():
    b = np.array([[-4, -3, -2],
     [
      -1, 0, 1],
     [
      2, 3, 4],
     [
      6, 9, 10]])
    b_norm = np.array([5.38516481, 1.41421356, 5.38516481,
     14.73091986])
    npt.assert_array_almost_equal(b_norm, recip.hkl_to_q(b))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)