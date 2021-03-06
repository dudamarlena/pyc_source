# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\models\efficientnet.py
# Compiled at: 2020-04-13 21:56:40
# Size of source mod 2**32: 31743 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, math, string, collections
from tensorflow.keras import backend, layers, models, utils
from six.moves import xrange
from keras_applications.imagenet_utils import _obtain_input_shape
import keras_applications.imagenet_utils as _preprocess_input
from xl_tensorflow.layers import get_swish, get_relu6
BASE_WEIGHTS_PATH = 'https://github.com/Callidior/keras-applications/releases/download/efficientnet/'
WEIGHTS_HASHES = {'efficientnet-b0':('163292582f1c6eaca8e7dc7b51b01c615b0dbc0039699b4dcd0b975cc21533dc', 'c1421ad80a9fc67c2cc4000f666aa50789ce39eedb4e06d531b0c593890ccff3'), 
 'efficientnet-b1':('d0a71ddf51ef7a0ca425bab32b7fa7f16043ee598ecee73fc674d9560c8f09b0', '75de265d03ac52fa74f2f510455ba64f9c7c5fd96dc923cd4bfefa3d680c4b68'), 
 'efficientnet-b2':('bb5451507a6418a574534aa76a91b106f6b605f3b5dde0b21055694319853086', '433b60584fafba1ea3de07443b74cfd32ce004a012020b07ef69e22ba8669333'), 
 'efficientnet-b3':('03f1fba367f070bd2545f081cfa7f3e76f5e1aa3b6f4db700f00552901e75ab9', 'c5d42eb6cfae8567b418ad3845cfd63aa48b87f1bd5df8658a49375a9f3135c7'), 
 'efficientnet-b4':('98852de93f74d9833c8640474b2c698db45ec60690c75b3bacb1845e907bf94f', '7942c1407ff1feb34113995864970cd4d9d91ea64877e8d9c38b6c1e0767c411'), 
 'efficientnet-b5':('30172f1d45f9b8a41352d4219bf930ee3339025fd26ab314a817ba8918fefc7d', '9d197bc2bfe29165c10a2af8c2ebc67507f5d70456f09e584c71b822941b1952'), 
 'efficientnet-b6':('f5270466747753485a082092ac9939caa546eb3f09edca6d6fff842cad938720', '1d0923bb038f2f8060faaf0a0449db4b96549a881747b7c7678724ac79f427ed'), 
 'efficientnet-b7':('876a41319980638fa597acbbf956a82d10819531ff2dcb1a52277f10c7aefa1a', '60b56ff3a8daccc8d96edfd40b204c113e51748da657afd58034d54d3cec2bac')}
BlockArgs = collections.namedtuple('BlockArgs', [
 'kernel_size', 'num_repeat', 'input_filters', 'output_filters',
 'expand_ratio', 'id_skip', 'strides', 'se_ratio'])
BlockArgs.__new__.__defaults__ = (None, ) * len(BlockArgs._fields)
DEFAULT_BLOCKS_ARGS = [
 BlockArgs(kernel_size=3, num_repeat=1, input_filters=32, output_filters=16, expand_ratio=1,
   id_skip=True,
   strides=[1, 1],
   se_ratio=0.25),
 BlockArgs(kernel_size=3, num_repeat=2, input_filters=16, output_filters=24, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=0.25),
 BlockArgs(kernel_size=5, num_repeat=2, input_filters=24, output_filters=40, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=0.25),
 BlockArgs(kernel_size=3, num_repeat=3, input_filters=40, output_filters=80, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=0.25),
 BlockArgs(kernel_size=5, num_repeat=3, input_filters=80, output_filters=112, expand_ratio=6,
   id_skip=True,
   strides=[1, 1],
   se_ratio=0.25),
 BlockArgs(kernel_size=5, num_repeat=4, input_filters=112, output_filters=192, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=0.25),
 BlockArgs(kernel_size=3, num_repeat=1, input_filters=192, output_filters=320, expand_ratio=6,
   id_skip=True,
   strides=[1, 1],
   se_ratio=0.25)]
DEFAULT_LITE_BLOCKS_ARGS = [
 BlockArgs(kernel_size=3, num_repeat=1, input_filters=32, output_filters=16, expand_ratio=1,
   id_skip=True,
   strides=[1, 1],
   se_ratio=None),
 BlockArgs(kernel_size=3, num_repeat=2, input_filters=16, output_filters=24, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=None),
 BlockArgs(kernel_size=5, num_repeat=2, input_filters=24, output_filters=40, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=None),
 BlockArgs(kernel_size=3, num_repeat=3, input_filters=40, output_filters=80, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=None),
 BlockArgs(kernel_size=5, num_repeat=3, input_filters=80, output_filters=112, expand_ratio=6,
   id_skip=True,
   strides=[1, 1],
   se_ratio=None),
 BlockArgs(kernel_size=5, num_repeat=4, input_filters=112, output_filters=192, expand_ratio=6,
   id_skip=True,
   strides=[2, 2],
   se_ratio=None),
 BlockArgs(kernel_size=3, num_repeat=1, input_filters=192, output_filters=320, expand_ratio=6,
   id_skip=True,
   strides=[1, 1],
   se_ratio=None)]
CONV_KERNEL_INITIALIZER = {'class_name':'VarianceScaling', 
 'config':{'scale':2.0, 
  'mode':'fan_out', 
  'distribution':'normal'}}
DENSE_KERNEL_INITIALIZER = {'class_name':'VarianceScaling', 
 'config':{'scale':0.3333333333333333, 
  'mode':'fan_out', 
  'distribution':'uniform'}}

def preprocess_input(x, **kwargs):
    kwargs = {k:v for k, v in kwargs.items() if k in ('backend', 'layers', 'models',
                                                      'utils') if k in ('backend',
                                                                        'layers',
                                                                        'models',
                                                                        'utils')}
    return _preprocess_input(x, mode='torch', **kwargs)


def round_filters(filters, width_coefficient, depth_divisor, skip=False):
    """Round number of filters based on width multiplier."""
    if skip:
        return filters
    filters *= width_coefficient
    new_filters = int(filters + depth_divisor / 2) // depth_divisor * depth_divisor
    new_filters = max(depth_divisor, new_filters)
    if new_filters < 0.9 * filters:
        new_filters += depth_divisor
    return int(new_filters)


def round_repeats(repeats, depth_coefficient):
    """Round number of repeats based on depth multiplier."""
    return int(math.ceil(depth_coefficient * repeats))


def mb_conv_block(inputs, block_args, activation, drop_rate=None, prefix='', using_se_global_pooling=True):
    """Mobile Inverted Residual Bottleneck."""
    has_se = block_args.se_ratio is not None and 0 < block_args.se_ratio <= 1
    bn_axis = 3 if backend.image_data_format() == 'channels_last' else 1
    filters = block_args.input_filters * block_args.expand_ratio
    if block_args.expand_ratio != 1:
        x = layers.Conv2D(filters, 1, padding='same',
          use_bias=False,
          kernel_initializer=CONV_KERNEL_INITIALIZER,
          name=(prefix + 'expand_conv'))(inputs)
        x = layers.BatchNormalization(axis=bn_axis, name=(prefix + 'expand_bn'))(x)
        x = layers.Activation(activation, name=(prefix + 'expand_activation'))(x)
    else:
        x = inputs
    x = layers.DepthwiseConv2D((block_args.kernel_size), strides=(block_args.strides),
      padding='same',
      use_bias=False,
      depthwise_initializer=CONV_KERNEL_INITIALIZER,
      name=(prefix + 'dwconv'))(x)
    x = layers.BatchNormalization(axis=bn_axis, name=(prefix + 'bn'))(x)
    x = layers.Activation(activation, name=(prefix + 'activation'))(x)
    if has_se:
        num_reduced_filters = max(1, int(block_args.input_filters * block_args.se_ratio))
        if using_se_global_pooling:
            se_tensor = layers.GlobalAveragePooling2D(name=(prefix + 'se_squeeze'))(x)
            target_shape = (1, 1, filters) if backend.image_data_format() == 'channels_last' else (filters, 1, 1)
            se_tensor = layers.Reshape(target_shape, name=(prefix + 'se_reshape'))(se_tensor)
        else:
            se_tensor = layers.AveragePooling2D(pool_size=(x.shape[1], x.shape[1]), name=(prefix + 'se_avg_pooling2d'))(x)
        se_tensor = layers.Conv2D(num_reduced_filters, 1, activation=activation,
          padding='same',
          use_bias=True,
          kernel_initializer=CONV_KERNEL_INITIALIZER,
          name=(prefix + 'se_reduce'))(se_tensor)
        se_tensor = layers.Conv2D(filters, 1, activation='sigmoid',
          padding='same',
          use_bias=True,
          kernel_initializer=CONV_KERNEL_INITIALIZER,
          name=(prefix + 'se_expand'))(se_tensor)
        x = layers.Multiply(name=(prefix + 'se_excite'))([x, se_tensor])
    else:
        x = layers.Conv2D((block_args.output_filters), 1, padding='same',
          use_bias=False,
          kernel_initializer=CONV_KERNEL_INITIALIZER,
          name=(prefix + 'project_conv'))(x)
        x = layers.BatchNormalization(axis=bn_axis, name=(prefix + 'project_bn'))(x)
        if block_args.id_skip:
            if all((s == 1 for s in block_args.strides)) and block_args.input_filters == block_args.output_filters:
                if drop_rate:
                    if drop_rate > 0:
                        x = layers.Dropout(drop_rate, noise_shape=(None, 1, 1, 1), name=(prefix + 'drop'))(x)
                x = layers.Add(name=(prefix + 'add'))([x, inputs])
    return x


def EfficientNet(width_coefficient, depth_coefficient, default_resolution, dropout_rate=0.2, drop_connect_rate=0.2, depth_divisor=8, blocks_args=DEFAULT_BLOCKS_ARGS, model_name='efficientnet', include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, fix_head_stem=False, using_se_global_pooling=True, **kwargs):
    """
    This version of EfficentNet must specify input shape!!!
    Instantiates the EfficientNet architecture using given scaling coefficients.
    Optionally loads weights pre-trained on ImageNet.
    Note that the data format convention used by the model is
    the one specified in your Keras config at `~/.keras/keras.json`.
    # Arguments
        width_coefficient: float, scaling coefficient for network width.
        depth_coefficient: float, scaling coefficient for network depth.
        default_resolution: int, default input image size.
        dropout_rate: float, dropout rate before final classifier layer.
        drop_connect_rate: float, dropout rate at skip connections.
        depth_divisor: int.
        blocks_args: A list of BlockArgs to construct block modules.
        model_name: string, model name.
        include_top: whether to include the fully-connected
            layer at the top of the network.
        weights: one of `None` (random initialization),
              'imagenet' (pre-training on ImageNet),
              or the path to the weights file to be loaded.
        input_tensor: optional Keras tensor
            (i.e. output of `layers.Input()`)
            to use as image input for the model.
        input_shape: optional shape tuple, only to be specified
            if `include_top` is False.
            It should have exactly 3 inputs channels.
        pooling: optional pooling mode for feature extraction
            when `include_top` is `False`.
            - `None` means that the output of the model will be
                the 4D tensor output of the
                last convolutional layer.
            - `avg` means that global average pooling
                will be applied to the output of the
                last convolutional layer, and thus
                the output of the model will be a 2D tensor.
            - `max` means that global max pooling will
                be applied.
        classes: optional number of classes to classify images
            into, only to be specified if `include_top` is True, and
            if no `weights` argument is specified.
        using_se_global_pooling: if True, cannot use GPU in lite,
            if false,must specify input shape
        fix_head_stem: fix head and stem
        force_relu: force to using relu6 to replace swish, better for quant
    # Returns
        A Keras model instance.
    # Raises
        ValueError: in case of invalid argument for `weights`,
            or invalid input shape.
    """
    if not weights in {None, 'imagenet'}:
        if not os.path.exists(weights):
            raise ValueError('The `weights` argument should be either `None` (random initialization), `imagenet` (pre-training on ImageNet), or the path to the weights file to be loaded.')
        elif weights == 'imagenet':
            if include_top and classes != 1000:
                raise ValueError('If using `weights` as `"imagenet"` with `include_top` as true, `classes` should be 1000')
        input_shape = _obtain_input_shape(input_shape, default_size=default_resolution,
          min_size=32,
          data_format=(backend.image_data_format()),
          require_flatten=include_top,
          weights=weights)
        if input_tensor is None:
            img_input = layers.Input(shape=input_shape)
        else:
            if backend.backend() == 'tensorflow':
                from tensorflow.python.keras.backend import is_keras_tensor
            else:
                is_keras_tensor = backend.is_keras_tensor
            if not is_keras_tensor(input_tensor):
                img_input = layers.Input(tensor=input_tensor, shape=input_shape)
            else:
                img_input = input_tensor
        bn_axis = 3 if backend.image_data_format() == 'channels_last' else 1
        activation = get_swish() if not force_relu else get_relu6()
        x = img_input
        x = layers.Conv2D((round_filters(32, width_coefficient, depth_divisor, fix_head_stem)), 3, strides=(2,
                                                                                                            2),
          padding='same',
          use_bias=False,
          kernel_initializer=CONV_KERNEL_INITIALIZER,
          name='stem_conv')(x)
        x = layers.BatchNormalization(axis=bn_axis, name='stem_bn')(x)
        x = layers.Activation(activation, name='stem_activation')(x)
        num_blocks_total = sum((block_args.num_repeat for block_args in blocks_args))
        block_num = 0
        for idx, block_args in enumerate(blocks_args):
            assert block_args.num_repeat > 0
            if fix_head_stem:
                if idx == 0 or idx == len(blocks_args) - 1:
                    repeats = block_args.num_repeat
                else:
                    repeats = round_repeats(block_args.num_repeat, depth_coefficient)
                block_args = block_args._replace(input_filters=(round_filters(block_args.input_filters, width_coefficient, depth_divisor)),
                  output_filters=(round_filters(block_args.output_filters, width_coefficient, depth_divisor)),
                  num_repeat=repeats)
                drop_rate = drop_connect_rate * float(block_num) / num_blocks_total
                x = mb_conv_block(x, block_args, activation=activation,
                  drop_rate=drop_rate,
                  prefix=('block{}a_'.format(idx + 1)),
                  using_se_global_pooling=using_se_global_pooling)
                block_num += 1
                if block_args.num_repeat > 1:
                    block_args = block_args._replace(input_filters=(block_args.output_filters),
                      strides=[1, 1])
                    for bidx in xrange(block_args.num_repeat - 1):
                        drop_rate = drop_connect_rate * float(block_num) / num_blocks_total
                        block_prefix = 'block{}{}_'.format(idx + 1, string.ascii_lowercase[(bidx + 1)])
                        x = mb_conv_block(x, block_args, activation=activation,
                          drop_rate=drop_rate,
                          prefix=block_prefix,
                          using_se_global_pooling=using_se_global_pooling)
                        block_num += 1

        x = layers.Conv2D((round_filters(1280, width_coefficient, depth_divisor, fix_head_stem)), 1, padding='same',
          use_bias=False,
          kernel_initializer=CONV_KERNEL_INITIALIZER,
          name='top_conv')(x)
        x = layers.BatchNormalization(axis=bn_axis, name='top_bn')(x)
        x = layers.Activation(activation, name='top_activation')(x)
        if include_top:
            x = layers.GlobalAveragePooling2D(name='avg_pool')(x)
            if dropout_rate:
                if dropout_rate > 0:
                    x = layers.Dropout(dropout_rate, name='top_dropout')(x)
                x = layers.Dense(classes, activation='softmax',
                  kernel_initializer=DENSE_KERNEL_INITIALIZER,
                  name='probs')(x)
            else:
                if pooling == 'avg':
                    x = layers.GlobalAveragePooling2D(name='avg_pool')(x)
                else:
                    if pooling == 'max':
                        x = layers.GlobalMaxPooling2D(name='max_pool')(x)
            inputs = img_input
            model = models.Model(inputs, x, name=model_name)
            if weights == 'imagenet':
                if include_top:
                    file_name = model_name.replace('lite', '') + '_weights_tf_dim_ordering_tf_kernels_autoaugment.h5'
                    file_hash = WEIGHTS_HASHES[model_name.replace('lite', '')][0]
        else:
            file_name = model_name.replace('lite', '') + '_weights_tf_dim_ordering_tf_kernels_autoaugment_notop.h5'
            file_hash = WEIGHTS_HASHES[model_name.replace('lite', '')][1]
        weights_path = utils.get_file(file_name, (BASE_WEIGHTS_PATH + file_name),
          cache_subdir='models',
          file_hash=file_hash)
        model.load_weights(weights_path, by_name=True, skip_mismatch=True)
    else:
        if weights is not None:
            model.load_weights(weights, by_name=True, skip_mismatch=True)
        return model


def EfficientNetB0(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.0, 1.0, 224, 0.2, model_name='efficientnet-b0', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetB1(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.0, 1.1, 240, 0.2, model_name='efficientnet-b1', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetB2(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.1, 1.2, 260, 0.3, model_name='efficientnet-b2', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetB3(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.2, 1.4, 300, 0.3, model_name='efficientnet-b3', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetB4(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.4, 1.8, 380, 0.4, model_name='efficientnet-b4', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetB5(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, force_relu=False, classes=1000, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.6, 2.2, 456, 0.4, model_name='efficientnet-b5', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetB6(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.8, 2.6, 528, 0.5, model_name='efficientnet-b6', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetB7(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=False, using_se_global_pooling=True, **kwargs):
    return EfficientNet(2.0, 3.1, 600, 0.5, model_name='efficientnet-b7', 
     include_top=include_top, 
     weights=weights, input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetLiteB0(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=True, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.0, 1.0, 224, 0.2, model_name='efficientnetlite-b0', 
     include_top=include_top, 
     weights=weights, blocks_args=DEFAULT_LITE_BLOCKS_ARGS, 
     fix_head_stem=True, 
     input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetLiteB1(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=True, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.0, 1.1, 240, 0.2, model_name='efficientnetlite-b1', 
     include_top=include_top, 
     weights=weights, blocks_args=DEFAULT_LITE_BLOCKS_ARGS, 
     fix_head_stem=True, 
     input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetLiteB2(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=True, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.1, 1.2, 260, 0.3, model_name='efficientnetlite-b2', 
     include_top=include_top, 
     weights=weights, blocks_args=DEFAULT_LITE_BLOCKS_ARGS, 
     fix_head_stem=True, 
     input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetLiteB3(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=True, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.2, 1.4, 280, 0.3, model_name='efficientnetlite-b3', 
     include_top=include_top, 
     weights=weights, blocks_args=DEFAULT_LITE_BLOCKS_ARGS, 
     fix_head_stem=True, 
     input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


def EfficientNetLiteB4(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000, force_relu=True, using_se_global_pooling=True, **kwargs):
    return EfficientNet(1.4, 1.8, 300, 0.3, model_name='efficientnetlite-b4', 
     include_top=include_top, 
     weights=weights, blocks_args=DEFAULT_LITE_BLOCKS_ARGS, 
     fix_head_stem=True, 
     input_tensor=input_tensor, 
     input_shape=input_shape, pooling=pooling, 
     classes=classes, force_relu=force_relu, using_se_global_pooling=using_se_global_pooling, **kwargs)


setattr(EfficientNetB0, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetB1, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetB2, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetB3, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetB4, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetB5, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetB6, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetB7, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetLiteB0, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetLiteB1, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetLiteB2, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetLiteB3, '__doc__', EfficientNet.__doc__)
setattr(EfficientNetLiteB4, '__doc__', EfficientNet.__doc__)

def main():
    model = EfficientNetB1(include_top=True, weights='imagenet', using_se_global_pooling=False)
    print(model.summary())


if __name__ == '__main__':
    main()