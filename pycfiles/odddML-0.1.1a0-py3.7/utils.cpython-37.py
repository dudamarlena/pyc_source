# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\odddML\utils.py
# Compiled at: 2019-12-20 05:06:33
# Size of source mod 2**32: 937 bytes
import numpy as np, cv2

def preprocess_img(fname, im_shape):
    """
    ### Arguments
        fname: image path
        imshape: the shape you want your image to be resized into, expects tuple with width and height ex. (100, 100).
    ##### Returns: Resized and normalized image in Grayscale with shape (width, height, 1)
    #### Usage: Use it to resize your images. We are using it by iteratively passing image paths into it to get back preprocessed images. 
    """
    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, dsize=im_shape)
    img = np.array(img)
    img = img.reshape(im_shape[0], im_shape[1], 1)
    img = img / 255.0
    return img


def convert_to_one_hot(Y, C):
    """
    ### Arguments
        Y: Array with you labels
        C: The number of classes
    ##### Returns: returns one_hot_encoded labels
    """
    Y = np.eye(C)[Y.reshape(-1)]
    return Y