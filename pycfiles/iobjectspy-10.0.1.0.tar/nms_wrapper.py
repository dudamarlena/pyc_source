# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\model\nms_wrapper.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 745 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from model.config import cfg
from utils.nms import cpu_nms

def nms(dets, thresh, force_cpu=False):
    """Dispatch to either CPU or GPU NMS implementations."""
    if dets.shape[0] == 0:
        return []
    if cfg.USE_GPU_NMS:
        if not force_cpu:
            return cpu_nms(dets, thresh)
    return cpu_nms(dets, thresh)