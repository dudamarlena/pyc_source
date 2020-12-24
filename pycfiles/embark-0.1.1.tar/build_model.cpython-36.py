# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/naresh/Projects/embark/embark/tensorflow_classifier/models/build_model.py
# Compiled at: 2020-02-03 18:14:23
# Size of source mod 2**32: 2074 bytes
import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

def build_model(model_name: str, n_classes: int, fine_tune_at: int=150):
    model = None
    transforms = {}
    if model_name == 'resnet50':
        img_size = 224
        img_shape = (img_size, img_size, 3)
        transforms['resize'] = (img_size, img_size)
        base_model = tf.keras.applications.ResNet50(input_shape=img_shape, include_top=False, weights='imagenet')
        base_model.trainable = True
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False

        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
        prediction_layer = tf.keras.layers.Dense(n_classes - 1)
        model = tf.keras.Sequential([
         base_model,
         global_average_layer,
         prediction_layer])
    else:
        if model_name == 'mobilenetv2':
            img_size = 160
            img_shape = (img_size, img_size, 3)
            transforms['resize'] = (img_size, img_size)
            base_model = tf.keras.applications.MobileNetV2(input_shape=img_shape, include_top=False, weights='imagenet')
            base_model.trainable = False
            global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
            prediction_layer = tf.keras.layers.Dense(n_classes - 1)
            model = tf.keras.Sequential([
             base_model,
             global_average_layer,
             prediction_layer])
    return (
     model, transforms)


def main():
    model, transforms = build_model('mobilenetv2', 2)
    img_batch = tf.random.uniform(shape=(1, transforms['resize'][0], transforms['resize'][1], 3))
    model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), optimizer=tf.keras.optimizers.RMSprop(lr=1e-05),
      metrics=[
     'accuracy'])
    print(model(img_batch).shape)


if __name__ == '__main__':
    main()