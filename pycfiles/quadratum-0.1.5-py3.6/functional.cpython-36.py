# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quadratum/functional.py
# Compiled at: 2019-04-08 05:36:32
# Size of source mod 2**32: 2672 bytes
from __future__ import division
import os, numpy as np
from cv2 import imread
from cv2 import imencode
from skimage.color import gray2rgb
from skimage.transform import resize

def validate_image(path, min_size=2, allow_gray=False):
    if not os.path.isfile(path):
        return False
    else:
        image = imread(path)
        if image is None:
            return False
        is_valid, istr = imencode('.jpg', image)
        if not is_valid:
            return False
        try:
            h, w = image.shape
            c = 1
        except ValueError:
            try:
                h, w, c = image.shape
            except ValueError:
                return False

        if not allow_gray:
            if c < 3:
                return False
        if h < min_size or w < min_size:
            return False
        if image.var() < 1:
            return False
        if not (istr[0] == 255 and istr[1] == 216 and istr[(len(istr) - 2)] == 255 and istr[(len(istr) - 1)] == 217):
            return False
        return True


def whiten(image):
    try:
        h, w, c = image.shape
    except:
        h, w = image.shape
        return gray2rgb(image)
    else:
        if c == 3:
            return image
        if c == 4:
            alpha = image[:, :, 3].astype(np.float32)[:, :, np.newaxis] / 255
            image = image[:, :, :3]
            canvas = np.ones((h, w, 3), dtype=(np.float32)) * 255
            composed = alpha * image + (1 - alpha) * canvas
            return composed.astype(np.uint8)
        raise ValueError('Invalid image channel size.')


def invert(image):
    return image.max() - image


def dominofy(image, threshold=2):
    h, w, _ = image.shape
    if h / w < threshold:
        if w / h < threshold:
            return image
    if h > w:
        cy = int(h / 2)
        size = w * threshold / 2
        return image[int(cy - size):int(cy + size), :, :]
    else:
        cx = int(w / 2)
        size = h * threshold / 2
        return image[:, int(cx - size):int(cx + size), :]


def contain(image, size, fill='white'):
    if type(size) == int:
        size = (
         size, size)
    else:
        bh = size[0]
        bw = size[1]
        if fill == 'white':
            canvas = np.ones((bh, bw, 3), dtype=(np.uint8)) * 255
        else:
            if fill == 'black':
                canvas = np.zeros((bh, bw, 3), dtype=(np.uint8))
            else:
                raise ValueError('Invalid fill option.')
        ih, iw, _ = image.shape
        ir = ih / iw
        br = bh / bw
        if ir > br:
            image = resize(image, (bh, int(bh / ir)), mode='reflect', preserve_range=True)
        else:
            image = resize(image, (int(bw * ir), bw), mode='reflect', preserve_range=True)
    h, w, _ = image.shape
    canvas[int(bh / 2 - h / 2):int(bh / 2 + h / 2), int(bw / 2 - w / 2):int(bw / 2 + w / 2), :] = image
    return canvas