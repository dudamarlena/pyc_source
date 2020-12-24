# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\models\yolov3\inference.py
# Compiled at: 2020-04-18 02:05:29
# Size of source mod 2**32: 9045 bytes
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont
from xl_tensorflow.models.yolov3.utils import letterbox_image, draw_image
from xl_tensorflow.models.yolov3.model import yolo_body, tiny_yolo_body, yolo_eval, yolo_eval_lite, yolo_efficientnetliteb4_body, yolo_efficientnetliteb1_body
from tensorflow.keras import Input, Model
from xl_tool.xl_io import file_scanning
from .training import body_dict
import tensorflow as tf, pathlib

def _get_anchors(anchors_path):
    anchors_path = os.path.expanduser(anchors_path)
    with open(anchors_path) as (f):
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)


def single_inference_model_lite(model_name, weights, num_classes, image_shape=(480, 640), anchors=None, input_shape=(416, 416), score_threshold=0.6, iou_threshold=0.5):
    """
    专门用于移动端处理，无5维tensor和掩码
    """
    if anchors == None:
        anchors = _get_anchors('./config/yolo_anchors.txt')
    yolo_model = body_dict[model_name](Input(shape=(*input_shape, *(3, ))), len(anchors) // 3, num_classes)
    yolo_model.load_weights(weights)
    boxes_, scores_ = yolo_eval_lite(yolo_model.outputs, anchors, num_classes, image_shape, 20, score_threshold, iou_threshold)
    model = Model(inputs=(yolo_model.inputs), outputs=(boxes_, scores_))
    return model


def tf_saved_model_to_lite(model_path, save_lite_file, input_shape=None, quantize_method=None, allow_custom_ops=False):
    """
    tensorflow saved model转成lite格式
    Args:
        model_path:  saved_model path（include version directory）
        save_lite_file: lite file name(full path)
        input_shape； specified input shape, if none means  [None, 224, 224, 3]
        quantize_method: str, valid value：float16,int,weight
        allow_custom_ops:是否允许自定义算子
    """
    try:
        converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
    except ValueError:
        model = tf.saved_model.load(model_path)
        concrete_func = model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
        concrete_func.inputs[0].set_shape(input_shape if input_shape else [None, 224, 224, 3])
        converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])

    if allow_custom_ops:
        converter.allow_custom_ops = True
        print('允许使用自定义算子')
        converter.target_spec.supported_ops = [tf.lite.OpsSet.SELECT_TF_OPS]
    return pathlib.Path(save_lite_file).write_bytes(converter.convert())


def predict_image(model, image_file, input_shape=(416, 416), xy_order=False):
    image = Image.open(image_file)
    boxed_image = letterbox_image(image, input_shape)
    image_data = np.array(boxed_image, dtype='float32')
    image_data /= 255.0
    image_data = np.expand_dims(image_data, 0)
    out_boxes, out_scores, out_classes = model.predict(image_data)
    try:
        if xy_order:
            out_boxes = [
             map(lambda x: [x[(1, x[0], x[3], x[2])]], list(out_boxes))]
        else:
            out_boxes = list(out_boxes)
        out_scores, out_classes = list(out_scores), list(out_classes)
        return (out_boxes, out_scores, out_classes)
    except IndexError:
        return []