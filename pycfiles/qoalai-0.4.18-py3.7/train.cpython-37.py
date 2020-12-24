# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoalai/segmentations/train.py
# Compiled at: 2019-09-05 02:38:27
# Size of source mod 2**32: 1254 bytes
import qoalai.segmentations as dl
import tensorflow as tf
segmentation = dl.DeepLab(num_classes=1, is_training=True)
segmentation.saver_all = tf.train.Saver()
segmentation.session = tf.Session()
segmentation.session.run(tf.global_variables_initializer())
train_generator = segmentation.batch_generator(batch_size=1, dataset_path='/home/dataset/part_segmentation/',
  message='TRAIN')
val_generator = segmentation.batch_generator(batch_size=1, dataset_path='/home/dataset/part_segmentation/',
  message='VAL')
segmentation.check_val_data(train_generator)
segmentation.optimize(subdivisions=10, iterations=10000,
  best_loss=1000,
  train_batch=train_generator,
  val_batch=val_generator,
  save_path='/home/model/melon_segmentation/v0')