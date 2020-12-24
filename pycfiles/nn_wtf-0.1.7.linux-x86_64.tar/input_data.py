# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nn_wtf/input_data.py
# Compiled at: 2016-12-17 04:58:38
"""Functions for reading image data from files or URLs."""
import os, numpy, urllib.request

def maybe_download(filename, base_url, work_directory):
    """Download a file from a URL if it is not already present in the work directory.

    :param filename: Name of the file online and in work directory.
    :param base_url: URL of the downloadable file minus the file name.
    :param work_directory: Directory to look for or save the file in.
    :return: The path to the (downloaded or already present) file.
    """
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
    file_path = os.path.join(work_directory, filename)
    if not os.path.exists(file_path):
        file_path, _ = urllib.request.urlretrieve(base_url + filename, file_path)
        download_size = os.stat(file_path).st_size
        print ('Successfully downloaded', filename, download_size, 'bytes.')
    return file_path


def read_one_image_from_file(filename, rows, cols, depth=1):
    """Reads one image from a file.

    :param filename: The file containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <1, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    with open(filename, 'rb') as (bytestream):
        return _one_image_from_bytestream(bytestream, rows, cols, depth)


def read_one_image_from_url(url, rows, cols, depth=1):
    """Reads one image from a URL.

    :param url: The URL containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <1, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    with urllib.request.urlopen(url) as (bytestream):
        return _one_image_from_bytestream(bytestream, rows, cols, depth)


def read_images_from_file(filename, rows, cols, num_images, depth=1):
    """Reads multiple images from a single file.

    :param filename: The file containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param num_images: Number of images to read.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <num_images, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    with open(filename, 'rb') as (bytestream):
        return images_from_bytestream(bytestream, rows, cols, num_images, depth)


def read_images_from_url(url, rows, cols, num_images, depth=1):
    """Reads multiple images from a single URL.

    :param url: The URL containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param num_images: Number of images to read.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <num_images, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    with urllib.request.urlopen(url) as (bytestream):
        return images_from_bytestream(bytestream, rows, cols, num_images, depth)


def read_images_from_files(rows, cols, depth, *filenames):
    """Reads multiple images from a list of files.

    :param filenames: The files containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <num_images, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    return _concatenate_images_from_input_function(read_one_image_from_file, rows, cols, depth, filenames)


def read_images_from_urls(rows, cols, depth, *urls):
    """Reads multiple images from a list of URLs.

    :param urls: The URLs containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <num_images, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    return _concatenate_images_from_input_function(read_one_image_from_url, rows, cols, depth, urls)


def images_from_bytestream(bytestream, rows, cols, num_images, depth=1):
    """Reads a number of images from a byte stream.

    :param bytestream: The byte stream containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param num_images: Number of images to read.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <1, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    buf = bytestream.read(rows * cols * depth * num_images)
    data = numpy.frombuffer(buf, dtype=numpy.uint8)
    return data.reshape(num_images, rows, cols, depth)


def _one_image_from_bytestream(bytestream, rows, cols, depth=1):
    """Reads one image from a byte stream.

    :param bytestream: The byte stream containing the image data.
    :param rows: Image height.
    :param cols: Image width.
    :param depth: Color depth of the image in bytes.
    :return: A numpy.ndarray of shape <1, rows, cols, depth>
    """
    _check_describes_image_geometry(rows, cols, depth)
    return images_from_bytestream(bytestream, rows, cols, depth)


def _concatenate_images_from_input_function(input_function, rows, cols, depth, input_resources):
    image_data = numpy.concatenate([ input_function(input_resource, rows, cols, depth) for input_resource in input_resources ])
    return image_data


def _check_describes_image_geometry(rows, cols, depth):
    assert rows > 0
    assert cols > 0
    assert 0 < depth < 3