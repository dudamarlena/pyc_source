# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\poda\utils\convert_model_for_tensorflow_serving.py
# Compiled at: 2019-09-26 09:27:13
# Size of source mod 2**32: 2623 bytes
import tensorflow as tf, os
import poda.tranfer_learning.Vgg16 as vgg

def convert_model_vggg16(model_path=''):
    input_string = tf.placeholder((tf.string), shape=[None], name='string_input')
    decode = lambda raw_byte_str: tf.image.resize_images(tf.cast(tf.image.decode_jpeg(raw_byte_str, channels=3, name='decoded_image'), tf.uint8), [
     340, 340])
    input_images = tf.map_fn(decode, input_string, dtype=(tf.float32))
    input_images = input_images / 255.0
    var_list, non_logit, top_layer_vgg16 = vgg.VGG16().create_pretrain_model_vgg(input_tensor=input_images, num_classes=1, num_blocks=4, is_last_checkpoint=False, path_last_checkpoint=None, is_training=False, num_depthwise_layer=1, num_fully_connected_layer=1, num_hidden_unit=512, activation_fully_connected='relu', regularizers=None)
    output_saver = tf.train.Saver()
    init = tf.initializers.global_variables()
    with tf.Session() as (sess):
        writer = tf.summary.FileWriter('output', sess.graph)
        sess.run(init)
        writer.close()
        output_saver.restore(sess, model_path)
        builder = tf.saved_model.builder.SavedModelBuilder('model_extraction/')
        tensor_info_x = tf.saved_model.utils.build_tensor_info(input_string)
        tensor_info_y = tf.saved_model.utils.build_tensor_info(top_layer_vgg16)
        prediction_signature = tf.saved_model.signature_def_utils.build_signature_def(inputs={'input': tensor_info_x},
          outputs={'output': tensor_info_y},
          method_name=(tf.saved_model.signature_constants.PREDICT_METHOD_NAME))
        legacy_init_op = tf.group((tf.tables_initializer()), name='legacy_init_op')
        builder.add_meta_graph_and_variables(sess,
          [tf.saved_model.tag_constants.SERVING], signature_def_map={'predict_result': prediction_signature},
          legacy_init_op=legacy_init_op)
        builder.save()