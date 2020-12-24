# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\phantom\similarity.py
# Compiled at: 2019-05-28 10:48:42
# Size of source mod 2**32: 3213 bytes
"""
Hashing techniques aplicable to images.
"""
import cv2, numpy as np, scipy.fftpack

def compare(h1, h2, threshold=12):
    """
    Compare two hashes (in numpy array form) and return True for equivalence,
    False otherwise.

    :param h1: first hash to compare
    :param h2: second hash to compare
    :param threshold: similarity threhshold on the Hamming distance
    """
    return np.sum(h1 ^ h2) <= threshold


def a_hash(source):
    """
    Image similarity hash based on the average colour of an image.

    Read more on:

    http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    """
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (8, 8), interpolation=(cv2.INTER_AREA))
    average = np.average(gray)
    hash_ = np.zeros((8, 8), dtype=(np.uint8))
    hash_[gray > average] = 1
    return hash_


def d_hash(source):
    """
    Image similarity hash based on horizontal gradients.

    Read more on:

    http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html
    """
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (9, 8), interpolation=(cv2.INTER_AREA))
    hash_ = gray[:, :8] < gray[:, 1:9]
    return hash_.astype(np.uint8)


def p_hash(source):
    """
    Image similarity hash based on the DCT components of an image.

    Read more on:

    http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    """
    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (32, 32), interpolation=(cv2.INTER_AREA))
    gray = scipy.fftpack.dct(gray, type=2, axis=0)
    gray = scipy.fftpack.dct(gray, type=2, axis=1)
    average = np.median(gray[:8, :8])
    hash_ = np.zeros((8, 8), dtype=(np.uint8))
    hash_[gray[:8, :8] > average] = 1
    return hash_