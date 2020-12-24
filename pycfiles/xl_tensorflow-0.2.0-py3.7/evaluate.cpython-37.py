# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\models\yolov3\evaluate.py
# Compiled at: 2020-04-18 02:36:49
# Size of source mod 2**32: 4409 bytes
import os
from .training import body_dict
from .utils import get_anchors, letterbox_image
from tensorflow.keras import Input, Model
from .model import yolo_eval, DEFALT_ANCHORS, yolo_eval_lite
from PIL import Image
import numpy as np

def single_inference_model_serving(model_name, weights, num_classes, image_shape=(416, 416), input_shape=(416, 416), anchors=None, score_threshold=0.1, iou_threshold=0.5, max_detections=20, dynamic_shape=False):
    """
    用于部署在serving端的模型，固定输入尺寸和图片尺寸，会对iou值和置信度进行过滤0.1
    暂时不将尺寸和阙值写入模型，因此返回框的尺寸和位置需要根据图片进行重新调整（与resize方式有关）
    Args:
        image_shape: 宽高
    Returns:
        tf.keras.Model object, 预测图片的绝对值坐标x1,y1,x2,y2
    """
    if anchors == None:
        anchors = DEFALT_ANCHORS
    else:
        yolo_model = body_dict[model_name](Input(shape=(*input_shape, *(3, ))), len(anchors) // 3, num_classes)
        if weights:
            yolo_model.load_weights(weights)
        if dynamic_shape:
            shape_input = Input(shape=(2, ))
            boxes_, scores_, classes_ = yolo_eval((yolo_model.outputs), anchors,
              num_classes, shape_input, max_detections, score_threshold,
              iou_threshold,
              return_xy=True)
            model = Model(inputs=(yolo_model.inputs + [shape_input]), outputs=(boxes_, scores_, classes_))
        else:
            boxes_, scores_, classes_ = yolo_eval((yolo_model.outputs), anchors,
              num_classes, image_shape, max_detections, score_threshold,
              iou_threshold,
              return_xy=True)
        model = Model(inputs=(yolo_model.inputs), outputs=(boxes_, scores_, classes_))
    return model


def single_inference_model_lite(model_name, weights, num_classes, image_shape=(480, 640), anchors=None, input_shape=(416, 416), score_threshold=0.6, iou_threshold=0.5):
    """
    专门用于移动端处理，无5维tensor和掩码
    """
    if anchors == None:
        anchors = DEFALT_ANCHORS
    yolo_model = body_dict[model_name](Input(shape=(*input_shape, *(3, ))), len(anchors) // 3, num_classes)
    yolo_model.load_weights(weights)
    boxes_, scores_ = yolo_eval_lite(yolo_model.outputs, anchors, num_classes, image_shape, 20, score_threshold, iou_threshold)
    model = Model(inputs=(yolo_model.inputs), outputs=(boxes_, scores_))
    return model


def map_evaluate--- This code section failed: ---

 L.  80         0  LOAD_GLOBAL              single_inference_model_serving
                2  LOAD_FAST                'model_name'
                4  LOAD_FAST                'weights'
                6  LOAD_FAST                'num_classes'

 L.  81         8  LOAD_CONST               True
               10  LOAD_CONST               ('model_name', 'weights', 'num_classes', 'dynamic_shape')
               12  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               14  STORE_FAST               'model'

 L.  82        16  SETUP_LOOP          174  'to 174'
               18  LOAD_FAST                'image_files'
               20  GET_ITER         
             22_0  COME_FROM           168  '168'
               22  FOR_ITER            172  'to 172'
               24  STORE_FAST               'image_file'

 L.  83        26  LOAD_GLOBAL              Image
               28  LOAD_METHOD              open
               30  LOAD_FAST                'image_file'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  STORE_FAST               'image'

 L.  84        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              basename
               42  LOAD_FAST                'image_file'
               44  CALL_METHOD_1         1  '1 positional argument'
               46  STORE_FAST               'image_id'

 L.  85        48  LOAD_GLOBAL              letterbox_image
               50  LOAD_FAST                'image'
               52  LOAD_CONST               (416, 416)
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  STORE_FAST               'boxed_image'

 L.  86        58  LOAD_GLOBAL              np
               60  LOAD_ATTR                array
               62  LOAD_FAST                'boxed_image'
               64  LOAD_STR                 'float32'
               66  LOAD_CONST               ('dtype',)
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  STORE_FAST               'image_data'

 L.  87        72  LOAD_FAST                'image_data'
               74  LOAD_CONST               255.0
               76  INPLACE_TRUE_DIVIDE
               78  STORE_FAST               'image_data'

 L.  88        80  LOAD_GLOBAL              np
               82  LOAD_METHOD              expand_dims
               84  LOAD_FAST                'image_data'
               86  LOAD_CONST               0
               88  CALL_METHOD_2         2  '2 positional arguments'
               90  STORE_FAST               'image_data'

 L.  89        92  LOAD_FAST                'model'
               94  LOAD_METHOD              predict
               96  LOAD_FAST                'image_data'
               98  LOAD_GLOBAL              np
              100  LOAD_METHOD              array
              102  LOAD_FAST                'image'
              104  LOAD_ATTR                size
              106  BUILD_LIST_UNPACK_1     1 
              108  LOAD_CONST               None
              110  LOAD_CONST               None
              112  LOAD_CONST               -1
              114  BUILD_SLICE_3         3 
              116  BINARY_SUBSCR    
              118  BUILD_LIST_1          1 
              120  CALL_METHOD_1         1  '1 positional argument'
              122  BUILD_LIST_2          2 
              124  CALL_METHOD_1         1  '1 positional argument'
              126  UNPACK_SEQUENCE_3     3 
              128  STORE_FAST               'boxes_'
              130  STORE_FAST               'scores_'
              132  STORE_FAST               'classes_'

 L.  90       134  LOAD_FAST                'boxes_'
              136  LOAD_CONST               0
              138  BINARY_SUBSCR    
              140  LOAD_FAST                'scores_'
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  LOAD_FAST                'classes_'
              148  LOAD_CONST               0
              150  BINARY_SUBSCR    
              152  ROT_THREE        
              154  ROT_TWO          
              156  STORE_FAST               'boxes_'
              158  STORE_FAST               'scores_'
              160  STORE_FAST               'classes_'

 L.  91       162  LOAD_FAST                'scores_'
              164  LOAD_CONST               0
              166  BINARY_SUBSCR    
              168  POP_JUMP_IF_FALSE    22  'to 22'

 L.  93       170  JUMP_BACK            22  'to 22'
              172  POP_BLOCK        
            174_0  COME_FROM_LOOP       16  '16'

Parse error at or near `POP_BLOCK' instruction at offset 172