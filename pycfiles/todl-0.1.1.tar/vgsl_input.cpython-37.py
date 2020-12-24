# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/street/python/vgsl_input.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 6733 bytes
"""String network description language to define network layouts."""
import collections, tensorflow as tf
from tensorflow.python.ops import parsing_ops
ImageShape = collections.namedtuple('ImageTensorDims', [
 'batch_size', 'height', 'width', 'depth'])

def ImageInput(input_pattern, num_threads, shape, using_ctc, reader=None):
    """Creates an input image tensor from the input_pattern filenames.

  TODO(rays) Expand for 2-d labels, 0-d labels, and logistic targets.
  Args:
    input_pattern:  Filenames of the dataset(s) to read.
    num_threads:    Number of preprocessing threads.
    shape:          ImageShape with the desired shape of the input.
    using_ctc:      Take the unpadded_class labels instead of padded.
    reader:         Function that returns an actual reader to read Examples from
      input files. If None, uses tf.TFRecordReader().
  Returns:
    images:   Float Tensor containing the input image scaled to [-1.28, 1.27].
    heights:  Tensor int64 containing the heights of the images.
    widths:   Tensor int64 containing the widths of the images.
    labels:   Serialized SparseTensor containing the int64 labels.
    sparse_labels:   Serialized SparseTensor containing the int64 labels.
    truths:   Tensor string of the utf8 truth texts.
  Raises:
    ValueError: if the optimizer type is unrecognized.
  """
    data_files = tf.gfile.Glob(input_pattern)
    assert data_files, 'no files found for dataset ' + input_pattern
    queue_capacity = shape.batch_size * num_threads * 2
    filename_queue = tf.train.string_input_producer(data_files,
      capacity=queue_capacity)
    images_and_label_lists = []
    for _ in range(num_threads):
        image, height, width, labels, text = _ReadExamples(filename_queue, shape, using_ctc, reader)
        images_and_label_lists.append([image, height, width, labels, text])

    images, heights, widths, labels, truths = tf.train.batch_join(images_and_label_lists,
      batch_size=(shape.batch_size),
      capacity=(16 * shape.batch_size),
      dynamic_pad=True)
    labels = tf.deserialize_many_sparse(labels, tf.int64)
    sparse_labels = tf.cast(labels, tf.int32)
    labels = tf.sparse_tensor_to_dense(labels)
    labels = tf.reshape(labels, [shape.batch_size, -1], name='Labels')
    heights = tf.reshape(heights, [-1], name='Heights')
    widths = tf.reshape(widths, [-1], name='Widths')
    truths = tf.reshape(truths, [-1], name='Truths')
    images = tf.identity(images, name='Images')
    tf.summary.image('Images', images)
    return (images, heights, widths, labels, sparse_labels, truths)


def _ReadExamples(filename_queue, shape, using_ctc, reader=None):
    """Builds network input tensor ops for TF Example.

  Args:
    filename_queue: Queue of filenames, from tf.train.string_input_producer
    shape:          ImageShape with the desired shape of the input.
    using_ctc:      Take the unpadded_class labels instead of padded.
    reader:         Function that returns an actual reader to read Examples from
      input files. If None, uses tf.TFRecordReader().
  Returns:
    image:   Float Tensor containing the input image scaled to [-1.28, 1.27].
    height:  Tensor int64 containing the height of the image.
    width:   Tensor int64 containing the width of the image.
    labels:  Serialized SparseTensor containing the int64 labels.
    text:    Tensor string of the utf8 truth text.
  """
    if reader:
        reader = reader()
    else:
        reader = tf.TFRecordReader()
    _, example_serialized = reader.read(filename_queue)
    example_serialized = tf.reshape(example_serialized, shape=[])
    features = tf.parse_single_example(example_serialized, {'image/encoded':parsing_ops.FixedLenFeature([
      1],
       dtype=tf.string, default_value=''), 
     'image/text':parsing_ops.FixedLenFeature([
      1],
       dtype=tf.string, default_value=''), 
     'image/class':parsing_ops.VarLenFeature(dtype=tf.int64), 
     'image/unpadded_class':parsing_ops.VarLenFeature(dtype=tf.int64), 
     'image/height':parsing_ops.FixedLenFeature([
      1],
       dtype=tf.int64, default_value=1), 
     'image/width':parsing_ops.FixedLenFeature([
      1],
       dtype=tf.int64, default_value=1)})
    if using_ctc:
        labels = features['image/unpadded_class']
    else:
        labels = features['image/class']
    labels = tf.serialize_sparse(labels)
    image = tf.reshape((features['image/encoded']), shape=[], name='encoded')
    image = _ImageProcessing(image, shape)
    height = tf.reshape(features['image/height'], [-1])
    width = tf.reshape(features['image/width'], [-1])
    text = tf.reshape((features['image/text']), shape=[])
    return (
     image, height, width, labels, text)


def _ImageProcessing(image_buffer, shape):
    """Convert a PNG string into an input tensor.

  We allow for fixed and variable sizes.
  Does fixed conversion to floats in the range [-1.28, 1.27].
  Args:
    image_buffer: Tensor containing a PNG encoded image.
    shape:          ImageShape with the desired shape of the input.
  Returns:
    image:        Decoded, normalized image in the range [-1.28, 1.27].
  """
    image = tf.image.decode_png(image_buffer, channels=(shape.depth))
    image.set_shape([shape.height, shape.width, shape.depth])
    image = tf.cast(image, tf.float32)
    image = tf.subtract(image, 128.0)
    image = tf.multiply(image, 0.01)
    return image