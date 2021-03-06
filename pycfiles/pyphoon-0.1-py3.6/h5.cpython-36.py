# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pyphoon/io/h5.py
# Compiled at: 2018-02-07 10:19:06
# Size of source mod 2**32: 4190 bytes
import h5py
from os import listdir
from os.path import isfile, join, isdir
import numpy as np

def get_h5_filenames(directory):
    """ Obtains the list of H5 file names within the given directory. If the
    specified directory is a H5 file itself, then the name of the file is
    returned.

    :param directory: Path to an H5 file or a folder with a set of H5 files.
    :type directory: str
    :return: List with the paths to all H5 files available according to the
        specified directory. List is empty if no file was found).
    :rtype: list
    """
    if isdir(directory):
        files = [f for f in listdir(directory) if f.endswith('.h5') if isfile(join(directory, f))]
        files = sorted(files)
    else:
        if directory.endswith('.h5'):
            directory = directory.split('/')[(-1)]
            files = [directory]
        else:
            files = []
    return files


def read_h5file(path_to_file):
    """ Reads an HDF file and returns its content in a dictionary-fashion.

    :param path_to_file: Path to an H5 file.
    :type path_to_file: str
    :return: Content of the H5 file as a dictionary. Keys stand for data
        field names, values are the corresponding data.
    :rtype: dict
    """
    with h5py.File(path_to_file, 'r') as (h5f):
        keys = list(h5f.keys())
        data = {}
        for key in keys:
            if key != 'name':
                value = h5f[key][:]
                if isinstance(value, np.ndarray):
                    if isinstance(value[0], bytes):
                        _value = value
                        value = [n.decode('utf-8') for n in _value]
                data[key] = value

    return data


def write_h5file(data, path_to_file, compression):
    """ Constructs and stores an H5 file containing the given data.

    :param data: Dictionary containing the data to be stored. Keys stand for
        data field names, values are the corresponding data.
    :type data: dict
    :param path_to_file: Path where the new H5 file will be created.
    :type path_to_file: str
    :param compression: Use to compress H5 file. Find more details at
            the `h5py documentation`_

    .. _h5py documentation:
            http://docs.h5py.org/en/latest/high/dataset.html
    """
    with h5py.File(path_to_file, 'w') as (h5f):
        for key, value in data.items():
            if isinstance(value, list):
                if isinstance(value[0], str):
                    _value = value
                    value = [n.encode('ascii', 'ignore') for n in _value]
            h5f.create_dataset(key, data=value, compression=compression)


def read_images(path_to_folder):
    """ Reads all image files within a given folder. Note that all images are
    assumed to have the same dimensionality. In addition, an image should have
    been stored as a dataset, with name 'infrared', in an HDF file.

    :param path_to_folder: Complete path to the folder containing HDF image
        files.
    :type path_to_folder: str
    :return: *NxWxH* Numpy array (*N*: #images, *W*: image width, *H*: image
        height)
    """
    files = get_h5_filenames(path_to_folder)
    images = []
    for file in files:
        img = read_image(join(path_to_folder, file))
        images.append(img)

    return np.array(images)


def read_image(path_to_file):
    """ Reads an image from an HDF file. It assumes that the image was stored
    as a dataset with name 'infrared'.

    :param path_to_file: Path to the HDF file storing the image.
    :type path_to_file: str
    :return: Image
    :rtype: list
    """
    data = read_h5file(path_to_file)
    return data['infrared']