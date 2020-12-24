# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/examples/util/mnist.py
# Compiled at: 2012-10-11 20:17:38
import os, struct
from array import array
from cvxopt.base import matrix

def read(digits, dataset='training', path='.'):
    """
    Python function for importing the MNIST data set.
    """
    if dataset is 'training':
        fname_img = os.path.join(path, 'train-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
    else:
        if dataset is 'testing':
            fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
            fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
        else:
            raise ValueError, "dataset must be 'testing' or 'training'"
        flbl = open(fname_lbl, 'rb')
        magic_nr, size = struct.unpack('>II', flbl.read(8))
        lbl = array('b', flbl.read())
        flbl.close()
        fimg = open(fname_img, 'rb')
        magic_nr, size, rows, cols = struct.unpack('>IIII', fimg.read(16))
        img = array('B', fimg.read())
        fimg.close()
        ind = [ k for k in xrange(size) if lbl[k] in digits ]
        images = matrix(0, (len(ind), rows * cols))
        labels = matrix(0, (len(ind), 1))
        for i in xrange(len(ind)):
            images[i, :] = img[ind[i] * rows * cols:(ind[i] + 1) * rows * cols]
            labels[i] = lbl[ind[i]]

    return (
     images, labels)