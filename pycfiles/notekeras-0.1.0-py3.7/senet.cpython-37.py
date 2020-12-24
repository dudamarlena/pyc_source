# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/retinanet/models/senet.py
# Compiled at: 2020-04-26 08:17:34
# Size of source mod 2**32: 5835 bytes
from classification_models.keras import Classifiers
from tensorflow import keras
from tensorflow.keras.utils import get_file
from . import Backbone
from .retinanet import RetinaNetModel

class SeBackbone(Backbone):
    __doc__ = ' Describes backbone information and provides utility functions.\n    '

    def __init__(self, backbone):
        super(SeBackbone, self).__init__(backbone)
        _, self.preprocess_image_func = Classifiers.get(self.backbone)

    def retinanet(self, *args, **kwargs):
        """ Returns a retinanet model using the correct backbone.
        """
        return senet_retinanet(args, backbone=self.backbone, **kwargs)

    def download_imagenet(self):
        """ Downloads ImageNet weights and returns path to weights file.
        """
        from classification_models.weights import WEIGHTS_COLLECTION
        weights_path = None
        for el in WEIGHTS_COLLECTION:
            if el['model'] == self.backbone:
                weights_path = el['include_top'] or get_file((el['name']), (el['url']), cache_subdir='models', file_hash=(el['md5']))

        if weights_path is None:
            raise ValueError('Unable to find imagenet weights for backbone {}!'.format(self.backbone))
        return weights_path

    def validate(self):
        """ Checks whether the backbone string is correct.
        """
        allowed_backbones = [
         'seresnet18', 'seresnet34', 'seresnet50', 'seresnet101', 'seresnet152',
         'seresnext50', 'seresnext101', 'senet154']
        backbone = self.backbone.split('_')[0]
        if backbone not in allowed_backbones:
            raise ValueError("Backbone ('{}') not in allowed backbones ({}).".format(backbone, allowed_backbones))

    def preprocess_image(self, inputs):
        """ Takes as input an image and prepares it for being passed through the network.
        """
        return self.preprocess_image_func(inputs)


def senet_retinanet(num_classes, backbone='seresnext50', inputs=None, modifier=None, **kwargs):
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
        if keras.backend.image_data_format() == 'channels_first':
            inputs = keras.layers.Input(shape=(3, None, None))
        else:
            inputs = keras.layers.Input(shape=(None, None, 3))
    else:
        classifier, _ = Classifiers.get(backbone)
        model = classifier(input_tensor=inputs, include_top=False, weights=None)
        if backbone == 'seresnet18' or backbone == 'seresnet34':
            layer_outputs = [
             'stage3_unit1_relu1', 'stage4_unit1_relu1', 'relu1']
        else:
            if backbone == 'seresnet50':
                layer_outputs = [
                 'activation_36', 'activation_66', 'activation_81']
            else:
                if backbone == 'seresnet101':
                    layer_outputs = [
                     'activation_36', 'activation_151', 'activation_166']
                else:
                    if backbone == 'seresnet152':
                        layer_outputs = [
                         'activation_56', 'activation_236', 'activation_251']
                    else:
                        if backbone == 'seresnext50':
                            layer_outputs = [
                             'activation_37', 'activation_67', 'activation_81']
                        else:
                            if backbone == 'seresnext101':
                                layer_outputs = [
                                 'activation_37', 'activation_152', 'activation_166']
                            else:
                                if backbone == 'senet154':
                                    layer_outputs = [
                                     'activation_59', 'activation_239', 'activation_253']
                                else:
                                    raise ValueError("Backbone ('{}') is invalid.".format(backbone))
    layer_outputs = [
     model.get_layer(name=(layer_outputs[0])).output,
     model.get_layer(name=(layer_outputs[1])).output,
     model.get_layer(name=(layer_outputs[2])).output]
    model = keras.models.Model(inputs=inputs, outputs=layer_outputs, name=(model.name))
    if modifier:
        model = modifier(model)
    return RetinaNetModel(inputs=inputs, num_classes=num_classes, backbone_layers=model.outputs, **kwargs)


def seresnet18_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='seresnet18', inputs=inputs, **kwargs)


def seresnet34_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='seresnet34', inputs=inputs, **kwargs)


def seresnet50_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='seresnet50', inputs=inputs, **kwargs)


def seresnet101_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='seresnet101', inputs=inputs, **kwargs)


def seresnet152_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='seresnet152', inputs=inputs, **kwargs)


def seresnext50_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='seresnext50', inputs=inputs, **kwargs)


def seresnext101_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='seresnext101', inputs=inputs, **kwargs)


def senet154_retinanet(num_classes, inputs=None, **kwargs):
    return senet_retinanet(num_classes=num_classes, backbone='senet154', inputs=inputs, **kwargs)