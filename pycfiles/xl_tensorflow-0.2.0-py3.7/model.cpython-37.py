# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\models\yolov3\model.py
# Compiled at: 2020-04-18 02:07:21
# Size of source mod 2**32: 48328 bytes
from functools import wraps
import numpy as np, tensorflow as tf
import tensorflow.keras as K
from tensorflow.keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from ..efficientnet import EfficientNetB4, EfficientNetB3, EfficientNetLiteB4, mb_conv_block, BlockArgs, get_swish, EfficientNetLiteB1, EfficientNetB0
from .utils import compose
DEFALT_ANCHORS = np.array([[10.0, 13.0],
 [
  16.0, 30.0],
 [
  33.0, 23.0],
 [
  30.0, 61.0],
 [
  62.0, 45.0],
 [
  59.0, 119.0],
 [
  116.0, 90.0],
 [
  156.0, 198.0],
 [
  373.0, 326.0]],
  dtype='float')

def output_wrapper(func):
    """将backbone的输出形状(batch,anchor,anchor,3*(5+num_classes))
     reshape为(batch,anchor,anchor,3，(5+num_classes)),主要用于自定义的yololoss"""

    @wraps(func)
    def wrapper(inputs, num_anchors, num_classes, reshape_y=False):
        model = func(inputs, num_anchors, num_classes)
        if reshape_y:
            y1, y2, y3 = model.outputs
            y1 = tf.keras.layers.Reshape((y1.shape[1], y1.shape[2], num_anchors, num_classes + 5))(y1)
            y2 = tf.keras.layers.Reshape((y2.shape[1], y2.shape[2], num_anchors, num_classes + 5))(y2)
            y3 = tf.keras.layers.Reshape((y3.shape[1], y3.shape[2], num_anchors, num_classes + 5))(y3)
            model = Model(inputs, [y1, y2, y3])
        return model

    return wrapper


@wraps(Conv2D)
def DarknetConv2D(*args, **kwargs):
    """Wrapper to set Darknet parameters for Convolution2D."""
    darknet_conv_kwargs = {'kernel_regularizer': l2(0.0005)}
    darknet_conv_kwargs['padding'] = 'valid' if kwargs.get('strides') == (2, 2) else 'same'
    darknet_conv_kwargs.update(kwargs)
    return Conv2D(*args, **darknet_conv_kwargs)


def DarknetConv2D_BN_Leaky(*args, **kwargs):
    """Darknet Convolution2D followed by BatchNormalization and LeakyReLU."""
    no_bias_kwargs = {'use_bias': False}
    no_bias_kwargs.update(kwargs)
    return compose(DarknetConv2D(*args, **no_bias_kwargs), BatchNormalization(), LeakyReLU(alpha=0.1))


def resblock_body(x, num_filters, num_blocks):
    """A series of resblocks starting with a downsampling Convolution2D"""
    x = ZeroPadding2D(((1, 0), (1, 0)))(x)
    x = DarknetConv2D_BN_Leaky(num_filters, (3, 3), strides=(2, 2))(x)
    for i in range(num_blocks):
        y = compose(DarknetConv2D_BN_Leaky(num_filters // 2, (1, 1)), DarknetConv2D_BN_Leaky(num_filters, (3,
                                                                                                           3)))(x)
        x = Add()([x, y])

    return x


def darknet_body(x):
    """Darknent body having 52 Convolution2D layers"""
    x = DarknetConv2D_BN_Leaky(32, (3, 3))(x)
    x = resblock_body(x, 64, 1)
    x = resblock_body(x, 128, 2)
    x = resblock_body(x, 256, 8)
    x = resblock_body(x, 512, 8)
    x = resblock_body(x, 1024, 4)
    return x


def make_last_layers(x, num_filters, out_filters):
    """6 Conv2D_BN_Leaky layers followed by a Conv2D_linear layer"""
    x = compose(DarknetConv2D_BN_Leaky(num_filters, (1, 1)), DarknetConv2D_BN_Leaky(num_filters * 2, (3,
                                                                                                      3)), DarknetConv2D_BN_Leaky(num_filters, (1,
                                                                                                                                                1)), DarknetConv2D_BN_Leaky(num_filters * 2, (3,
                                                                                                                                                                                              3)), DarknetConv2D_BN_Leaky(num_filters, (1,
                                                                                                                                                                                                                                        1)))(x)
    y = compose(DarknetConv2D_BN_Leaky(num_filters * 2, (3, 3)), DarknetConv2D(out_filters, (1,
                                                                                             1)))(x)
    return (x, y)


@output_wrapper
def yolo_body(inputs, num_anchors, num_classes):
    """Create YOLO_V3 model CNN body in Keras."""
    darknet = Model(inputs, darknet_body(inputs))
    x, y1 = make_last_layers(darknet.output, 512, num_anchors * (num_classes + 5))
    x = compose(DarknetConv2D_BN_Leaky(256, (1, 1)), UpSampling2D(2))(x)
    x = Concatenate()([x, darknet.layers[152].output])
    x, y2 = make_last_layers(x, 256, num_anchors * (num_classes + 5))
    x = compose(DarknetConv2D_BN_Leaky(128, (1, 1)), UpSampling2D(2))(x)
    x = Concatenate()([x, darknet.layers[92].output])
    x, y3 = make_last_layers(x, 128, num_anchors * (num_classes + 5))
    return Model(inputs, [y1, y2, y3])


def make_last_layers_efficientnet(x, block_args, prefix):
    num_filters = block_args.input_filters * block_args.expand_ratio
    x = compose(tf.keras.layers.Conv2D(num_filters, kernel_size=1,
      padding='same',
      use_bias=False), tf.keras.layers.BatchNormalization(epsilon=0.001,
      momentum=0.9), tf.keras.layers.ReLU(6.0), lambda x: mb_conv_block(x, block_args, activation=(get_swish()), drop_rate=0.2, prefix=('1_' + prefix)), tf.keras.layers.Conv2D(num_filters, kernel_size=1,
      padding='same',
      use_bias=False), tf.keras.layers.BatchNormalization(epsilon=0.001,
      momentum=0.9), tf.keras.layers.ReLU(6.0), lambda x: mb_conv_block(x, block_args, activation=(get_swish()), drop_rate=0.2, prefix=('2_' + prefix)), tf.keras.layers.Conv2D(num_filters, kernel_size=1,
      padding='same',
      use_bias=False), tf.keras.layers.BatchNormalization(epsilon=0.001,
      momentum=0.9), tf.keras.layers.ReLU(6.0))(x)
    y = compose(lambda x: mb_conv_block(x, block_args, activation=(get_swish()), drop_rate=0.2, prefix=('3_' + prefix)), tf.keras.layers.Conv2D((block_args.output_filters), kernel_size=1,
      padding='same',
      use_bias=False))(x)
    return (x, y)


@output_wrapper
def yolo_efficientnetb4_body(inputs, number_anchors, number_classes):
    block_args = BlockArgs(kernel_size=3, num_repeat=1,
      input_filters=512,
      output_filters=(number_anchors * (number_classes + 5)),
      expand_ratio=1,
      id_skip=True,
      se_ratio=0.25,
      strides=[
     1, 1])
    backbone = EfficientNetB4(include_top=False, input_tensor=inputs, weights=None)
    x, y1 = make_last_layers_efficientnet(backbone.output, block_args, 'y1_')
    x = compose(tf.keras.layers.Conv2D(256, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_20_conv'), tf.keras.layers.BatchNormalization(momentum=0.9, name='block_20_BN'), tf.keras.layers.ReLU(6.0, name='block_20_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=256)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block6a_expand_activation').output])
    x, y2 = make_last_layers_efficientnet(x, block_args, 'y2_')
    x = compose(tf.keras.layers.Conv2D(128, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_24_conv'), tf.keras.layers.BatchNormalization(momentum=0.9,
      name='block_24_BN'), tf.keras.layers.ReLU(6.0, name='block_24_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=128)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block4a_expand_activation').output])
    x, y3 = make_last_layers_efficientnet(x, block_args, 'y3_')
    return Model(inputs, [y1, y2, y3])


@output_wrapper
def yolo_efficientnetliteb4_body(inputs, number_anchors, number_classes):
    block_args = BlockArgs(kernel_size=3, num_repeat=1,
      input_filters=512,
      output_filters=(number_anchors * (number_classes + 5)),
      expand_ratio=1,
      id_skip=True,
      se_ratio=None,
      strides=[
     1, 1])
    backbone = EfficientNetLiteB4(include_top=False, input_tensor=inputs, weights=None)
    x, y1 = make_last_layers_efficientnet(backbone.output, block_args, 'y1_')
    x = compose(tf.keras.layers.Conv2D(256, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_20_conv'), tf.keras.layers.BatchNormalization(momentum=0.9, name='block_20_BN'), tf.keras.layers.ReLU(6.0, name='block_20_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=256)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block6a_expand_activation').output])
    x, y2 = make_last_layers_efficientnet(x, block_args, 'y2_')
    x = compose(tf.keras.layers.Conv2D(128, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_24_conv'), tf.keras.layers.BatchNormalization(momentum=0.9,
      name='block_24_BN'), tf.keras.layers.ReLU(6.0, name='block_24_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=128)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block4a_expand_activation').output])
    x, y3 = make_last_layers_efficientnet(x, block_args, 'y3_')
    return Model(inputs, [y1, y2, y3])


@output_wrapper
def yolo_efficientnetliteb1_body(inputs, number_anchors, number_classes):
    block_args = BlockArgs(kernel_size=3, num_repeat=1,
      input_filters=512,
      output_filters=(number_anchors * (number_classes + 5)),
      expand_ratio=1,
      id_skip=True,
      se_ratio=None,
      strides=[
     1, 1])
    backbone = EfficientNetLiteB1(include_top=False, input_tensor=inputs, weights=None)
    x, y1 = make_last_layers_efficientnet(backbone.output, block_args, 'y1_')
    x = compose(tf.keras.layers.Conv2D(256, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_20_conv'), tf.keras.layers.BatchNormalization(momentum=0.9, name='block_20_BN'), tf.keras.layers.ReLU(6.0, name='block_20_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=256)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block6a_expand_activation').output])
    x, y2 = make_last_layers_efficientnet(x, block_args, 'y2_')
    x = compose(tf.keras.layers.Conv2D(128, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_24_conv'), tf.keras.layers.BatchNormalization(momentum=0.9,
      name='block_24_BN'), tf.keras.layers.ReLU(6.0, name='block_24_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=128)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block4a_expand_activation').output])
    x, y3 = make_last_layers_efficientnet(x, block_args, 'y3_')
    return Model(inputs, [y1, y2, y3])


@output_wrapper
def yolo_efficientnetb3_body(inputs, number_anchors, number_classes):
    block_args = BlockArgs(kernel_size=3, num_repeat=1,
      input_filters=512,
      output_filters=(number_anchors * (number_classes + 5)),
      expand_ratio=1,
      id_skip=True,
      se_ratio=0.25,
      strides=[
     1, 1])
    backbone = EfficientNetB3(include_top=False, input_tensor=inputs, weights=None)
    x, y1 = make_last_layers_efficientnet(backbone.output, block_args, 'y1_')
    x = compose(tf.keras.layers.Conv2D(256, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_20_conv'), tf.keras.layers.BatchNormalization(momentum=0.9, name='block_20_BN'), tf.keras.layers.ReLU(6.0, name='block_20_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=256)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block6a_expand_activation').output])
    x, y2 = make_last_layers_efficientnet(x, block_args, 'y2_')
    x = compose(tf.keras.layers.Conv2D(128, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_24_conv'), tf.keras.layers.BatchNormalization(momentum=0.9,
      name='block_24_BN'), tf.keras.layers.ReLU(6.0, name='block_24_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=128)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block4a_expand_activation').output])
    x, y3 = make_last_layers_efficientnet(x, block_args, 'y3_')
    return Model(inputs, [y1, y2, y3])


@output_wrapper
def yolo_efficientnetb0_body(inputs, number_anchors, number_classes):
    block_args = BlockArgs(kernel_size=3, num_repeat=1,
      input_filters=512,
      output_filters=(number_anchors * (number_classes + 5)),
      expand_ratio=1,
      id_skip=True,
      se_ratio=0.25,
      strides=[
     1, 1])
    backbone = EfficientNetB0(include_top=False, input_tensor=inputs, weights=None)
    x, y1 = make_last_layers_efficientnet(backbone.output, block_args, 'y1_')
    x = compose(tf.keras.layers.Conv2D(256, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_20_conv'), tf.keras.layers.BatchNormalization(momentum=0.9, name='block_20_BN'), tf.keras.layers.ReLU(6.0, name='block_20_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=256)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block6a_expand_activation').output])
    x, y2 = make_last_layers_efficientnet(x, block_args, 'y2_')
    x = compose(tf.keras.layers.Conv2D(128, kernel_size=1,
      padding='same',
      use_bias=False,
      name='block_24_conv'), tf.keras.layers.BatchNormalization(momentum=0.9,
      name='block_24_BN'), tf.keras.layers.ReLU(6.0, name='block_24_relu6'), tf.keras.layers.UpSampling2D(2))(x)
    block_args = block_args._replace(input_filters=128)
    x = tf.keras.layers.Concatenate()([
     x, backbone.get_layer('block4a_expand_activation').output])
    x, y3 = make_last_layers_efficientnet(x, block_args, 'y3_')
    return Model(inputs, [y1, y2, y3])


def tiny_yolo_body(inputs, num_anchors, num_classes):
    """Create Tiny YOLO_v3 model CNN body in keras."""
    x1 = compose(DarknetConv2D_BN_Leaky(16, (3, 3)), MaxPooling2D(pool_size=(2, 2), strides=(2,
                                                                                             2), padding='same'), DarknetConv2D_BN_Leaky(32, (3,
                                                                                                                                              3)), MaxPooling2D(pool_size=(2,
                                                                                                                                                                           2), strides=(2,
                                                                                                                                                                                        2), padding='same'), DarknetConv2D_BN_Leaky(64, (3,
                                                                                                                                                                                                                                         3)), MaxPooling2D(pool_size=(2,
                                                                                                                                                                                                                                                                      2), strides=(2,
                                                                                                                                                                                                                                                                                   2), padding='same'), DarknetConv2D_BN_Leaky(128, (3,
                                                                                                                                                                                                                                                                                                                                     3)), MaxPooling2D(pool_size=(2,
                                                                                                                                                                                                                                                                                                                                                                  2), strides=(2,
                                                                                                                                                                                                                                                                                                                                                                               2), padding='same'), DarknetConv2D_BN_Leaky(256, (3,
                                                                                                                                                                                                                                                                                                                                                                                                                                 3)))(inputs)
    x2 = compose(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'), DarknetConv2D_BN_Leaky(512, (3,
                                                                                                              3)), MaxPooling2D(pool_size=(2,
                                                                                                                                           2), strides=(1,
                                                                                                                                                        1), padding='same'), DarknetConv2D_BN_Leaky(1024, (3,
                                                                                                                                                                                                           3)), DarknetConv2D_BN_Leaky(256, (1,
                                                                                                                                                                                                                                             1)))(x1)
    y1 = compose(DarknetConv2D_BN_Leaky(512, (3, 3)), DarknetConv2D(num_anchors * (num_classes + 5), (1,
                                                                                                      1)))(x2)
    x2 = compose(DarknetConv2D_BN_Leaky(128, (1, 1)), UpSampling2D(2))(x2)
    y2 = compose(Concatenate(), DarknetConv2D_BN_Leaky(256, (3, 3)), DarknetConv2D(num_anchors * (num_classes + 5), (1,
                                                                                                                     1)))([x2, x1])
    return Model(inputs, [y1, y2])


def yolo_head_lite(feats, anchors, num_classes, input_shape, calc_loss=False):
    """计算grid和预测box的坐标和长宽
        Args:
            feats, 即yolobody的输出，未经过未经过sigmoid函数处理,输出为batch 26,26,255
            anchors: anchor box
            num_classes: number class
            input_shape: input shape of yolobody, like 416,320
            calc_loss: where to caculate loss, used for training
        Returns:
            box_xy  相对整图的大小，0至1
            box_wh   相对input shape即416的大小，0，+无穷大
            box_confidence
            box_class_probs
    """
    num_anchors = len(anchors)
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, num_anchors, 2])
    grid_shape = K.shape(feats)[1:3]
    grid_y = K.tile(K.reshape(K.arange(0, stop=(grid_shape[0])), [-1, 1, 1, 1]), [
     1, grid_shape[1], 1, 1])
    grid_x = K.tile(K.reshape(K.arange(0, stop=(grid_shape[1])), [1, -1, 1, 1]), [
     grid_shape[0], 1, 1, 1])
    grid = K.concatenate([grid_x, grid_y])
    grid = K.cast(grid, K.dtype(feats))
    feats = K.reshape(feats, [grid_shape[0], grid_shape[1], num_anchors, num_classes + 5])
    box_xy = (K.sigmoid(feats[:, :, :, :2]) + grid) / K.cast(grid_shape[::-1], K.dtype(feats))
    box_wh = K.exp(feats[:, :, :, 2:4]) * anchors_tensor / K.cast(input_shape[::-1], K.dtype(feats))
    box_confidence = K.sigmoid(feats[:, :, :, 4:5])
    box_class_probs = K.sigmoid(feats[:, :, :, 5:])
    if calc_loss == True:
        return (
         grid, feats, box_xy, box_wh)
    return (
     box_xy, box_wh, box_confidence, box_class_probs)


def yolo_head(feats, anchors, num_classes, input_shape, calc_loss=False):
    """计算grid和预测box的坐标和长宽
        Args:
            feats, 即yolobody的输出，未经过未经过sigmoid函数处理,输出为batch 26,26,255
            anchors: anchor box
            num_classes: number class
            input_shape: input shape of yolobody, like 416,320
            calc_loss: where to caculate loss, used for training
        Returns:
            box_xy  相对整图的大小，0至1,shape like (batch, gridx,gridy,3,2)
            box_wh   相对input shape即416的大小，0，+无穷大
            box_confidence
            box_class_probs
    """
    num_anchors = len(anchors)
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])
    grid_shape = K.shape(feats)[1:3]
    grid_y = K.tile(K.reshape(K.arange(0, stop=(grid_shape[0])), [-1, 1, 1, 1]), [
     1, grid_shape[1], 1, 1])
    grid_x = K.tile(K.reshape(K.arange(0, stop=(grid_shape[1])), [1, -1, 1, 1]), [
     grid_shape[0], 1, 1, 1])
    grid = K.concatenate([grid_x, grid_y])
    grid = K.cast(grid, K.dtype(feats))
    feats = K.reshape(feats, [-1, grid_shape[0], grid_shape[1], num_anchors, num_classes + 5])
    box_xy = (K.sigmoid(feats[..., :2]) + grid) / K.cast(grid_shape[::-1], K.dtype(feats))
    box_wh = K.exp(feats[..., 2:4]) * anchors_tensor / K.cast(input_shape[::-1], K.dtype(feats))
    box_confidence = K.sigmoid(feats[..., 4:5])
    box_class_probs = K.sigmoid(feats[..., 5:])
    if calc_loss == True:
        return (
         grid, feats, box_xy, box_wh)
    return (
     box_xy, box_wh, box_confidence, box_class_probs)


def yolo_head_sp(feats, anchors, num_classes, input_shape, grid_shape, calc_loss=False):
    """计算grid和预测box的坐标和长宽(专门用于指定的tf loss类)
        Args:
            feats, 即yolobody的输出，未经过未经过sigmoid函数处理,输出为batch 26,26,3,85
            anchors: anchor box
            num_classes: number class
            input_shape: input shape of yolobody, like 416,320
            calc_loss: where to caculate loss, used for training
        Returns:
            box_xy  相对整图的大小，0至1,shape like (batch, gridx,gridy,3,2)
            box_wh   相对input shape即416的大小，0，+无穷大
            box_confidence
            box_class_probs
    """
    num_anchors = len(anchors)
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])
    grid_shape = K.shape(feats)[1:3]
    grid_y = K.tile(K.reshape(K.arange(0, stop=(grid_shape[0])), [-1, 1, 1, 1]), [
     1, grid_shape[1], 1, 1])
    grid_x = K.tile(K.reshape(K.arange(0, stop=(grid_shape[1])), [1, -1, 1, 1]), [
     grid_shape[0], 1, 1, 1])
    grid = K.concatenate([grid_x, grid_y])
    grid = K.cast(grid, K.dtype(feats))
    box_xy = (K.sigmoid(feats[..., :2]) + grid) / K.cast(grid_shape[::-1], K.dtype(feats))
    box_wh = K.exp(feats[..., 2:4]) * anchors_tensor / K.cast(input_shape[::-1], K.dtype(feats))
    box_confidence = K.sigmoid(feats[..., 4:5])
    box_class_probs = K.sigmoid(feats[..., 5:])
    if calc_loss == True:
        return (
         grid, feats, box_xy, box_wh)
    return (
     box_xy, box_wh, box_confidence, box_class_probs)


def yolo_correct_boxes_lite(box_xy, box_wh, input_shape, image_shape):
    """
    获取正确的box坐标，相对整图的坐标
    Args:
        box_xy  xy坐标值
        box_wh  宽高
        input_shape  模型输入尺寸
        image_shape  图片原始尺寸，用于还原重建坐标，Height * Width

    """
    box_yx = box_xy[:, :, :, ::-1]
    box_hw = box_wh[:, :, :, ::-1]
    input_shape = K.cast(input_shape, K.dtype(box_yx))
    image_shape = K.cast(image_shape, K.dtype(box_yx))
    new_shape = K.round(image_shape * K.min(input_shape / image_shape))
    offset = (input_shape - new_shape) / 2.0 / input_shape
    scale = input_shape / new_shape
    box_yx = (box_yx - offset) * scale
    box_hw *= scale
    box_mins = box_yx - box_hw / 2.0
    box_maxes = box_yx + box_hw / 2.0
    boxes = K.concatenate([
     box_mins[:, :, :, 0:1],
     box_mins[:, :, :, 1:2],
     box_maxes[:, :, :, 0:1],
     box_maxes[:, :, :, 1:2]])
    boxes *= K.concatenate([image_shape, image_shape])
    return boxes


def yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape):
    """
    获取正确的box坐标，相对整图的坐标
    Args:
        box_xy  xy坐标值
        box_wh  宽高
        input_shape  模型输入尺寸
        image_shape  图片原始尺寸，用于还原重建坐标，Height * Width

    """
    box_yx = box_xy[..., ::-1]
    box_hw = box_wh[..., ::-1]
    input_shape = K.cast(input_shape, K.dtype(box_yx))
    image_shape = K.cast(image_shape, K.dtype(box_yx))
    new_shape = K.round(image_shape * K.min(input_shape / image_shape))
    offset = (input_shape - new_shape) / 2.0 / input_shape
    scale = input_shape / new_shape
    box_yx = (box_yx - offset) * scale
    box_hw *= scale
    box_mins = box_yx - box_hw / 2.0
    box_maxes = box_yx + box_hw / 2.0
    boxes = K.concatenate([
     box_mins[..., 0:1],
     box_mins[..., 1:2],
     box_maxes[..., 0:1],
     box_maxes[..., 1:2]])
    boxes *= K.concatenate([image_shape, image_shape])
    return boxes


def yolo_boxes_and_scores(feats, anchors, num_classes, input_shape, image_shape):
    """Process Conv layer output"""
    box_xy, box_wh, box_confidence, box_class_probs = yolo_head(feats, anchors, num_classes, input_shape)
    boxes = yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape)
    boxes = K.reshape(boxes, [-1, 4])
    box_scores = box_confidence * box_class_probs
    box_scores = K.reshape(box_scores, [-1, num_classes])
    return (boxes, box_scores)


def yolo_boxes_and_scores_lite(feats, anchors, num_classes, input_shape, image_shape):
    """Process Conv layer output"""
    box_xy, box_wh, box_confidence, box_class_probs = yolo_head_lite(feats, anchors, num_classes, input_shape)
    boxes = yolo_correct_boxes_lite(box_xy, box_wh, input_shape, image_shape)
    boxes = K.reshape(boxes, [-1, 4])
    box_scores = box_confidence * box_class_probs
    box_scores = K.reshape(box_scores, [-1, num_classes])
    return (boxes, box_scores)


def yolo_eval(yolo_outputs, anchors, num_classes, image_shape, max_boxes=20, score_threshold=0.6, iou_threshold=0.5, return_xy=True):
    """Evaluate YOLO model on given input and return filtered boxes.
    只适用于一张图片的处理，不适合批处理
    Args:
        image_shape: 原始输入图片尺寸, 高X宽
    Returns:
        boxes,其中box格式为[y1,x1,y2,x2]
    """
    num_layers = len(yolo_outputs)
    anchor_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]] if num_layers == 3 else [[3, 4, 5], [1, 2, 3]]
    input_shape = K.shape(yolo_outputs[0])[1:3] * 32
    boxes = []
    box_scores = []
    for l in range(num_layers):
        _boxes, _box_scores = yolo_boxes_and_scores(yolo_outputs[l], anchors[anchor_mask[l]], num_classes, input_shape, image_shape)
        boxes.append(_boxes)
        box_scores.append(_box_scores)

    boxes = K.concatenate(boxes, axis=0)
    box_scores = K.concatenate(box_scores, axis=0)
    mask = box_scores >= score_threshold
    max_boxes_tensor = K.constant(max_boxes, dtype='int32')
    boxes_ = []
    scores_ = []
    classes_ = []
    for c in range(num_classes):
        class_boxes = tf.boolean_mask(boxes, mask[:, c])
        class_box_scores = tf.boolean_mask(box_scores[:, c], mask[:, c])
        nms_index = tf.image.non_max_suppression(class_boxes,
          class_box_scores, max_boxes_tensor, iou_threshold=iou_threshold)
        class_boxes = K.gather(class_boxes, nms_index)
        class_box_scores = K.gather(class_box_scores, nms_index)
        classes = K.ones_like(class_box_scores, 'int32') * c
        boxes_.append(class_boxes)
        scores_.append(class_box_scores)
        classes_.append(classes)

    if return_xy:
        boxes_ = K.concatenate([
         boxes_[..., 1:2],
         boxes_[..., 0:1],
         boxes_[..., 3:],
         boxes_[..., 2:3]])
    boxes_ = K.expand_dims(K.concatenate(boxes_, axis=0), axis=0)
    scores_ = K.expand_dims(K.concatenate(scores_, axis=0), axis=0)
    classes_ = K.expand_dims(K.concatenate(classes_, axis=0), axis=0)
    return (
     boxes_, scores_, classes_)


def yolo_eval_lite(yolo_outputs, anchors, num_classes, image_shape, return_xy=True):
    """Todo 未测试和完善
    """
    num_layers = len(yolo_outputs)
    anchor_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]] if num_layers == 3 else [[3, 4, 5], [1, 2, 3]]
    input_shape = K.shape(yolo_outputs[0])[1:3] * 32
    boxes = []
    box_scores = []
    for l in range(num_layers):
        _boxes, _box_scores = yolo_boxes_and_scores_lite(yolo_outputs[l], anchors[anchor_mask[l]], num_classes, input_shape, image_shape)
        boxes.append(_boxes)
        box_scores.append(_box_scores)

    boxes = K.concatenate(boxes, axis=0)
    if return_xy:
        boxes = K.concatenate([
         boxes[..., 1:2],
         boxes[..., 0:1],
         boxes[..., 3:],
         boxes[..., 2:3]])
    box_scores = K.concatenate(box_scores, axis=0)
    box_scores = tf.transpose(box_scores)
    return (K.expand_dims(boxes, 0), K.expand_dims(box_scores, 0))


def box_iou(b1, b2):
    """Return iou tensor, 即所有预测box与真实box的iou值
    Parameters
    ----------
    b1: predict box tensor, shape=(i1,...,iN, 4), xywh, shape like 26*26*3*4
    b2: true box tensor, tensor, shape=(j, 4), xywh, j mean the real box number for image
    Returns
    -------
    iou: tensor, shape=(i1,...,iN, j)
    """
    b1 = K.expand_dims(b1, -2)
    b1_xy = b1[..., :2]
    b1_wh = b1[..., 2:4]
    b1_wh_half = b1_wh / 2.0
    b1_mins = b1_xy - b1_wh_half
    b1_maxes = b1_xy + b1_wh_half
    b2 = K.expand_dims(b2, 0)
    b2_xy = b2[..., :2]
    b2_wh = b2[..., 2:4]
    b2_wh_half = b2_wh / 2.0
    b2_mins = b2_xy - b2_wh_half
    b2_maxes = b2_xy + b2_wh_half
    intersect_mins = K.maximum(b1_mins, b2_mins)
    intersect_maxes = K.minimum(b1_maxes, b2_maxes)
    intersect_wh = K.maximum(intersect_maxes - intersect_mins, 0.0)
    intersect_area = intersect_wh[(Ellipsis, 0)] * intersect_wh[(Ellipsis, 1)]
    b1_area = b1_wh[(Ellipsis, 0)] * b1_wh[(Ellipsis, 1)]
    b2_area = b2_wh[(Ellipsis, 0)] * b2_wh[(Ellipsis, 1)]
    iou = intersect_area / (b1_area + b2_area - intersect_area)
    return iou


def yolo_loss(data, anchors, num_classes, ignore_thresh=0.5, print_loss=True):
    """Return yolo_loss tensor
    Parameters
    ----------
    yolo_outputs: list of tensor, the output of yolo_body or tiny_yolo_body
    y_true: list of array, the output of preprocess_true_boxes
    anchors: array, shape=(N, 2), 2 refer to wh, N refer to number of achors
    num_classes: integer
    ignore_thresh: float, the iou threshold whether to ignore object confidence loss
    Returns
    -------
    loss: tensor, shape=(1,)
    """
    num_layers = len(anchors) // 3
    yolo_outputs = data[:num_layers]
    y_true = data[num_layers:]
    anchor_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]] if num_layers == 3 else [[3, 4, 5], [1, 2, 3]]
    input_shape = K.cast(K.shape(yolo_outputs[0])[1:3] * 32, K.dtype(y_true[0]))
    grid_shapes = [K.cast(K.shape(yolo_outputs[l])[1:3], K.dtype(y_true[0])) for l in range(num_layers)]
    loss = 0
    m = K.shape(yolo_outputs[0])[0]
    mf = K.cast(m, K.dtype(yolo_outputs[0]))
    for l in range(num_layers):
        object_mask = y_true[l][..., 4:5]
        true_class_probs = y_true[l][..., 5:]
        grid, raw_pred, pred_xy, pred_wh = yolo_head((yolo_outputs[l]), (anchors[anchor_mask[l]]),
          num_classes, input_shape, calc_loss=True)
        pred_box = K.concatenate([pred_xy, pred_wh])
        raw_true_xy = y_true[l][..., :2] * grid_shapes[l][::-1] - grid
        raw_true_wh = K.log(y_true[l][..., 2:4] / anchors[anchor_mask[l]] * input_shape[::-1])
        raw_true_wh = K.switch(object_mask, raw_true_wh, K.zeros_like(raw_true_wh))
        box_loss_scale = 2 - y_true[l][..., 2:3] * y_true[l][..., 3:4]
        ignore_mask = tf.TensorArray((K.dtype(y_true[0])), size=1, dynamic_size=True)
        object_mask_bool = K.cast(object_mask, 'bool')

        def loop_body(b, ignore_mask):
            true_box = tf.boolean_mask(y_true[l][b, ..., 0:4], object_mask_bool[(b, ..., 0)])
            iou = box_iou(pred_box[b], true_box)
            best_iou = K.max(iou, axis=(-1))
            ignore_mask = ignore_mask.write(b, K.cast(best_iou < ignore_thresh, K.dtype(true_box)))
            return (b + 1, ignore_mask)

        _, ignore_mask = tf.while_loop(lambda b, *args: b < m, loop_body, [0, ignore_mask])
        ignore_mask = ignore_mask.stack()
        ignore_mask = K.expand_dims(ignore_mask, -1)
        xy_loss = object_mask * box_loss_scale * K.binary_crossentropy(raw_true_xy, (raw_pred[..., 0:2]), from_logits=True)
        wh_loss = object_mask * box_loss_scale * 0.5 * K.square(raw_true_wh - raw_pred[..., 2:4])
        confidence_loss = object_mask * K.binary_crossentropy(object_mask, (raw_pred[..., 4:5]), from_logits=True) + (1 - object_mask) * K.binary_crossentropy(object_mask, (raw_pred[..., 4:5]), from_logits=True) * ignore_mask
        class_loss = object_mask * K.binary_crossentropy(true_class_probs, (raw_pred[..., 5:]), from_logits=True)
        xy_loss = K.sum(xy_loss) / mf
        wh_loss = K.sum(wh_loss) / mf
        confidence_loss = K.sum(confidence_loss) / mf
        class_loss = K.sum(class_loss) / mf
        loss += xy_loss + wh_loss + confidence_loss + class_loss
        if print_loss:
            loss = tf.compat.v1.Print(loss, [loss, xy_loss, wh_loss, confidence_loss, class_loss, K.sum(ignore_mask)], message='loss: ')

    loss = tf.expand_dims(loss, 0)
    return loss


def do_giou_calculate(b1, b2, mode='giou'):
    """
    Args:
        b1: bounding box. The coordinates of the each bounding box in boxes are
        encoded as [y_min, x_min, y_max, x_max].
        b2: the other bounding box. The coordinates of the each bounding box
        in boxes are encoded as [y_min, x_min, y_max, x_max].
        mode: one of ['giou', 'iou'],
        decided to calculate giou loss or iou loss.
    Returns:
        GIoU loss float `Tensor`.
    """
    zero = tf.convert_to_tensor(0.0, b1.dtype)
    b1_ymin, b1_xmin, b1_ymax, b1_xmax = tf.unstack(b1, 4, axis=(-1))
    b2_ymin, b2_xmin, b2_ymax, b2_xmax = tf.unstack(b2, 4, axis=(-1))
    b1_width = tf.maximum(zero, b1_xmax - b1_xmin)
    b1_height = tf.maximum(zero, b1_ymax - b1_ymin)
    b2_width = tf.maximum(zero, b2_xmax - b2_xmin)
    b2_height = tf.maximum(zero, b2_ymax - b2_ymin)
    b1_area = b1_width * b1_height
    b2_area = b2_width * b2_height
    intersect_ymin = tf.maximum(b1_ymin, b2_ymin)
    intersect_xmin = tf.maximum(b1_xmin, b2_xmin)
    intersect_ymax = tf.minimum(b1_ymax, b2_ymax)
    intersect_xmax = tf.minimum(b1_xmax, b2_xmax)
    intersect_width = tf.maximum(zero, intersect_xmax - intersect_xmin)
    intersect_height = tf.maximum(zero, intersect_ymax - intersect_ymin)
    intersect_area = intersect_width * intersect_height
    union_area = b1_area + b2_area - intersect_area
    iou = tf.math.divide_no_nan(intersect_area, union_area)
    if mode == 'iou':
        return iou
    enclose_ymin = tf.minimum(b1_ymin, b2_ymin)
    enclose_xmin = tf.minimum(b1_xmin, b2_xmin)
    enclose_ymax = tf.maximum(b1_ymax, b2_ymax)
    enclose_xmax = tf.maximum(b1_xmax, b2_xmax)
    enclose_width = tf.maximum(zero, enclose_xmax - enclose_xmin)
    enclose_height = tf.maximum(zero, enclose_ymax - enclose_ymin)
    enclose_area = enclose_width * enclose_height
    giou = iou - tf.math.divide_no_nan(enclose_area - union_area, enclose_area)
    return giou


class YoloLoss(tf.keras.losses.Loss):
    __doc__ = 'yolo损失函数\n    定义模型为标准输出，把yolo head写入模型里面（即还原成相对坐标形式）\n    不把损失函数写入模型里面\n    '
    defalt_anchors = DEFALT_ANCHORS

    def __init__(self, scale_stage, input_shape, num_class, giou_loss=False, anchors=None, ignore_thresh=0.5, print_loss=False):
        """
        计算每个stage的损失
        Args:
            scale_stage: ie 1: 13X13 2:26X26 3:52X52
            anchors: anchors for yolo
            ignore_thresh: float,0-1, the iou threshold whether to ignore object confidence loss
        """
        super(YoloLoss, self).__init__(reduction=(tf.losses.Reduction.NONE), name='yolo_loss')
        anchor_masks = len(anchors) // 3 == 3 or anchors or [[6, 7, 8], [3, 4, 5], [0, 1, 2]] if anchors else [[3, 4, 5], [1, 2, 3]]
        self.scale_stage = scale_stage
        self.ignore_thresh = ignore_thresh
        self.anchor = anchors[anchor_masks[scale_stage]] if anchors else self.defalt_anchors[anchor_masks[scale_stage]]
        self.input_shape = input_shape
        self.num_class = num_class
        self.giou_loss = giou_loss
        self.print_loss = print_loss
        self.grid_shape = (input_shape[0] // 32 * (scale_stage + 1), input_shape[1] // 32 * (scale_stage + 1))

    def call(self, y_true, y_pred):
        """
        y_pred:  shape like (batch, gridx,gridy,(5+class)*3)
        y_true:  shape like  (batch,gridx,gridy,3,(5+class))
        anchors: array, shape=(N, 2), wh, default value:
        num_classes: integer
        ignore_thresh: float, the iou threshold whether to ignore object confidence loss
        Returns
        loss: tensor, shape=(1,)

        """
        loss = 0
        batch = K.shape(y_pred)[0]
        batch_tensor = K.cast(K.shape(y_pred)[0], K.dtype(y_true[0]))
        grid_shape = K.cast(K.shape(y_pred)[1:3], K.dtype(y_true))
        object_mask = y_true[..., 4:5]
        true_class_probs = y_true[..., 5:]
        input_shape = tf.shape(y_pred)[1:3]
        grid, raw_pred, pred_xy, pred_wh = yolo_head_sp(y_pred, (self.anchor),
          (self.num_class), input_shape,
          (self.grid_shape), calc_loss=True)
        pred_box = K.concatenate([pred_xy, pred_wh])
        raw_true_xy = y_true[..., :2] * grid_shape[::-1] - grid
        raw_true_wh = K.log(y_true[..., 2:4] / self.anchor * self.input_shape[::-1] + 1e-10)
        raw_true_wh = K.switch(object_mask, raw_true_wh, K.zeros_like(raw_true_wh))
        box_loss_scale = 2 - y_true[..., 2:3] * y_true[..., 3:4]
        ignore_mask = tf.TensorArray((K.dtype(y_true)), size=1, dynamic_size=True)
        object_mask_bool = K.cast(object_mask, 'bool')

        def loop_body(b, ignore_mask):
            true_box = tf.boolean_mask(y_true[b, ..., 0:4], object_mask_bool[(b, ..., 0)])
            iou = box_iou(pred_box[b], true_box)
            best_iou = K.max(iou, axis=(-1))
            ignore_mask = ignore_mask.write(b, K.cast(best_iou < self.ignore_thresh, K.dtype(true_box)))
            return (b + 1, ignore_mask)

        _, ignore_mask = tf.while_loop(lambda b, *args: b < batch, loop_body, [0, ignore_mask])
        ignore_mask = ignore_mask.stack()
        ignore_mask = K.expand_dims(ignore_mask, -1)
        confidence_loss = object_mask * K.binary_crossentropy(object_mask, (raw_pred[..., 4:5]), from_logits=True) + (1 - object_mask) * K.binary_crossentropy(object_mask, (raw_pred[..., 4:5]), from_logits=True) * ignore_mask
        class_loss = object_mask * K.binary_crossentropy(true_class_probs, (raw_pred[..., 5:]), from_logits=True)
        confidence_loss = tf.reduce_sum(confidence_loss) / batch_tensor
        class_loss = tf.reduce_sum(class_loss) / batch_tensor
        if self.giou_loss:
            pred_max = tf.reverse(pred_xy + pred_wh / 2.0, [-1])
            pred_min = tf.reverse(pred_xy - pred_wh / 2.0, [-1])
            pred_box = tf.concat([pred_min, pred_max], -1)
            true_xy = y_true[..., :2]
            true_wh = y_true[..., 2:4]
            true_max = tf.reverse(true_xy + true_wh / 2.0, [-1])
            true_min = tf.reverse(true_xy - true_wh / 2.0, [-1])
            true_box = tf.concat([true_min, true_max], -1)
            true_box = tf.clip_by_value(true_box, 0, 1)
            giou = do_giou_calculate(pred_box, true_box)
            giou_loss = object_mask * (1 - tf.expand_dims(giou, -1))
            giou_loss = tf.reduce_sum(giou_loss) / batch_tensor
            loss += giou_loss + confidence_loss + class_loss
            if self.print_loss:
                tf.print(str(self.idx) + ':', giou_loss, confidence_loss, class_loss, tf.reduce_sum(ignore_mask))
        else:
            xy_loss = object_mask * box_loss_scale * K.binary_crossentropy(raw_true_xy, (raw_pred[..., 0:2]), from_logits=True)
            wh_loss = object_mask * box_loss_scale * 0.5 * K.square(raw_true_wh - raw_pred[..., 2:4])
            xy_loss = tf.reduce_sum(xy_loss) / batch_tensor
            wh_loss = tf.reduce_sum(wh_loss) / batch_tensor
            loss += xy_loss + wh_loss + confidence_loss + class_loss
        if self.print_loss:
            loss = tf.print(loss, [loss, xy_loss, wh_loss, confidence_loss, class_loss, K.sum(ignore_mask)], message='loss: ')
        return loss