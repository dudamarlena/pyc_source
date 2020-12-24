# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/tests/test_roi.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 13979 bytes
from __future__ import absolute_import, division, print_function
import logging, numpy as np
from .. import roi
from .. import utils as core
import itertools
from skimage import morphology
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_almost_equal
from nose.tools import assert_equal, assert_true, assert_raises
logger = logging.getLogger(__name__)

def test_rectangles():
    shape = (15, 26)
    roi_data = np.array(([2, 2, 6, 3], [6, 7, 8, 5], [8, 18, 5, 10]), dtype=np.int64)
    all_roi_inds = roi.rectangles(roi_data, shape)
    roi_inds, pixel_list = roi.extract_label_indices(all_roi_inds)
    ty = np.zeros(shape).ravel()
    ty[pixel_list] = roi_inds
    num_pixels_m = np.bincount(ty.astype(int))[1:]
    re_mesh = ty.reshape(*shape)
    for i, (col_coor, row_coor, col_val, row_val) in enumerate(roi_data, 0):
        ind_co = np.column_stack(np.where(re_mesh == i + 1))
        left, right = np.max([col_coor, 0]), np.min([col_coor + col_val,
         shape[0]])
        top, bottom = np.max([row_coor, 0]), np.min([row_coor + row_val,
         shape[1]])
        assert_almost_equal(left, ind_co[0][0])
        assert_almost_equal(right - 1, ind_co[(-1)][0])
        assert_almost_equal(top, ind_co[0][1])
        assert_almost_equal(bottom - 1, ind_co[(-1)][(-1)])


def test_rings():
    center = (100.0, 100.0)
    img_dim = (200, 205)
    first_q = 10.0
    delta_q = 5.0
    num_rings = 7
    one_step_q = 5.0
    step_q = [2.5, 3.0, 5.8]
    edges = roi.ring_edges(first_q, width=delta_q, spacing=one_step_q, num_rings=num_rings)
    print('edges there is same spacing between rings ', edges)
    label_array = roi.rings(edges, center, img_dim)
    print('label_array there is same spacing between rings', label_array)
    label_mask, pixel_list = roi.extract_label_indices(label_array)
    num_pixels = np.bincount(label_mask, minlength=np.max(label_mask) + 1)
    num_pixels = num_pixels[1:]
    edges = roi.ring_edges(first_q, width=delta_q, spacing=2.5, num_rings=num_rings)
    print('edges there is same spacing between rings ', edges)
    label_array = roi.rings(edges, center, img_dim)
    print('label_array there is same spacing between rings', label_array)
    label_mask, pixel_list = roi.extract_label_indices(label_array)
    num_pixels = np.bincount(label_mask, minlength=np.max(label_mask) + 1)
    num_pixels = num_pixels[1:]
    edges = roi.ring_edges(first_q, width=delta_q, spacing=step_q, num_rings=4)
    print('edges when there is different spacing between rings', edges)
    label_array = roi.rings(edges, center, img_dim)
    print('label_array there is different spacing between rings', label_array)
    label_mask, pixel_list = roi.extract_label_indices(label_array)
    num_pixels = np.bincount(label_mask, minlength=np.max(label_mask) + 1)
    num_pixels = num_pixels[1:]
    edges = roi.ring_edges(first_q, width=delta_q, num_rings=num_rings)
    print('edges', edges)
    label_array = roi.rings(edges, center, img_dim)
    print('label_array', label_array)
    label_mask, pixel_list = roi.extract_label_indices(label_array)
    num_pixels = np.bincount(label_mask, minlength=np.max(label_mask) + 1)
    num_pixels = num_pixels[1:]
    print(np.unique(label_array))
    actual_num_rings = len(np.unique(label_array)) - 1
    assert_equal(actual_num_rings, num_rings)
    ring_areas = np.bincount(label_array.ravel())[1:]
    area_comparison = np.diff(ring_areas)
    print(area_comparison)
    areas_monotonically_increasing = np.all(area_comparison > 0)
    assert_true(areas_monotonically_increasing)
    assert_raises(ValueError, lambda : roi.ring_edges(1, 2))
    assert_raises(ValueError, lambda : roi.ring_edges(1, [1, 2, 3], num_rings=2))
    assert_raises(ValueError, lambda : roi.ring_edges(1, [1, 2, 3], [1]))
    assert_raises(ValueError, lambda : roi.ring_edges(1, [1, 2, 3], [1, 2, 3]))
    assert_raises(ValueError, lambda : roi.ring_edges(1, [1, 2, 3], [1, 2], 5))


def _helper_check(pixel_list, inds, num_pix, edges, center, img_dim, num_qs):
    ty = np.zeros(img_dim).ravel()
    ty[pixel_list] = inds
    data = ty.reshape(img_dim[0], img_dim[1])
    grid_values = core.radial_grid(img_dim, center)
    zero_grid = np.zeros((img_dim[0], img_dim[1]))
    for r in range(num_qs):
        vl = (edges[r][0] <= grid_values) & (grid_values < edges[r][1])
        zero_grid[vl] = r + 1

    num_pixels = []
    for r in range(num_qs):
        num_pixels.append(int(np.histogramdd(np.ravel(grid_values), bins=1, range=[
         [
          edges[r][0],
          edges[r][1] - 1e-06]])[0][0]))

    assert_array_equal(num_pix, num_pixels)


def test_segmented_rings():
    center = (75, 75)
    img_dim = (150, 140)
    first_q = 5
    delta_q = 5
    num_rings = 4
    slicing = 4
    edges = roi.ring_edges(first_q, width=delta_q, spacing=4, num_rings=num_rings)
    print('edges', edges)
    label_array = roi.segmented_rings(edges, slicing, center, img_dim, offset_angle=0)
    print('label_array for segmented_rings', label_array)
    label_list = np.unique(label_array.ravel())
    actual_num_labels = len(label_list) - 1
    num_labels = num_rings * slicing
    assert_equal(actual_num_labels, num_labels)
    assert_array_equal(label_list, np.arange(num_labels + 1))
    num_pixels = np.bincount(label_array.ravel())
    expected_num_pixels = [18372, 59, 59, 59, 59, 129, 129, 129,
     129, 200, 200, 200, 200, 269, 269, 269, 269]
    assert_array_equal(num_pixels, expected_num_pixels)


def test_roi_pixel_values():
    images = morphology.diamond(8)
    label_array = np.zeros((256, 256))
    assert_raises(ValueError, lambda : roi.roi_pixel_values(images, label_array))
    center = (8.0, 8.0)
    inner_radius = 2.0
    width = 1
    spacing = 1
    edges = roi.ring_edges(inner_radius, width, spacing, num_rings=5)
    rings = roi.rings(edges, center, images.shape)
    intensity_data, index = roi.roi_pixel_values(images, rings)
    assert_array_equal(intensity_data[0], [1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1])
    assert_array_equal([1, 2, 3, 4, 5], index)


def test_roi_max_counts():
    img_stack1 = np.random.randint(0, 60, size=(50, 50, 50))
    img_stack2 = np.random.randint(0, 60, size=(100, 50, 50))
    img_stack1[0][(20, 20)] = 60
    samples = (
     img_stack1, img_stack2)
    label_array = np.zeros(img_stack1[0].shape)
    label_array[img_stack1[0] < 20] = 1
    label_array[img_stack1[0] > 40] = 2
    assert_array_equal(60, roi.roi_max_counts(samples, label_array))


def test_static_test_sets():
    images1 = []
    for i in range(10):
        int_array = np.tril(i * np.ones(50))
        int_array[int_array == 0] = i * 100
        images1.append(int_array)

    images2 = []
    for i in range(20):
        int_array = np.triu(i * np.ones(50))
        int_array[int_array == 0] = i * 100
        images2.append(int_array)

    samples = {'sample1': np.asarray(images1), 'sample2': np.asarray(images2)}
    roi_data = np.array(([2, 30, 12, 15], [40, 20, 15, 10]), dtype=np.int64)
    label_array = roi.rectangles(roi_data, shape=(50, 50))
    roi_data = []
    for k, v in sorted(samples.items()):
        intensity, index_list = roi.mean_intensity(v, label_array)
        roi_data.append(intensity)

    return_values = [roi_data[0][:, 0], roi_data[0][:, 1],
     roi_data[1][:, 0], roi_data[1][:, 1]]
    expected_values = [
     np.asarray([float(x) for x in range(0, 1000, 100)]),
     np.asarray([float(x) for x in range(0, 10, 1)]),
     np.asarray([float(x) for x in range(0, 20, 1)]),
     np.asarray([float(x) for x in range(0, 2000, 100)])]
    err_msg = ['roi%s of sample%s is incorrect' % (i, j) for i, j in itertools.product((1,
                                                                                        2), (1,
                                                                                             2))]
    for returned, expected, err in zip(return_values, expected_values, err_msg):
        assert_array_equal(returned, expected, err_msg=err, verbose=True)


def test_circular_average():
    image = np.zeros((12, 12))
    calib_center = (5, 5)
    inner_radius = 1
    edges = roi.ring_edges(inner_radius, width=1, spacing=1, num_rings=2)
    labels = roi.rings(edges, calib_center, image.shape)
    image[labels == 1] = 10
    image[labels == 2] = 10
    bin_cen, ring_avg = roi.circular_average(image, calib_center, nx=6)
    assert_array_almost_equal(bin_cen, [0.70710678, 2.12132034,
     3.53553391, 4.94974747, 6.36396103,
     7.77817459], decimal=6)
    assert_array_almost_equal(ring_avg, [8.0, 2.5, 5.55555556, 0.0,
     0.0, 0.0], decimal=6)


def test_kymograph():
    calib_center = (25, 25)
    inner_radius = 5
    edges = roi.ring_edges(inner_radius, width=2, num_rings=1)
    labels = roi.rings(edges, calib_center, (50, 50))
    images = []
    num_images = 100
    for i in range(num_images):
        int_array = i * np.ones(labels.shape)
        images.append(int_array)

    kymograph_data = roi.kymograph(np.asarray(images), labels, num=1)
    expected_shape = (
     num_images, np.sum(labels[(labels == 1)]))
    assert kymograph_data.shape[0] == expected_shape[0]
    assert kymograph_data.shape[1] == expected_shape[1]
    assert np.all(kymograph_data[:, 0] == np.arange(num_images))
    for row in kymograph_data:
        if not np.all(row == row[0]):
            raise AssertionError