# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/attention_ocr/python/demo_inference.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 3593 bytes
"""A script to run inference on a set of image files.

NOTE #1: The Attention OCR model was trained only using FSNS train dataset and
it will work only for images which look more or less similar to french street
names. In order to apply it to images from a different distribution you need
to retrain (or at least fine-tune) it using images from that distribution.

NOTE #2: This script exists for demo purposes only. It is highly recommended
to use tools and mechanisms provided by the TensorFlow Serving system to run
inference on TensorFlow models in production:
https://www.tensorflow.org/serving/serving_basic

Usage:
python demo_inference.py --batch_size=32   --checkpoint=model.ckpt-399731  --image_path_pattern=./datasets/data/fsns/temp/fsns_train_%02d.png
"""
import numpy as np, PIL.Image, tensorflow as tf
from tensorflow.python.platform import flags
from tensorflow.python.training import monitored_session
import common_flags, datasets, data_provider
FLAGS = flags.FLAGS
common_flags.define()
flags.DEFINE_string('image_path_pattern', '', 'A file pattern with a placeholder for the image index.')

def get_dataset_image_size(dataset_name):
    ds_module = getattr(datasets, dataset_name)
    height, width, _ = ds_module.DEFAULT_CONFIG['image_shape']
    return (width, height)


def load_images(file_pattern, batch_size, dataset_name):
    width, height = get_dataset_image_size(dataset_name)
    images_actual_data = np.ndarray(shape=(batch_size, height, width, 3), dtype='uint8')
    for i in range(batch_size):
        path = file_pattern % i
        print('Reading %s' % path)
        pil_image = PIL.Image.open(tf.gfile.GFile(path, 'rb'))
        images_actual_data[(i, ...)] = np.asarray(pil_image)

    return images_actual_data


def create_model(batch_size, dataset_name):
    width, height = get_dataset_image_size(dataset_name)
    dataset = common_flags.create_dataset(split_name=(FLAGS.split_name))
    model = common_flags.create_model(num_char_classes=(dataset.num_char_classes),
      seq_length=(dataset.max_sequence_length),
      num_views=(dataset.num_of_views),
      null_code=(dataset.null_code),
      charset=(dataset.charset))
    raw_images = tf.placeholder((tf.uint8), shape=[batch_size, height, width, 3])
    images = tf.map_fn((data_provider.preprocess_image), raw_images, dtype=(tf.float32))
    endpoints = model.create_base(images, labels_one_hot=None)
    return (raw_images, endpoints)


def run(checkpoint, batch_size, dataset_name, image_path_pattern):
    images_placeholder, endpoints = create_model(batch_size, dataset_name)
    images_data = load_images(image_path_pattern, batch_size, dataset_name)
    session_creator = monitored_session.ChiefSessionCreator(checkpoint_filename_with_path=checkpoint)
    with monitored_session.MonitoredSession(session_creator=session_creator) as (sess):
        predictions = sess.run((endpoints.predicted_text), feed_dict={images_placeholder: images_data})
    return [pr_bytes.decode('utf-8') for pr_bytes in predictions.tolist()]


def main(_):
    print('Predicted strings:')
    predictions = run(FLAGS.checkpoint, FLAGS.batch_size, FLAGS.dataset_name, FLAGS.image_path_pattern)
    for line in predictions:
        print(line)


if __name__ == '__main__':
    tf.app.run()