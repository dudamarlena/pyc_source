# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_utils.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 21135 bytes
from __future__ import absolute_import, division, print_function
import logging, six, numpy as np
logger = logging.getLogger(__name__)
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal
import sys
from nose.tools import assert_equal, assert_true, raises
import skxray.core.utils as core, numpy.testing as npt

def test_bin_1D():
    x = np.linspace(0, 1, 100)
    y = np.arange(100)
    nx = 10
    edges, val, count = core.bin_1D(x, y, nx)
    assert_array_almost_equal(edges, np.linspace(0, 1, nx + 1, endpoint=True))
    assert_array_almost_equal(val, np.sum(y.reshape(nx, -1), axis=1))
    assert_array_equal(count, np.ones(nx) * 10)


def test_bin_1D_2():
    """
    Test for appropriate default value handling
    """
    x = np.linspace(0, 1, 100)
    y = np.arange(100)
    nx = None
    min_x = None
    max_x = None
    edges, val, count = core.bin_1D(x=x, y=y, nx=nx, min_x=min_x, max_x=max_x)
    nx = core._defaults['bins']
    assert_array_almost_equal(edges, np.linspace(0, 1, nx + 1, endpoint=True))
    assert_array_almost_equal(val, np.sum(y.reshape(nx, -1), axis=1))
    assert_array_equal(count, np.ones(nx))


def test_bin_1D_limits():
    x = np.linspace(0, 1, 100)
    y = np.arange(100)
    nx = 10
    min_x, max_x = (0.25, 0.75)
    edges, val, count = core.bin_1D(x, y, nx, min_x, max_x)
    assert_array_almost_equal(edges, np.linspace(min_x, max_x, nx + 1, endpoint=True))
    assert_array_almost_equal(val, np.sum(y[25:75].reshape(nx, -1), axis=1))
    assert_array_equal(count, np.ones(nx) * 5)


def _bin_edges_helper(p_dict):
    bin_edges = core.bin_edges(**p_dict)
    assert_almost_equal(0, np.ptp(np.diff(bin_edges)))
    if 'nbins' in p_dict:
        nbins = p_dict['nbins']
        assert_equal(nbins + 1, len(bin_edges))
    if 'step' in p_dict:
        step = p_dict['step']
        assert_almost_equal(step, np.diff(bin_edges))
    if 'range_max' in p_dict:
        range_max = p_dict['range_max']
        assert_true(np.all(bin_edges <= range_max))
    if 'range_min' in p_dict:
        range_min = p_dict['range_min']
        assert_true(np.all(bin_edges >= range_min))
    if 'range_max' in p_dict and 'step' in p_dict:
        step = p_dict['step']
        range_max = p_dict['range_max']
        assert_true(range_max - bin_edges[(-1)] < step)


@raises(ValueError)
def _bin_edges_exceptions(param_dict):
    core.bin_edges(**param_dict)


def test_bin_edges():
    test_dicts = [
     {'range_min': 1.234, 
      'range_max': 5.678, 
      'nbins': 42, 
      'step': np.pi / 10}]
    for param_dict in test_dicts:
        for drop_key in ['range_min', 'range_max', 'step', 'nbins']:
            tmp_pdict = dict(param_dict)
            tmp_pdict.pop(drop_key)
            yield (_bin_edges_helper, tmp_pdict)

    fail_dicts = [{},
     {'range_min': 1.234, 
      'range_max': 5.678, 
      'nbins': 42, 
      'step': np.pi / 10},
     {'range_min': 1.234, 
      'step': np.pi / 10},
     {'range_min': 1.234},
     {'range_max': 1.234, 
      'range_min': 5.678, 
      'step': np.pi / 10},
     {'range_min': 1.234, 
      'range_max': 5.678, 
      'step': np.pi * 10},
     {'range_min': 1.234, 
      'range_max': 5.678, 
      'nbins': 0}]
    for param_dict in fail_dicts:
        yield (
         _bin_edges_exceptions, param_dict)


def test_grid3d():
    size = 10
    q_max = np.array([1.0, 1.0, 1.0])
    q_min = np.array([-1.0, -1.0, -1.0])
    dqn = np.array([size, size, size])
    param_dict = {'nx': dqn[0], 
     'ny': dqn[1], 
     'nz': dqn[2], 
     'xmin': q_min[0], 
     'ymin': q_min[1], 
     'zmin': q_min[2], 
     'xmax': q_max[0], 
     'ymax': q_max[1], 
     'zmax': q_max[2]}
    slc = [slice(_min + (_max - _min) / (s * 2), _max - (_max - _min) / (s * 2), complex(0.0, 1.0) * s) for _min, _max, s in zip(q_min, q_max, dqn)]
    X, Y, Z = np.mgrid[slc]
    I = np.ones_like(X).ravel()
    data = np.array([np.ravel(X),
     np.ravel(Y),
     np.ravel(Z)]).T
    mean, occupancy, std_err, oob, bounds = core.grid3d(data, I, **param_dict)
    npt.assert_array_equal(mean.ravel(), I)
    npt.assert_equal(oob, 0)
    npt.assert_array_equal(occupancy, np.ones_like(occupancy))
    npt.assert_array_equal(std_err, 0)


def test_process_grid_std_err():
    size = 10
    q_max = np.array([1.0, 1.0, 1.0])
    q_min = np.array([-1.0, -1.0, -1.0])
    dqn = np.array([size, size, size])
    param_dict = {'nx': dqn[0], 
     'ny': dqn[1], 
     'nz': dqn[2], 
     'xmin': q_min[0], 
     'ymin': q_min[1], 
     'zmin': q_min[2], 
     'xmax': q_max[0], 
     'ymax': q_max[1], 
     'zmax': q_max[2]}
    slc = [slice(_min + (_max - _min) / (s * 2), _max - (_max - _min) / (s * 2), complex(0.0, 1.0) * s) for _min, _max, s in zip(q_min, q_max, dqn)]
    X, Y, Z = np.mgrid[slc]
    I = np.hstack([j * np.ones_like(X).ravel() for j in range(1, 6)])
    data = np.vstack([np.tile(_, 5) for _ in (np.ravel(X), np.ravel(Y), np.ravel(Z))]).T
    mean, occupancy, std_err, oob, bounds = core.grid3d(data, I, **param_dict)
    npt.assert_array_equal(mean, np.ones_like(X) * np.mean(np.arange(1, 6)))
    npt.assert_equal(oob, 0)
    npt.assert_array_equal(occupancy, np.ones_like(occupancy) * 5)
    npt.assert_array_equal(std_err, np.ones_like(occupancy) * np.std(np.arange(1, 6)) / np.sqrt(4))


def test_bin_edge2center():
    test_edges = np.arange(11)
    centers = core.bin_edges_to_centers(test_edges)
    assert_array_almost_equal(0.5, centers % 1)
    assert_equal(10, len(centers))


def test_small_verbosedict():
    expected_string = "You tried to access the key 'b' which does not exist.  The extant keys are: ['a']"
    dd = core.verbosedict()
    dd['a'] = 1
    assert_equal(dd['a'], 1)
    try:
        dd['b']
    except KeyError as e:
        assert_equal(eval(six.text_type(e)), expected_string)
    else:
        assert False


def test_large_verbosedict():
    expected_sting = "You tried to access the key 'a' which does not exist.  There are 100 extant keys, which is too many to show you"
    dd = core.verbosedict()
    for j in range(100):
        dd[j] = j

    for j in range(100):
        assert_equal(dd[j], j)

    try:
        dd['a']
    except KeyError as e:
        assert_equal(eval(six.text_type(e)), expected_sting)
    else:
        assert False


def test_d_q_conversion():
    assert_equal(2 * np.pi, core.d_to_q(1))
    assert_equal(2 * np.pi, core.q_to_d(1))
    test_data = np.linspace(0.1, 5, 100)
    assert_array_almost_equal(test_data, core.d_to_q(core.q_to_d(test_data)), decimal=12)
    assert_array_almost_equal(test_data, core.q_to_d(core.d_to_q(test_data)), decimal=12)


def test_q_twotheta_conversion():
    wavelength = 1
    q = np.linspace(0, 4 * np.pi, 100)
    assert_array_almost_equal(q, core.twotheta_to_q(core.q_to_twotheta(q, wavelength), wavelength), decimal=12)
    two_theta = np.linspace(0, np.pi, 100)
    assert_array_almost_equal(two_theta, core.q_to_twotheta(core.twotheta_to_q(two_theta, wavelength), wavelength), decimal=12)


def test_radius_to_twotheta():
    dist_sample = 100
    radius = np.linspace(50, 100)
    two_theta = np.array([0.46364761, 0.47177751, 0.47984053, 0.48783644, 0.49576508,
     0.5036263, 0.51142, 0.51914611, 0.52680461, 0.53439548,
     0.54191875, 0.54937448, 0.55676277, 0.56408372, 0.57133748,
     0.57852421, 0.58564412, 0.5926974, 0.59968432, 0.60660511,
     0.61346007, 0.62024949, 0.62697369, 0.63363301, 0.6402278,
     0.64675843, 0.65322528, 0.65962874, 0.66596924, 0.67224718,
     0.67846301, 0.68461716, 0.6907101, 0.69674228, 0.70271418,
     0.70862627, 0.71447905, 0.720273, 0.72600863, 0.73168643,
     0.73730693, 0.74287063, 0.74837805, 0.75382971, 0.75922613,
     0.76456784, 0.76985537, 0.77508925, 0.78027, 0.78539816])
    assert_array_almost_equal(two_theta, core.radius_to_twotheta(dist_sample, radius), decimal=8)


def test_multi_tau_lags():
    multi_tau_levels = 3
    multi_tau_channels = 8
    delay_steps = [
     0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28]
    tot_channels, lag_steps = core.multi_tau_lags(multi_tau_levels, multi_tau_channels)
    assert_array_equal(16, tot_channels)
    assert_array_equal(delay_steps, lag_steps)


@raises(NotImplementedError)
def test_wedge_integration():
    core.wedge_integration(src_data=None, center=None, theta_start=None, delta_theta=None, r_inner=None, delta_r=None)


def test_subtract_reference_images():
    num_images = 10
    img_dims = 200
    ones = np.ones((img_dims, img_dims))
    img_lst = [ones * _ for _ in range(num_images)]
    img_arr = np.asarray(img_lst)
    is_dark_lst = [True]
    is_dark = False
    was_dark = True
    while len(is_dark_lst) < num_images:
        if was_dark:
            is_dark = False
        else:
            is_dark = np.random.rand() > 0.5
        was_dark = is_dark
        is_dark_lst.append(is_dark)

    is_dark_arr = np.asarray(is_dark_lst)
    core.subtract_reference_images(imgs=img_lst, is_reference=is_dark_arr)
    core.subtract_reference_images(imgs=img_arr, is_reference=is_dark_lst)
    core.subtract_reference_images(imgs=img_arr, is_reference=is_dark_lst)
    num_expected_images = is_dark_lst.count(False)
    subtracted = core.subtract_reference_images(img_lst, is_dark_lst)
    try:
        assert_equal(num_expected_images, len(subtracted))
    except AssertionError as ae:
        print('is_dark_lst: {0}'.format(is_dark_lst))
        print('num_expected_images: {0}'.format(num_expected_images))
        print('len(subtracted): {0}'.format(len(subtracted)))
        six.reraise(AssertionError, ae, sys.exc_info()[2])

    img_sum_lst = [img_dims * img_dims * val for val in range(num_images)]
    total_val = sum(img_sum_lst)
    expected_return_val = 0
    dark_val = 0
    for idx, (is_dark, img_val) in enumerate(zip(is_dark_lst, img_sum_lst)):
        if is_dark:
            dark_val = img_val
        else:
            expected_return_val = expected_return_val - dark_val + img_val

    return_sum = sum(subtracted)
    try:
        while True:
            return_sum = sum(return_sum)

    except TypeError:
        pass

    try:
        assert_equal(expected_return_val, return_sum)
    except AssertionError as ae:
        print('is_dark_lst: {0}'.format(is_dark_lst))
        print('expected_return_val: {0}'.format(expected_return_val))
        print('return_sum: {0}'.format(return_sum))
        six.reraise(AssertionError, ae, sys.exc_info()[2])


@raises(ValueError)
def _fail_img_to_relative_xyi_helper(input_dict):
    core.img_to_relative_xyi(**input_dict)


def test_img_to_relative_fails():
    fail_dicts = [
     {'img': np.ones((100, 100)), 'cx': 50, 'cy': 50, 'pixel_size_x': -1, 'pixel_size_y': -1},
     {'img': np.ones((100, 100)), 'cx': 50, 'cy': 50, 'pixel_size_x': 1},
     {'img': np.ones((100, 100)), 'cx': 50, 'cy': 50, 'pixel_size_y': 1},
     {'img': np.ones((100, 100)), 'cx': 50, 'cy': 50, 'pixel_size_x': -1, 'pixel_size_y': 1},
     {'img': np.ones((100, 100)), 'cx': 50, 'cy': 50, 'pixel_size_x': 1, 'pixel_size_y': -1},
     {'img': np.ones((100, 100)), 'cx': 50, 'cy': 50, 'pixel_size_x': -1},
     {'img': np.ones((100, 100)), 'cx': 50, 'cy': 50, 'pixel_size_y': -1}]
    for failer in fail_dicts:
        yield (_fail_img_to_relative_xyi_helper, failer)


def test_img_to_relative_xyi(random_seed=None):
    from skxray.core.utils import img_to_relative_xyi
    if random_seed is not None:
        np.random.seed(42)
    maxx = 2000
    maxy = 2000
    nx = int(np.random.rand() * maxx)
    ny = int(np.random.rand() * maxy)
    cx = np.random.rand() * nx
    cy = np.random.rand() * ny
    img = np.ones((nx, ny))
    cx_lst = [
     0, cx, nx]
    cy_lst = [
     0, cy, ny]
    for cx, cy in zip(cx_lst, cy_lst):
        x, y, i = img_to_relative_xyi(img=img, cx=cx, cy=cy)
        logger.debug('y {0}'.format(y))
        logger.debug('sum(y) {0}'.format(sum(y)))
        expected_total_y = sum(np.arange(ny, dtype=np.int64) - cy) * nx
        logger.debug('expected_total_y {0}'.format(expected_total_y))
        logger.debug('x {0}'.format(x))
        logger.debug('sum(x) {0}'.format(sum(x)))
        expected_total_x = sum(np.arange(nx, dtype=np.int64) - cx) * ny
        logger.debug('expected_total_x {0}'.format(expected_total_x))
        expected_total_intensity = nx * ny
        try:
            assert_almost_equal(sum(x), expected_total_x, decimal=0)
            assert_almost_equal(sum(y), expected_total_y, decimal=0)
            assert_equal(sum(i), expected_total_intensity)
        except AssertionError as ae:
            logger.error('img dims: ({0}, {1})'.format(nx, ny))
            logger.error('img center: ({0}, {1})'.format(cx, cy))
            logger.error('sum(returned_x): {0}'.format(sum(x)))
            logger.error('expected_x: {0}'.format(expected_total_x))
            logger.error('sum(returned_y): {0}'.format(sum(y)))
            logger.error('expected_y: {0}'.format(expected_total_y))
            logger.error('sum(returned_i): {0}'.format(sum(i)))
            logger.error('expected_x: {0}'.format(expected_total_intensity))
            six.reraise(AssertionError, ae, sys.exc_info()[2])


def run_image_to_relative_xyi_repeatedly():
    level = logging.ERROR
    ch = logging.StreamHandler()
    ch.setLevel(level)
    logger.addHandler(ch)
    logger.setLevel(level)
    num_calls = 0
    while 1:
        test_img_to_relative_xyi()
        num_calls += 1
        if num_calls % 10 == 0:
            print('{0} calls successful'.format(num_calls))


def test_angle_grid():
    a = core.angle_grid((3, 3), (7, 7))
    assert_equal(a[(3, -1)], 0)
    assert_almost_equal(a[(3, 0)], np.pi)
    assert_almost_equal(a[(4, 4)], np.pi / 4)
    correct_domain = np.all((a < np.pi + 0.1) & (a > -np.pi - 0.1))
    assert_true(correct_domain)


def test_radial_grid():
    a = core.radial_grid((3, 3), (7, 7))
    assert_equal(a[(3, 3)], 0)
    assert_equal(a[(3, 4)], 1)


def test_geometric_series():
    time_series = core.geometric_series(common_ratio=5, number_of_images=150)
    assert_array_equal(time_series, [1, 5, 25, 125])


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)