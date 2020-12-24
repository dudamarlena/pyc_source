# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/input_reader_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 3531 bytes
"""Tests for input_reader_builder."""
import os, numpy as np, tensorflow as tf
from google.protobuf import text_format
from tensorflow.core.example import example_pb2
from tensorflow.core.example import feature_pb2
from object_detection.builders import input_reader_builder
from object_detection.core import standard_fields as fields
from object_detection.protos import input_reader_pb2

class InputReaderBuilderTest(tf.test.TestCase):

    def create_tf_record(self):
        path = os.path.join(self.get_temp_dir(), 'tfrecord')
        writer = tf.python_io.TFRecordWriter(path)
        image_tensor = np.random.randint(255, size=(4, 5, 3)).astype(np.uint8)
        with self.test_session():
            encoded_jpeg = tf.image.encode_jpeg(tf.constant(image_tensor)).eval()
        example = example_pb2.Example(features=feature_pb2.Features(feature={'image/encoded': feature_pb2.Feature(bytes_list=feature_pb2.BytesList(value=[encoded_jpeg])), 
         'image/format': feature_pb2.Feature(bytes_list=feature_pb2.BytesList(value=['jpeg'.encode('utf-8')])), 
         'image/object/bbox/xmin': feature_pb2.Feature(float_list=feature_pb2.FloatList(value=[0.0])), 
         'image/object/bbox/xmax': feature_pb2.Feature(float_list=feature_pb2.FloatList(value=[1.0])), 
         'image/object/bbox/ymin': feature_pb2.Feature(float_list=feature_pb2.FloatList(value=[0.0])), 
         'image/object/bbox/ymax': feature_pb2.Feature(float_list=feature_pb2.FloatList(value=[1.0])), 
         'image/object/class/label': feature_pb2.Feature(int64_list=feature_pb2.Int64List(value=[2]))}))
        writer.write(example.SerializeToString())
        writer.close()
        return path

    def test_build_tf_record_input_reader(self):
        tf_record_path = self.create_tf_record()
        input_reader_text_proto = "\n      shuffle: false\n      num_readers: 1\n      tf_record_input_reader {{\n        input_path: '{0}'\n      }}\n    ".format(tf_record_path)
        input_reader_proto = input_reader_pb2.InputReader()
        text_format.Merge(input_reader_text_proto, input_reader_proto)
        tensor_dict = input_reader_builder.build(input_reader_proto)
        sv = tf.train.Supervisor(logdir=self.get_temp_dir())
        with sv.prepare_or_wait_for_session() as (sess):
            sv.start_queue_runners(sess)
            output_dict = sess.run(tensor_dict)
        self.assertEquals((4, 5, 3), output_dict[fields.InputDataFields.image].shape)
        self.assertEquals([
         2], output_dict[fields.InputDataFields.groundtruth_classes])
        self.assertEquals((1, 4), output_dict[fields.InputDataFields.groundtruth_boxes].shape)
        self.assertAllEqual([
         0.0, 0.0, 1.0, 1.0], output_dict[fields.InputDataFields.groundtruth_boxes][0])


if __name__ == '__main__':
    tf.test.main()