# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\roi_data_layer\minibatch.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 2767 bytes
"""Compute minibatch blobs for training a Fast R-CNN network."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2, numpy as np
import numpy.random as npr
from model.config import cfg
from utils.blob import prep_im_for_blob, im_list_to_blob

def get_minibatch(roidb, num_classes):
    """Given a roidb, construct a minibatch sampled from it."""
    num_images = len(roidb)
    random_scale_inds = npr.randint(0, high=(len(cfg.TRAIN.SCALES)), size=num_images)
    if not cfg.TRAIN.BATCH_SIZE % num_images == 0:
        raise AssertionError('num_images ({}) must divide BATCH_SIZE ({})'.format(num_images, cfg.TRAIN.BATCH_SIZE))
    else:
        im_blob, im_scales = _get_image_blob(roidb, random_scale_inds)
        blobs = {'data': im_blob}
        assert len(im_scales) == 1, 'Single batch only'
        assert len(roidb) == 1, 'Single batch only'
        if cfg.TRAIN.USE_ALL_GT:
            gt_inds = np.where(roidb[0]['gt_classes'] != 0)[0]
        else:
            gt_inds = np.where(roidb[0]['gt_classes'] != 0 & np.all((roidb[0]['gt_overlaps'].toarray() > -1.0), axis=1))[0]
    gt_boxes = np.empty((len(gt_inds), 5), dtype=(np.float32))
    gt_boxes[:, 0:4] = roidb[0]['boxes'][gt_inds, :] * im_scales[0]
    gt_boxes[:, 4] = roidb[0]['gt_classes'][gt_inds]
    blobs['gt_boxes'] = gt_boxes
    blobs['im_info'] = np.array([
     im_blob.shape[1], im_blob.shape[2], im_scales[0]],
      dtype=(np.float32))
    return blobs


def _get_image_blob(roidb, scale_inds):
    """Builds an input blob from the images in the roidb at the specified
    scales.
    """
    num_images = len(roidb)
    processed_ims = []
    im_scales = []
    for i in range(num_images):
        im = cv2.imread(roidb[i]['image'])
        if roidb[i]['flipped']:
            im = im[:, ::-1, :]
        target_size = cfg.TRAIN.SCALES[scale_inds[i]]
        im, im_scale = prep_im_for_blob(im, cfg.PIXEL_MEANS, target_size, cfg.TRAIN.MAX_SIZE)
        im_scales.append(im_scale)
        processed_ims.append(im)

    blob = im_list_to_blob(processed_ims)
    return (
     blob, im_scales)