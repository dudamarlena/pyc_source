# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/retinanet/models/effnet.py
# Compiled at: 2020-04-26 08:16:50
# Size of source mod 2**32: 6135 bytes
import efficientnet.keras as efn
import tensorflow.keras.backend as K
from keras.utils import get_file
from tensorflow import keras
from . import Backbone
from .retinanet import RetinaNetModel

class EfficientNetBackbone(Backbone):
    __doc__ = ' Describes backbone information and provides utility functions.\n    '

    def __init__(self, backbone):
        super(EfficientNetBackbone, self).__init__(backbone)
        self.preprocess_image_func = None

    def retinanet(self, *args, **kwargs):
        """ Returns a retinanet model using the correct backbone.
        """
        return effnet_retinanet(args, backbone=self.backbone, **kwargs)

    def download_imagenet(self):
        """ Downloads ImageNet weights and returns path to weights file.
        """
        from efficientnet.weights import IMAGENET_WEIGHTS_PATH
        from efficientnet.weights import IMAGENET_WEIGHTS_HASHES
        model_name = 'efficientnet-b' + self.backbone[(-1)]
        file_name = model_name + '_weights_tf_dim_ordering_tf_kernels_autoaugment_notop.h5'
        file_hash = IMAGENET_WEIGHTS_HASHES[model_name][1]
        weights_path = get_file(file_name, (IMAGENET_WEIGHTS_PATH + file_name), cache_subdir='models', file_hash=file_hash)
        return weights_path

    def validate(self):
        """ Checks whether the backbone string is correct.
        """
        allowed_backbones = [
         'EfficientNetB0', 'EfficientNetB1', 'EfficientNetB2', 'EfficientNetB3', 'EfficientNetB4',
         'EfficientNetB5', 'EfficientNetB6', 'EfficientNetB7']
        backbone = self.backbone.split('_')[0]
        if backbone not in allowed_backbones:
            raise ValueError("Backbone ('{}') not in allowed backbones ({}).".format(backbone, allowed_backbones))

    def preprocess_image(self, inputs):
        """ Takes as input an image and prepares it for being passed through the network.
        """
        return efn.preprocess_input(inputs)


def effnet_retinanet(num_classes, backbone='EfficientNetB0', inputs=None, modifier=None, **kwargs):
    """ Constructs a retinanet model using a resnet backbone.

    Args
        num_classes: Number of classes to predict.
        backbone: Which backbone to use (one of ('resnet50', 'resnet101', 'resnet152')).
        inputs: The inputs to the network (defaults to a Tensor of shape (None, None, 3)).
        modifier: A function handler which can modify the backbone before using it in retinanet (this can be used to freeze backbone layers for example).

    Returns
        RetinaNet model with a ResNet backbone.
    """
    if inputs is None:
        if K.image_data_format() == 'channels_first':
            inputs = keras.layers.Input(shape=(3, None, None))
        else:
            inputs = keras.layers.Input(shape=(None, None, 3))
    elif backbone == 'EfficientNetB0':
        model = efn.EfficientNetB0(input_tensor=inputs, include_top=False, weights=None)
    else:
        if backbone == 'EfficientNetB1':
            model = efn.EfficientNetB1(input_tensor=inputs, include_top=False, weights=None)
        else:
            if backbone == 'EfficientNetB2':
                model = efn.EfficientNetB2(input_tensor=inputs, include_top=False, weights=None)
            else:
                if backbone == 'EfficientNetB3':
                    model = efn.EfficientNetB3(input_tensor=inputs, include_top=False, weights=None)
                else:
                    if backbone == 'EfficientNetB4':
                        model = efn.EfficientNetB4(input_tensor=inputs, include_top=False, weights=None)
                    else:
                        if backbone == 'EfficientNetB5':
                            model = efn.EfficientNetB5(input_tensor=inputs, include_top=False, weights=None)
                        else:
                            if backbone == 'EfficientNetB6':
                                model = efn.EfficientNetB6(input_tensor=inputs, include_top=False, weights=None)
                            else:
                                if backbone == 'EfficientNetB7':
                                    model = efn.EfficientNetB7(input_tensor=inputs, include_top=False, weights=None)
                                else:
                                    raise ValueError("Backbone ('{}') is invalid.".format(backbone))
    layer_outputs = [
     'block4a_expand_activation', 'block6a_expand_activation', 'top_activation']
    layer_outputs = [
     model.get_layer(name=(layer_outputs[0])).output,
     model.get_layer(name=(layer_outputs[1])).output,
     model.get_layer(name=(layer_outputs[2])).output]
    model = keras.models.Model(inputs=inputs, outputs=layer_outputs, name=(model.name))
    if modifier:
        model = modifier(model)
    return RetinaNetModel(inputs=inputs, num_classes=num_classes, backbone_layers=model.outputs, **kwargs)


def EfficientNetB0_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB0', inputs=inputs, **kwargs)


def EfficientNetB1_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB1', inputs=inputs, **kwargs)


def EfficientNetB2_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB2', inputs=inputs, **kwargs)


def EfficientNetB3_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB3', inputs=inputs, **kwargs)


def EfficientNetB4_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB4', inputs=inputs, **kwargs)


def EfficientNetB5_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB5', inputs=inputs, **kwargs)


def EfficientNetB6_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB6', inputs=inputs, **kwargs)


def EfficientNetB7_retinanet(num_classes, inputs=None, **kwargs):
    return effnet_retinanet(num_classes=num_classes, backbone='EfficientNetB7', inputs=inputs, **kwargs)