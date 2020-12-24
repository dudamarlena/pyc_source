# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notemodel/models/yolo.py
# Compiled at: 2020-04-16 05:33:04
# Size of source mod 2**32: 1493 bytes
import hashlib, numpy as np
from notekeras.model.yolo import YoloBody
from notekeras.utils import read_lines
from notemodel.database import set_weight_path
set_weight_path('/Users/liangtaoniu/workspace/MyDiary/src/tianchi/live/data/weights')
classes = read_lines('coco.names')

def get_md5(weight):
    m = hashlib.md5()
    m.update(weight)
    return m.hexdigest()


def get_anchors():
    anchors = '10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326'
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)


anchors = get_anchors()
yolo_body1 = YoloBody(anchors=anchors, num_classes=(len(classes)))
yolo_body2 = YoloBody(anchors=anchors, num_classes=(len(classes)))
yolo_body1.load_weights('/Users/liangtaoniu/workspace/MyDiary/tmp/models/yolo/configs/yolov3.h5', freeze_body=3)
yolo_body2.load_layer_weights()
for i, layer1 in enumerate(yolo_body1.yolo_model.layers):
    layer2 = yolo_body2.yolo_model.layers[i]
    weight1 = layer1.weights
    weight2 = layer2.weights
    if i in (0, 10, 50, 100, 150, 200, 240):
        print(i)