# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\examples\plot_mvtsne.py
# Compiled at: 2017-12-21 13:53:05
# Size of source mod 2**32: 2303 bytes
"""
==============
Multiview tSNE
==============

An example plot of multiview tSNE, using multiples views from same data thanks
to data given in `UCI Machine Learning Repository
<https://archive.ics.uci.edu/ml/datasets/Multiple+Features>`_.
"""
import numpy as np
from matplotlib import pyplot as plt
from multiview.mvtsne import MvtSNE

def readData(filename, data_type=0):
    """
    Given a txt file, returns a numpy matrix with the values, according
    to datatype specified in data_type parameters.

    Parameters
    ----------
    filename: string
        Path or name of the txt file.
    data_type: integer, default 0
        Specifies the matrix datatype. If data_type is 0, data loaded will be
        float type. If data_type is 1, matrix datatype will be float.

    Returns
    -------
    output: ndarray
        Matrix with data loaded.
    """
    if data_type != 0:
        if data_type != 1:
            raise ValueError('data_type must be either 0 or 1. Found value %d instead.' % data_type)
    with open(filename) as (txtfile):
        result = []
        myreader = txtfile.readlines()
        for row in myreader:
            if data_type == 0:
                result.append([float(x) for x in row.split()])
            else:
                if data_type == 1:
                    result.append([int(x) for x in row.split()])

    if data_type == 0:
        return np.array(result, dtype='float')
    else:
        return np.array(result, dtype='int')


fourier = readData('mfeat-fou.txt', 0)
profcorr = readData('mfeat-fac.txt', 1)
pixels = readData('mfeat-pix.txt', 1)
morpho = readData('mfeat-mor.txt', 0)
markers = [
 'o', '2', '<', '*', 'h', 'x', 'D', '|', '_', 'v']
mypalette = ['green', 'purple', 'pink', 'blue', 'black',
 'brown', 'yellow', 'orange', 'gray', 'red']
distance = [
 False] * 4
mvtsne = MvtSNE(k=2)
projection = mvtsne.fit_transform([
 fourier, profcorr, pixels, morpho], distance)
projection = projection[0]
for i in range(10):
    plt.scatter((projection[i * 200:200 * (i + 1), 0]), (projection[i * 200:200 * (1 + i), 1]),
      c=(mypalette[i]),
      marker=(markers[i]))

plt.axis('off')
plt.show()