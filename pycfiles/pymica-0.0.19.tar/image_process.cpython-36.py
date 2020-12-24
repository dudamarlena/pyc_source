# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/util/image_process.py
# Compiled at: 2020-04-15 21:24:26
# Size of source mod 2**32: 6522 bytes
from __future__ import absolute_import, print_function
import numpy as np
from scipy import ndimage

def get_ND_bounding_box(volume, margin=None):
    """
    get the bounding box of nonzero region in an ND volume
    """
    input_shape = volume.shape
    if margin is None:
        margin = [
         0] * len(input_shape)
    elif not len(input_shape) == len(margin):
        raise AssertionError
    indxes = np.nonzero(volume)
    idx_min = []
    idx_max = []
    for i in range(len(input_shape)):
        idx_min.append(indxes[i].min())
        idx_max.append(indxes[i].max() + 1)

    for i in range(len(input_shape)):
        idx_min[i] = max(idx_min[i] - margin[i], 0)
        idx_max[i] = min(idx_max[i] + margin[i], input_shape[i])

    return (idx_min, idx_max)


def crop_ND_volume_with_bounding_box(volume, min_idx, max_idx):
    """
    crop/extract a subregion form an nd image.
    """
    dim = len(volume.shape)
    if not (dim >= 2 and dim <= 5):
        raise AssertionError
    elif not max_idx[0] - min_idx[0] <= volume.shape[0]:
        raise AssertionError
    else:
        if dim == 2:
            output = volume[np.ix_(range(min_idx[0], max_idx[0]), range(min_idx[1], max_idx[1]))]
        else:
            if dim == 3:
                output = volume[np.ix_(range(min_idx[0], max_idx[0]), range(min_idx[1], max_idx[1]), range(min_idx[2], max_idx[2]))]
            else:
                if dim == 4:
                    output = volume[np.ix_(range(min_idx[0], max_idx[0]), range(min_idx[1], max_idx[1]), range(min_idx[2], max_idx[2]), range(min_idx[3], max_idx[3]))]
                else:
                    if dim == 5:
                        output = volume[np.ix_(range(min_idx[0], max_idx[0]), range(min_idx[1], max_idx[1]), range(min_idx[2], max_idx[2]), range(min_idx[3], max_idx[3]), range(min_idx[4], max_idx[4]))]
                    else:
                        raise ValueError('the dimension number shoud be 2 to 5')
    return output


def set_ND_volume_roi_with_bounding_box_range(volume, bb_min, bb_max, sub_volume, addition=True):
    """
    set a subregion to an nd image. if addition is True, the original volume is added by the subregion.
    """
    dim = len(bb_min)
    out = volume
    if dim == 2:
        if addition:
            out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]))] += sub_volume
        else:
            out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]))] = sub_volume
    elif dim == 3:
        if addition:
            out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]), range(bb_min[2], bb_max[2]))] += sub_volume
        else:
            out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]), range(bb_min[2], bb_max[2]))] = sub_volume
    elif dim == 4:
        if addition:
            out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]), range(bb_min[2], bb_max[2]), range(bb_min[3], bb_max[3]))] += sub_volume
        else:
            out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]), range(bb_min[2], bb_max[2]), range(bb_min[3], bb_max[3]))] = sub_volume
    else:
        if dim == 5:
            if addition:
                out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]), range(bb_min[2], bb_max[2]), range(bb_min[3], bb_max[3]), range(bb_min[4], bb_max[4]))] += sub_volume
            else:
                out[np.ix_(range(bb_min[0], bb_max[0]), range(bb_min[1], bb_max[1]), range(bb_min[2], bb_max[2]), range(bb_min[3], bb_max[3]), range(bb_min[4], bb_max[4]))] = sub_volume
        else:
            raise ValueError('array dimension should be 2 to 5')
        return out


def get_largest_component(image):
    """
    get the largest component from 2D or 3D binary image
    image: nd array
    """
    dim = len(image.shape)
    if image.sum() == 0:
        print('the largest component is null')
        return image
    else:
        if dim == 2:
            s = ndimage.generate_binary_structure(2, 1)
        else:
            if dim == 3:
                s = ndimage.generate_binary_structure(3, 1)
            else:
                raise ValueError('the dimension number should be 2 or 3')
        labeled_array, numpatches = ndimage.label(image, s)
        sizes = ndimage.sum(image, labeled_array, range(1, numpatches + 1))
        max_label = np.where(sizes == sizes.max())[0] + 1
        output = np.asarray(labeled_array == max_label, np.uint8)
        return output


def get_euclidean_distance(image, dim=3, spacing=[1.0, 1.0, 1.0]):
    """
    get euclidean distance transform of 2D or 3D binary images
    the output distance map is unsigned
    """
    img_shape = image.shape
    input_dim = len(img_shape)
    if input_dim != 3:
        raise ValueError('Not implemented for {0:}D image'.format(input_dim))
    else:
        if dim == 2:
            raise ValueError('Not implemented for {0:}D image'.format(input_dim))
        else:
            if dim == 3:
                fg_dis_map = ndimage.morphology.distance_transform_edt(image > 0.5)
                bg_dis_map = ndimage.morphology.distance_transform_edt(image <= 0.5)
                dis_map = bg_dis_map - fg_dis_map
            else:
                raise ValueError('Not implemented for {0:}D distance'.format(dim))
    return dis_map


def convert_label(label, source_list, target_list):
    """
    convert a label map based a source list and a target list of labels
    label: nd array 
    source_list: a list of labels that will be converted, e.g. [0, 1, 2, 4]
    target_list: a list of target labels, e.g. [0, 1, 2, 3]
    """
    assert len(source_list) == len(target_list)
    label_converted = np.zeros_like(label)
    for i in range(len(source_list)):
        label_temp = np.asarray(label == source_list[i], label.dtype)
        label_temp = label_temp * target_list[i]
        label_converted = label_converted + label_temp

    return label_converted