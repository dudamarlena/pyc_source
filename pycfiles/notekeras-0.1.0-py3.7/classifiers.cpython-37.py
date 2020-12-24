# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/resnet/classifiers.py
# Compiled at: 2020-04-22 04:42:36
# Size of source mod 2**32: 4678 bytes
from tensorflow import keras
from tensorflow.keras.models import Model
import notekeras.model.resnet as models

class ResNet18Classifier(Model):
    __doc__ = '\n    A :class:`ResNet18 <ResNet18>` object.\n\n    :param inputs: input tensor (e.g. an instance of `keras.layers.Input`)\n\n    Usage:\n        >>> from notekeras.model.resnet.classifiers import ResNet18Classifier\n        >>> shape, classes = (224, 224, 3), 1000\n        >>> x = keras.layers.Input(shape)\n        >>> model = ResNet18Classifier(x)\n        >>> model.compile("adam", "categorical_crossentropy", ["accuracy"])\n    '

    def __init__(self, inputs, classes):
        outputs = models.ResNet2D18(inputs)
        outputs = keras.layers.Flatten()(outputs.output)
        outputs = keras.layers.Dense(classes, activation='softmax')(outputs)
        super(ResNet18Classifier, self).__init__(inputs, outputs)


class ResNet34Classifier(Model):
    __doc__ = '\n    A :class:`ResNet34 <ResNet34>` object.\n\n    :param inputs: input tensor (e.g. an instance of `keras.layers.Input`)\n\n    Usage:\n        >>> from notekeras.model.resnet.classifiers import ResNet34Classifier\n        >>> shape, classes = (224, 224, 3), 1000\n        >>> x = keras.layers.Input(shape)\n        >>> model = ResNet34Classifier(x)\n        >>> model.compile("adam", "categorical_crossentropy", ["accuracy"])\n    '

    def __init__(self, inputs, classes):
        outputs = models.ResNet2D34(inputs)
        outputs = keras.layers.Flatten()(outputs.output)
        outputs = keras.layers.Dense(classes, activation='softmax')(outputs)
        super(ResNet34Classifier, self).__init__(inputs, outputs)


class ResNet50Classifier(Model):
    __doc__ = '\n    A :class:`ResNet50 <ResNet50>` object.\n\n    :param inputs: input tensor (e.g. an instance of `keras.layers.Input`)\n\n    Usage:\n\n        >>> from notekeras.model.resnet.classifiers import ResNet50Classifier\n        >>> shape, classes = (224, 224, 3), 1000\n        >>> x = keras.layers.Input(shape)\n        >>> model = ResNet50Classifier(x)\n        >>> model.compile("adam", "categorical_crossentropy", ["accuracy"])\n    '

    def __init__(self, inputs, classes):
        outputs = models.ResNet2D50(inputs)
        outputs = keras.layers.Flatten()(outputs.output)
        outputs = keras.layers.Dense(classes, activation='softmax')(outputs)
        super(ResNet50Classifier, self).__init__(inputs, outputs)


class ResNet101Classifier(Model):
    __doc__ = '\n    A :class:`ResNet101 <ResNet101>` object.\n\n    :param inputs: input tensor (e.g. an instance of `keras.layers.Input`)\n\n    Usage:\n        >>> from notekeras.model.resnet.classifiers import ResNet101Classifier\n        >>> shape, classes = (224, 224, 3), 1000\n        >>> x = keras.layers.Input(shape)\n        >>> model = ResNet101Classifier(x)\n        >>> model.compile("adam", "categorical_crossentropy", ["accuracy"])\n    '

    def __init__(self, inputs, classes):
        outputs = models.ResNet2D101(inputs)
        outputs = keras.layers.Flatten()(outputs.output)
        outputs = keras.layers.Dense(classes, activation='softmax')(outputs)
        super(ResNet101Classifier, self).__init__(inputs, outputs)


class ResNet152Classifier(Model):
    __doc__ = '\n    A :class:`ResNet152 <ResNet152>` object.\n\n    :param inputs: input tensor (e.g. an instance of `keras.layers.Input`)\n\n    Usage:\n        >>> from notekeras.model.resnet.classifiers import ResNet152Classifier\n        >>> shape, classes = (224, 224, 3), 1000\n        >>> x = keras.layers.Input(shape)\n        >>> model = ResNet152Classifier(x)\n        >>> model.compile("adam", "categorical_crossentropy", ["accuracy"])\n\n    '

    def __init__(self, inputs, classes):
        outputs = models.ResNet2D152(inputs)
        outputs = keras.layers.Flatten()(outputs.output)
        outputs = keras.layers.Dense(classes, activation='softmax')(outputs)
        super(ResNet152Classifier, self).__init__(inputs, outputs)


class ResNet200Classifier(Model):
    __doc__ = '\n    A :class:`ResNet200 <ResNet200>` object.\n\n    :param inputs: input tensor (e.g. an instance of `keras.layers.Input`)\n\n    Usage:\n        >>> from notekeras.model.resnet.classifiers import ResNet200Classifier\n        >>> shape, classes = (224, 224, 3), 1000\n        >>> x = keras.layers.Input(shape)\n        >>> model = ResNet200Classifier(x)\n        >>> model.compile("adam", "categorical_crossentropy", ["accuracy"])\n    '

    def __init__(self, inputs, classes):
        outputs = models.ResNet2D200(inputs)
        outputs = keras.layers.Flatten()(outputs.output)
        outputs = keras.layers.Dense(classes, activation='softmax')(outputs)
        super(ResNet200Classifier, self).__init__(inputs, outputs)