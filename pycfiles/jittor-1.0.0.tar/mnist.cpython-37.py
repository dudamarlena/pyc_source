# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/dataset/mnist.py
# Compiled at: 2020-04-10 04:00:28
# Size of source mod 2**32: 3117 bytes
import numpy as np, gzip
from PIL import Image
from jittor.dataset.dataset import Dataset, dataset_root
from jittor.dataset.utils import ensure_dir, download_url_to_local
import jittor as jt
import jittor.transform as trans

class MNIST(Dataset):

    def __init__(self, data_root=dataset_root + '/mnist_data/', train=True, download=True, transform=None):
        super().__init__()
        self.data_root = data_root
        self.is_train = train
        self.transform = transform
        if download == True:
            self.download_url()
        else:
            filesname = [
             'train-images-idx3-ubyte.gz',
             't10k-images-idx3-ubyte.gz',
             'train-labels-idx1-ubyte.gz',
             't10k-labels-idx1-ubyte.gz']
            self.mnist = {}
            if self.is_train:
                with gzip.open(data_root + filesname[0], 'rb') as (f):
                    self.mnist['images'] = np.frombuffer((f.read()), (np.uint8), offset=16).reshape(-1, 28, 28)
                with gzip.open(data_root + filesname[2], 'rb') as (f):
                    self.mnist['labels'] = np.frombuffer((f.read()), (np.uint8), offset=8)
            else:
                with gzip.open(data_root + filesname[1], 'rb') as (f):
                    self.mnist['images'] = np.frombuffer((f.read()), (np.uint8), offset=16).reshape(-1, 28, 28)
            with gzip.open(data_root + filesname[3], 'rb') as (f):
                self.mnist['labels'] = np.frombuffer((f.read()), (np.uint8), offset=8)
        assert self.mnist['images'].shape[0] == self.mnist['labels'].shape[0]
        self.total_len = self.mnist['images'].shape[0]
        self.set_attrs(total_len=(self.total_len))

    def __getitem__(self, index):
        img = Image.fromarray(self.mnist['images'][index]).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return (
         trans.to_tensor(img), self.mnist['labels'][index])

    def download_url(self):
        resources = [
         ('http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz', 'f68b3c2dcbeaaa9fbdd348bbdeb94873'),
         ('http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz', 'd53e105ee54ea40749a09fcbcd1e9432'),
         ('http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz', '9fb629c4189551a2d022fa330f9573f3'),
         ('http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz', 'ec29112dd5afa0611ce80d1b7f02629c')]
        for url, md5 in resources:
            filename = url.rpartition('/')[2]
            download_url_to_local(url, filename, self.data_root, md5)