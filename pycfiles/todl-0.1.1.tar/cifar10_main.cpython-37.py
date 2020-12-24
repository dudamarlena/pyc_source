# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/r1/resnet/cifar10_main.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 10503 bytes
"""Runs a ResNet model on the CIFAR-10 dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
from absl import app as absl_app
from absl import flags
from absl import logging
from six.moves import range
import tensorflow as tf
from official.r1.resnet import resnet_model
from official.r1.resnet import resnet_run_loop
import official.utils.flags as flags_core
from official.utils.logs import logger
HEIGHT = 32
WIDTH = 32
NUM_CHANNELS = 3
_DEFAULT_IMAGE_BYTES = HEIGHT * WIDTH * NUM_CHANNELS
_RECORD_BYTES = _DEFAULT_IMAGE_BYTES + 1
NUM_CLASSES = 10
_NUM_DATA_FILES = 5
NUM_IMAGES = {'train':50000, 
 'validation':10000}
DATASET_NAME = 'CIFAR-10'

def get_filenames(is_training, data_dir):
    """Returns a list of filenames."""
    assert tf.io.gfile.exists(data_dir), 'Run cifar10_download_and_extract.py first to download and extract the CIFAR-10 data.'
    if is_training:
        return [os.path.join(data_dir, 'data_batch_%d.bin' % i) for i in range(1, _NUM_DATA_FILES + 1)]
    return [
     os.path.join(data_dir, 'test_batch.bin')]


def parse_record(raw_record, is_training, dtype):
    """Parse CIFAR-10 image and label from a raw record."""
    record_vector = tf.io.decode_raw(raw_record, tf.uint8)
    label = tf.cast(record_vector[0], tf.int32)
    depth_major = tf.reshape(record_vector[1:_RECORD_BYTES], [
     NUM_CHANNELS, HEIGHT, WIDTH])
    image = tf.cast(tf.transpose(a=depth_major, perm=[1, 2, 0]), tf.float32)
    image = preprocess_image(image, is_training)
    image = tf.cast(image, dtype)
    return (
     image, label)


def preprocess_image(image, is_training):
    """Preprocess a single image of layout [height, width, depth]."""
    if is_training:
        image = tf.image.resize_with_crop_or_pad(image, HEIGHT + 8, WIDTH + 8)
        image = tf.image.random_crop(image, [HEIGHT, WIDTH, NUM_CHANNELS])
        image = tf.image.random_flip_left_right(image)
    image = tf.image.per_image_standardization(image)
    return image


def input_fn(is_training, data_dir, batch_size, num_epochs=1, dtype=tf.float32, datasets_num_private_threads=None, parse_record_fn=parse_record, input_context=None, drop_remainder=False):
    """Input function which provides batches for train or eval.

  Args:
    is_training: A boolean denoting whether the input is for training.
    data_dir: The directory containing the input data.
    batch_size: The number of samples per batch.
    num_epochs: The number of epochs to repeat the dataset.
    dtype: Data type to use for images/features
    datasets_num_private_threads: Number of private threads for tf.data.
    parse_record_fn: Function to use for parsing the records.
    input_context: A `tf.distribute.InputContext` object passed in by
      `tf.distribute.Strategy`.
    drop_remainder: A boolean indicates whether to drop the remainder of the
      batches. If True, the batch dimension will be static.

  Returns:
    A dataset that can be used for iteration.
  """
    filenames = get_filenames(is_training, data_dir)
    dataset = tf.data.FixedLengthRecordDataset(filenames, _RECORD_BYTES)
    if input_context:
        logging.info('Sharding the dataset: input_pipeline_id=%d num_input_pipelines=%d', input_context.input_pipeline_id, input_context.num_input_pipelines)
        dataset = dataset.shard(input_context.num_input_pipelines, input_context.input_pipeline_id)
    return resnet_run_loop.process_record_dataset(dataset=dataset,
      is_training=is_training,
      batch_size=batch_size,
      shuffle_buffer=(NUM_IMAGES['train']),
      parse_record_fn=parse_record_fn,
      num_epochs=num_epochs,
      dtype=dtype,
      datasets_num_private_threads=datasets_num_private_threads,
      drop_remainder=drop_remainder)


def get_synth_input_fn(dtype):
    return resnet_run_loop.get_synth_input_fn(HEIGHT,
      WIDTH, NUM_CHANNELS, NUM_CLASSES, dtype=dtype)


class Cifar10Model(resnet_model.Model):
    __doc__ = 'Model class with appropriate defaults for CIFAR-10 data.'

    def __init__(self, resnet_size, data_format=None, num_classes=NUM_CLASSES, resnet_version=resnet_model.DEFAULT_VERSION, dtype=resnet_model.DEFAULT_DTYPE):
        """These are the parameters that work for CIFAR-10 data.

    Args:
      resnet_size: The number of convolutional layers needed in the model.
      data_format: Either 'channels_first' or 'channels_last', specifying which
        data format to use when setting up the model.
      num_classes: The number of output classes needed from the model. This
        enables users to extend the same model to their own datasets.
      resnet_version: Integer representing which version of the ResNet network
      to use. See README for details. Valid values: [1, 2]
      dtype: The TensorFlow dtype to use for calculations.

    Raises:
      ValueError: if invalid resnet_size is chosen
    """
        if resnet_size % 6 != 2:
            raise ValueError('resnet_size must be 6n + 2:', resnet_size)
        num_blocks = (resnet_size - 2) // 6
        super(Cifar10Model, self).__init__(resnet_size=resnet_size,
          bottleneck=False,
          num_classes=num_classes,
          num_filters=16,
          kernel_size=3,
          conv_stride=1,
          first_pool_size=None,
          first_pool_stride=None,
          block_sizes=([
         num_blocks] * 3),
          block_strides=[
         1, 2, 2],
          resnet_version=resnet_version,
          data_format=data_format,
          dtype=dtype)


def cifar10_model_fn(features, labels, mode, params):
    """Model function for CIFAR-10."""
    features = tf.reshape(features, [-1, HEIGHT, WIDTH, NUM_CHANNELS])
    learning_rate_fn = resnet_run_loop.learning_rate_with_decay(batch_size=(params['batch_size'] * params.get('num_workers', 1)),
      batch_denom=128,
      num_images=(NUM_IMAGES['train']),
      boundary_epochs=[
     91, 136, 182],
      decay_rates=[1, 0.1, 0.01, 0.001])
    weight_decay = 0.0002

    def loss_filter_fn(_):
        return True

    return resnet_run_loop.resnet_model_fn(features=features,
      labels=labels,
      mode=mode,
      model_class=Cifar10Model,
      resnet_size=(params['resnet_size']),
      weight_decay=weight_decay,
      learning_rate_fn=learning_rate_fn,
      momentum=0.9,
      data_format=(params['data_format']),
      resnet_version=(params['resnet_version']),
      loss_scale=(params['loss_scale']),
      loss_filter_fn=loss_filter_fn,
      dtype=(params['dtype']),
      fine_tune=(params['fine_tune']))


def define_cifar_flags():
    resnet_run_loop.define_resnet_flags()
    flags.adopt_module_key_flags(resnet_run_loop)
    flags_core.set_defaults(data_dir='/tmp/cifar10_data/cifar-10-batches-bin', model_dir='/tmp/cifar10_model',
      resnet_size='56',
      train_epochs=182,
      epochs_between_evals=10,
      batch_size=128,
      image_bytes_as_serving_input=False)


def run_cifar(flags_obj):
    """Run ResNet CIFAR-10 training and eval loop.

  Args:
    flags_obj: An object containing parsed flag values.

  Returns:
    Dictionary of results. Including final accuracy.
  """
    if flags_obj.image_bytes_as_serving_input:
        logging.fatal('--image_bytes_as_serving_input cannot be set to True for CIFAR. This flag is only applicable to ImageNet.')
        return
    input_function = flags_obj.use_synthetic_data and get_synth_input_fn(flags_core.get_tf_dtype(flags_obj)) or input_fn
    result = resnet_run_loop.resnet_main(flags_obj,
      cifar10_model_fn, input_function, DATASET_NAME, shape=[
     HEIGHT, WIDTH, NUM_CHANNELS])
    return result


def main(_):
    with logger.benchmark_context(flags.FLAGS):
        run_cifar(flags.FLAGS)


if __name__ == '__main__':
    logging.set_verbosity(logging.INFO)
    define_cifar_flags()
    absl_app.run(main)