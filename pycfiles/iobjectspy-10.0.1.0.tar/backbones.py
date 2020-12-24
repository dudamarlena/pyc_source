# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\backbones\backbones.py
# Compiled at: 2019-12-31 04:09:03
# Size of source mod 2**32: 1136 bytes
from cls_models.cls_models import ResNet18, ResNet34, ResNet50, ResNet101, ResNet152
from cls_models.cls_models import ResNeXt50, ResNeXt101
from cls_models.cls_models import EfficientNetB0, EfficientNetB1, EfficientNetB2, EfficientNetB3
from .inception_resnet_v2 import InceptionResNetV2
from .inception_v3 import InceptionV3
from keras.applications import DenseNet121, DenseNet169, DenseNet201
from keras.applications import VGG16
from keras.applications import VGG19
backbones = {'vgg16':VGG16, 
 'vgg19':VGG19, 
 'resnet18':ResNet18, 
 'resnet34':ResNet34, 
 'resnet50':ResNet50, 
 'resnet101':ResNet101, 
 'resnet152':ResNet152, 
 'resnext50':ResNeXt50, 
 'resnext101':ResNeXt101, 
 'inceptionresnetv2':InceptionResNetV2, 
 'inceptionv3':InceptionV3, 
 'densenet121':DenseNet121, 
 'densenet169':DenseNet169, 
 'densenet201':DenseNet201, 
 'efficientnetb0':EfficientNetB0, 
 'efficientnetb1':EfficientNetB1, 
 'efficientnetb2':EfficientNetB2, 
 'efficientnetb3':EfficientNetB3}

def get_backbone(name, *args, **kwargs):
    return (backbones[name])(*args, **kwargs)