# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/epitome/generators.py
# Compiled at: 2020-01-22 09:52:53
# Size of source mod 2**32: 12730 bytes
"""
Functions for data generators.
"""
import numpy as np, tensorflow as tf
from .constants import *
from .functions import *
import epitome.iio as iio, glob
np.random.seed(0)

def load_data(data, label_cell_types, eval_cell_types, matrix, assaymap, cellmap, radii, **kwargs):
    exclusive = True
    mode = kwargs.get('mode')
    indices = kwargs.get('indices')
    if not isinstance(indices, np.ndarray) and not isinstance(indices, list):
        if mode == Dataset.TRAIN:
            feature_indices = np.concatenate(list(map(lambda c: get_y_indices_for_cell(matrix, cellmap, c), list(cellmap))))
            feature_indices = feature_indices[(feature_indices != -1)]
            if len(list(assaymap)) > 2:
                rowsums = np.sum((data[feature_indices, :]), axis=1)
                scale_factor = 1 / rowsums
                scaled = data[feature_indices, :] * scale_factor[:, np.newaxis]
                indices_zero = np.where(np.sum(scaled, axis=0) > 0)[0]
                indices = np.random.choice(indices_zero, (int(indices_zero.shape[0] * 0.4)), p=((np.sum(scaled, axis=0) / np.sum(scaled))[indices_zero]))
            else:
                feature_indices = np.concatenate(list(map(lambda c: get_y_indices_for_cell(matrix, cellmap, c), list(cellmap))))
                TF_indices = feature_indices.reshape([len(cellmap), len(assaymap)])[:, 1]
                TF_indices = TF_indices[(TF_indices != -1)]
                feature_indices = feature_indices[(feature_indices != -1)]
                positive_indices = np.where(np.sum((data[TF_indices, :]), axis=0) > 1)[0]
                indices_probs = np.ones([data.shape[1]])
                indices_probs[positive_indices] = 0
                indices_probs = indices_probs / np.sum(indices_probs, keepdims=1)
                negative_indices = np.random.choice((np.arange(0, data.shape[1])), (positive_indices.shape[0] * 10), p=indices_probs)
                indices = np.sort(np.concatenate([negative_indices, positive_indices]))
        else:
            indices = range(0, data.shape[(-1)])
    if not isinstance(indices, np.ndarray):
        if not isinstance(indices, list):
            indices = range(0, data.shape[(-1)])
    if not isinstance(mode, Dataset):
        raise ValueError('mode is not a Dataset enum')
    if mode == Dataset.RUNTIME:
        label_cell_types = [
         'PLACEHOLDER_CELL']
        dnase_vector = kwargs.get('dnase_vector')
        random_cell = list(cellmap)[0]
    print('using %s as labels for mode %s' % (label_cell_types, mode))
    radii_str = list(map(lambda x: 'DNASE_RADII_%i' % x, radii))

    def g():
        for i in indices:
            for cell in label_cell_types:
                dnases = []
                dnases_double_positive = []
                dnases_agreement = []
                feature_cell_indices_list = list(map(lambda c: get_y_indices_for_cell(matrix, cellmap, c), eval_cell_types))
                feature_cell_indices_list = [m[(m != -1)] for m in feature_cell_indices_list]
                if mode != Dataset.RUNTIME:
                    label_cell_indices = get_y_indices_for_cell(matrix, cellmap, cell)
                    label_cell_indices_no_dnase = np.delete(label_cell_indices, [0])
                    assay_mask = np.copy(label_cell_indices_no_dnase)
                    assay_mask[assay_mask == -1] = 0
                    assay_mask[assay_mask > 0] = 1
                else:
                    label_count = len(get_y_indices_for_cell(matrix, cellmap, random_cell)) - 1
                    garbage_labels = assay_mask = np.zeros(label_count)
                dnase_indices = np.array([x[0] for x in feature_cell_indices_list])
                for r, radius in enumerate(radii):
                    min_radius = max(0, i - radius + 1)
                    max_radius = min(i + radius, data.shape[1])
                    if exclusive:
                        if r != 0:
                            radius_range_1 = np.arange(min_radius, max(0, i - radii[(r - 1)] + 1))
                            radius_range_2 = np.arange(i + radii[(r - 1)], max_radius)
                            radius_range = np.concatenate([radius_range_1, radius_range_2])
                    else:
                        radius_range = np.arange(min_radius, max_radius)
                    if mode == Dataset.RUNTIME:
                        dnase_double_positive = np.average((data[(dnase_indices[:, None], radius_range)] * dnase_vector[radius_range]),
                          axis=1)
                        dnase_agreement = np.average((data[(dnase_indices[:, None], radius_range)] == dnase_vector[radius_range]),
                          axis=1)
                    else:
                        dnase_double_positive = np.average((data[(dnase_indices[:, None], radius_range)] * data[(label_cell_indices[0], radius_range)]),
                          axis=1)
                        dnase_agreement = np.average((data[(dnase_indices[:, None], radius_range)] == data[(label_cell_indices[0], radius_range)]),
                          axis=1)
                    dnases_double_positive.extend(dnase_double_positive)
                    dnases_agreement.extend(dnase_agreement)

                dnases_agreement_reshaped = np.array(dnases_agreement).reshape([len(radii), len(eval_cell_types)]).T
                dnases_double_positive_reshaped = np.array(dnases_double_positive).reshape([len(radii), len(eval_cell_types)]).T
                dnases = np.concatenate([dnases_agreement_reshaped, dnases_double_positive_reshaped], axis=1)
                final = []
                for j, c in enumerate(eval_cell_types):
                    cell_features = data[(feature_cell_indices_list[j], i)]
                    cell_dnase = dnases[j, :]
                    concat = np.concatenate([cell_features, cell_dnase])
                    if c == cell:
                        final.append(np.zeros(len(concat)))
                    else:
                        final.append(concat)

                if mode != Dataset.RUNTIME:
                    labels = data[(label_cell_indices_no_dnase, i)]
                else:
                    labels = garbage_labels
                final.append(labels.astype(np.float32))
                final.append(assay_mask.astype(np.float32))
                yield tuple(final)

    return g


def generator_to_tf_dataset(g, batch_size, shuffle_size, prefetch_size):
    """
    Generates a tensorflow dataset from a data generator.
    
    :param g: data generator
    :param batch_size: number of elements in generator to combine into a single batch
    :param shuffle_size: number of elements from the  generator fromw which the new dataset will shuffle
    :param prefetch_size: maximum number of elements that will be buffered  when prefetching
    
    :returns: tuple of (label shape, tf.data.Dataset)
    """
    for f in g():
        break

    labels = f[(-2)]
    assay_mask = f[(-1)]
    features = f[:-2]
    shapes = []
    for i in f:
        shapes.append(i.shape)

    try:
        dataset = tf.data.Dataset.from_generator(g,
          output_types=((
         tf.float32,) * len(f)),
          output_shapes=(tuple(shapes)))
    except NameError as e:
        print('Error: no data, %s' % e)
        dataset = tf.data.Dataset.from_generator(g,
          output_types=((
         tf.float32,) * len(features)))

    dataset = dataset.batch(batch_size)
    dataset = dataset.shuffle(shuffle_size)
    dataset = dataset.repeat()
    dataset = dataset.prefetch(prefetch_size)
    try:
        features
        return ([i.shape[0] for i in features], labels.shape, dataset)
    except NameError as e:
        return (
         None, None, dataset)