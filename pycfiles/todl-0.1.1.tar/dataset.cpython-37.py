# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/r1/mnist/dataset.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 4149 bytes
"""tf.data.Dataset interface to the MNIST dataset."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import gzip, os, shutil, tempfile, numpy as np
from six.moves import urllib
import tensorflow as tf

def read32(bytestream):
    """Read 4 bytes from bytestream as an unsigned 32-bit integer."""
    dt = np.dtype(np.uint32).newbyteorder('>')
    return np.frombuffer((bytestream.read(4)), dtype=dt)[0]


def check_image_file_header(filename):
    """Validate that filename corresponds to images for the MNIST dataset."""
    with tf.io.gfile.GFile(filename, 'rb') as (f):
        magic = read32(f)
        read32(f)
        rows = read32(f)
        cols = read32(f)
        if magic != 2051:
            raise ValueError('Invalid magic number %d in MNIST file %s' % (magic,
             f.name))
        if rows != 28 or cols != 28:
            raise ValueError('Invalid MNIST file %s: Expected 28x28 images, found %dx%d' % (
             f.name, rows, cols))


def check_labels_file_header(filename):
    """Validate that filename corresponds to labels for the MNIST dataset."""
    with tf.io.gfile.GFile(filename, 'rb') as (f):
        magic = read32(f)
        read32(f)
        if magic != 2049:
            raise ValueError('Invalid magic number %d in MNIST file %s' % (magic,
             f.name))


def download(directory, filename):
    """Download (and unzip) a file from the MNIST dataset if not already done."""
    filepath = os.path.join(directory, filename)
    if tf.io.gfile.exists(filepath):
        return filepath
    if not tf.io.gfile.exists(directory):
        tf.io.gfile.makedirs(directory)
    url = 'https://storage.googleapis.com/cvdf-datasets/mnist/' + filename + '.gz'
    _, zipped_filepath = tempfile.mkstemp(suffix='.gz')
    print('Downloading %s to %s' % (url, zipped_filepath))
    urllib.request.urlretrieve(url, zipped_filepath)
    with gzip.open(zipped_filepath, 'rb') as (f_in):
        with tf.io.gfile.GFile(filepath, 'wb') as (f_out):
            shutil.copyfileobj(f_in, f_out)
    os.remove(zipped_filepath)
    return filepath


def dataset(directory, images_file, labels_file):
    """Download and parse MNIST dataset."""
    images_file = download(directory, images_file)
    labels_file = download(directory, labels_file)
    check_image_file_header(images_file)
    check_labels_file_header(labels_file)

    def decode_image(image):
        image = tf.io.decode_raw(image, tf.uint8)
        image = tf.cast(image, tf.float32)
        image = tf.reshape(image, [784])
        return image / 255.0

    def decode_label(label):
        label = tf.io.decode_raw(label, tf.uint8)
        label = tf.reshape(label, [])
        return tf.cast(label, tf.int32)

    images = tf.data.FixedLengthRecordDataset(images_file,
      784, header_bytes=16).map(decode_image)
    labels = tf.data.FixedLengthRecordDataset(labels_file,
      1, header_bytes=8).map(decode_label)
    return tf.data.Dataset.zip((images, labels))


def train(directory):
    """tf.data.Dataset object for MNIST training data."""
    return dataset(directory, 'train-images-idx3-ubyte', 'train-labels-idx1-ubyte')


def test(directory):
    """tf.data.Dataset object for MNIST test data."""
    return dataset(directory, 't10k-images-idx3-ubyte', 't10k-labels-idx1-ubyte')