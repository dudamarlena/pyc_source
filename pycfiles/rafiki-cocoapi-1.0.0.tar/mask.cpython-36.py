# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kammeyer/src/cocoapi/PythonAPI/pycocotools/mask.py
# Compiled at: 2018-03-11 01:01:11
# Size of source mod 2**32: 4591 bytes
__author__ = 'tsungyi'
import pycocotools._mask as _mask
iou = _mask.iou
merge = _mask.merge
frPyObjects = _mask.frPyObjects

def encode(bimask):
    if len(bimask.shape) == 3:
        return _mask.encode(bimask)
    if len(bimask.shape) == 2:
        h, w = bimask.shape
        return _mask.encode(bimask.reshape((h, w, 1), order='F'))[0]


def decode(rleObjs):
    if type(rleObjs) == list:
        return _mask.decode(rleObjs)
    else:
        return _mask.decode([rleObjs])[:, :, 0]


def area(rleObjs):
    if type(rleObjs) == list:
        return _mask.area(rleObjs)
    else:
        return _mask.area([rleObjs])[0]


def toBbox(rleObjs):
    if type(rleObjs) == list:
        return _mask.toBbox(rleObjs)
    else:
        return _mask.toBbox([rleObjs])[0]