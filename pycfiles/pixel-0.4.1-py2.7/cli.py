# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pixel/cli.py
# Compiled at: 2016-09-28 10:30:55
import threading, json, click, pixel, h5py, numpy as np, os, hashlib
from backend import start_server
import deepzoom

@click.command()
@click.argument('path', type=click.Path(exists=True))
def main(path):
    """Console script for pixel"""
    if os.path.isfile(path):
        _, file_extension = os.path.splitext(path)
        if file_extension in ('.h5', '.hdf5'):
            exists, tmp_path = maybe_create_folder(path)
            if not exists:
                dataset_type = get_dataset_type(path)
                async_creation(path, tmp_path, dataset_type)
            start_server(tmp_path)
    else:
        raise Exception("Pixel doesn't support folders yet")


def get_dataset_type(path):
    with h5py.File(path) as (f):
        arr = f['main']
        if len(arr.shape) == 3:
            if arr.dtype == np.uint8:
                return 'grayscale'
            if arr.dtype == np.uint32:
                return 'segmentation'
        else:
            if len(arr.shape) == 4 and arr.shape[0] == 3 and arr.dtype == np.float32:
                return 'affinities'
            raise ValueError(('Do not know how to display array with shape {} of type {}').format(arr.shape, arr.dtype))


def maybe_create_folder(path):
    """
  It creates a folder /tmp/pixel-{hash}
  where the hash is generated from the path
  and the modification time of the file that
  corresponds to the path
  """
    statbuf = os.stat(path)
    hash_object = hashlib.md5(path + str(statbuf.st_mtime))
    hash_string = hash_object.hexdigest()
    directory = '/tmp/pixel-' + hash_string
    if os.path.exists(directory):
        return (True, directory)
    else:
        os.makedirs(directory)
        return (False, directory)


def _process_grayscale(arr_path, tmp_path):
    creator = deepzoom.ImageCreator(tile_format='jpg', image_quality=0.8)
    with h5py.File(arr_path) as (f):
        arr = f['main']
        for z in xrange(arr.shape[0]):
            creator.create(arr[z, :, :], ('{}/{}.dzi').format(tmp_path, z))


def _process_segmentation(arr_path, tmp_path):
    creator = deepzoom.ImageCreator(tile_format='jpg', image_quality=0.8)
    with h5py.File(arr_path) as (f):
        arr = f['main']
        for z in xrange(arr.shape[0]):
            mod = np.mod(arr[z, :, :], 255).astype(np.uint8)
            creator.create(mod, ('{}/{}.dzi').format(tmp_path, z))


def _process_affinities(arr_path, tmp_path):
    creator = deepzoom.ImageCreator(tile_format='jpg', image_quality=0.8)
    with h5py.File(arr_path) as (f):
        arr = f['main']
        for z in xrange(arr.shape[0]):
            creator.create(arr[z, :, :], ('{}/{}.dzi').format(tmp_path, z))


def save_metadata(tmpfolder, dataset_type):
    with open(('{}/metadata.json').format(tmpfolder), 'w') as (f):
        json.dump({'dataset_type': dataset_type}, f, ensure_ascii=False)


def async_creation(arr_path, tmp_path, dataset_type):
    save_metadata(tmp_path, dataset_type)
    if dataset_type == 'grayscale':
        t = FuncThread(_process_grayscale, arr_path, tmp_path)
    elif dataset_type == 'segmentation':
        t = FuncThread(_process_segmentation, arr_path, tmp_path)
    else:
        t = FuncThread(_process_affinities, arr_path, tmp_path)
    t.start()


class FuncThread(threading.Thread):

    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)
        self.join()


if __name__ == '__main__':
    main()