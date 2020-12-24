# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/dataset/utils.py
# Compiled at: 2020-04-11 06:08:16
# Size of source mod 2**32: 3961 bytes
import jittor as jt, os
from six.moves import urllib
import hashlib
from tqdm import tqdm
import numpy as np
from collections.abc import Sequence, Mapping
from PIL import Image
from .. import lock

def ensure_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def _progress():
    pbar = tqdm(total=None)

    def bar_update(block_num, block_size, total_size):
        if pbar.total is None:
            if total_size:
                pbar.total = total_size
        progress_bytes = block_num * block_size
        pbar.update(progress_bytes - pbar.n)

    return bar_update


@lock.lock_scope()
def download_url_to_local(url, filename, root_folder, md5):
    ensure_dir(root_folder)
    file_path = os.path.join(root_folder, filename)
    if check_file_exist(file_path, md5):
        print('Data file has been downloaded and verified')
    else:
        try:
            print('Downloading ' + url + ' to ' + file_path)
            urllib.request.urlretrieve(url,
              file_path, reporthook=(_progress()))
        except (urllib.error.URLError, IOError) as e:
            try:
                raise e
            finally:
                e = None
                del e

        if not check_file_exist(file_path, md5):
            raise RuntimeError('File downloads failed.')


def check_file_exist(file_path, md5):
    if not os.path.isfile(file_path):
        return False
    if md5 is None:
        return True
    return check_md5(file_path, md5)


def calculate_md5(file_path, chunk_size=1048576):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as (f):
        for chunk in iter(lambda : f.read(chunk_size), ''):
            md5.update(chunk)

    return md5.hexdigest()


def check_md5(file_path, md5, **kwargs):
    return md5 == calculate_md5(file_path, **kwargs)


def get_random_list(n):
    return list(np.random.permutation(range(n)))


def get_order_list(n):
    return [i for i in range(n)]


def collate_batch(batch):
    """Puts each data field into a tensor with outer dimension batch size"""
    real_size = len(batch)
    elem = batch[0]
    elem_type = type(elem)
    if isinstance(elem, jt.Var):
        if elem.ndim == 1:
            temp_data = np.stack([data.numpy() for data in batch], 0)
            temp_data = np.squeeze(temp_data, -1)
            return jt.array(temp_data)
        temp_data = np.stack([data.numpy() for data in batch], 0)
        return jt.array(temp_data)
    if elem_type is np.ndarray:
        temp_data = np.stack([data for data in batch], 0)
        return temp_data
    if np.issubdtype(elem_type, np.integer):
        return np.int32(batch)
    if isinstance(elem, int):
        return np.int32(batch)
    if isinstance(elem, float):
        return np.float32(batch)
    if isinstance(elem, str):
        return batch
    if isinstance(elem, Mapping):
        return {key:collate_batch([d[key] for d in batch]) for key in elem}
    if isinstance(elem, tuple):
        transposed = zip(*batch)
        return tuple((collate_batch(samples) for samples in transposed))
    if isinstance(elem, Sequence):
        transposed = zip(*batch)
        return [collate_batch(samples) for samples in transposed]
    if isinstance(elem, Image.Image):
        temp_data = np.stack([np.array(data) for data in batch], 0)
        return temp_data
    raise TypeError(f"Not support type <{elem_type.__name__}>")