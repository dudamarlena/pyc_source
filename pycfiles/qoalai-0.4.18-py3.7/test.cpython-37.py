# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoalai/test.py
# Compiled at: 2020-03-18 08:04:07
# Size of source mod 2**32: 2134 bytes
import tensorflow as tf
from face_recog.net import get_resnet
w_init_method = tf.contrib.layers.xavier_initializer(uniform=False)
image_height, image_width = (112, 112)
input_string = tf.placeholder((tf.string), shape=[None], name='string_input')
decode = lambda raw_byte_str: tf.image.resize_images(tf.cast(tf.image.decode_jpeg(raw_byte_str, channels=3, name='decoded_image'), tf.uint8), [
 image_height, image_width])
input_images = tf.map_fn(decode, input_string, dtype=(tf.float32)) - 127.5
input_images = input_images / 127.5
net = get_resnet(input_images, 50, type='ir', w_init=w_init_method, trainable=False)
embedding_tensor = net.outputs
saver = tf.train.Saver()
session = tf.Session()
saver.restore(session, '/home/model/facerecog/ckpt_model_d/InsightFace_iter_best_710000.ckpt')
print('===============')
builder = tf.saved_model.builder.SavedModelBuilder('/home/model/facerecog/ckpt_model_d/serving2/')
tensor_info_x = tf.saved_model.utils.build_tensor_info(input_string)
tensor_info_y = tf.saved_model.utils.build_tensor_info(embedding_tensor)
prediction_signature = tf.saved_model.signature_def_utils.build_signature_def(inputs={'input': tensor_info_x},
  outputs={'output': tensor_info_y},
  method_name=(tf.saved_model.signature_constants.PREDICT_METHOD_NAME))
legacy_init_op = tf.group((tf.tables_initializer()), name='legacy_init_op')
builder.add_meta_graph_and_variables(session,
  [tf.saved_model.tag_constants.SERVING], signature_def_map={'serving_default': prediction_signature},
  legacy_init_op=legacy_init_op)
builder.save()