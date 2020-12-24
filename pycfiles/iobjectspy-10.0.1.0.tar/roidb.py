# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\roi_data_layer\roidb.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 1952 bytes
"""Transform a roidb into a trainable roidb by adding a bunch of metadata."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import PIL, numpy as np

def prepare_roidb(imdb):
    """Enrich the imdb's roidb by adding some derived quantities that
    are useful for training. This function precomputes the maximum
    overlap, taken over ground-truth boxes, between each ROI and
    each ground-truth box. The class with maximum overlap is also
    recorded.
    """
    roidb = imdb.roidb
    if not imdb.name.startswith('coco'):
        sizes = [PIL.Image.open(imdb.image_path_at(i)).size for i in range(imdb.num_images)]
    for i in range(len(imdb.image_index)):
        roidb[i]['image'] = imdb.image_path_at(i)
        if not imdb.name.startswith('coco'):
            roidb[i]['width'] = sizes[i][0]
            roidb[i]['height'] = sizes[i][1]
        gt_overlaps = roidb[i]['gt_overlaps'].toarray()
        max_overlaps = gt_overlaps.max(axis=1)
        max_classes = gt_overlaps.argmax(axis=1)
        roidb[i]['max_classes'] = max_classes
        roidb[i]['max_overlaps'] = max_overlaps
        zero_inds = np.where(max_overlaps == 0)[0]
        assert all(max_classes[zero_inds] == 0)
        nonzero_inds = np.where(max_overlaps > 0)[0]
        assert all(max_classes[nonzero_inds] != 0)