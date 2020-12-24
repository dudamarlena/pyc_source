# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/wardHierarchical.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1188 bytes
import numpy as np, scipy as sp
from sklearn.feature_extraction.image import grid_to_graph
from sklearn.cluster import AgglomerativeClustering
from sklearn.utils.testing import SkipTest
from sklearn.utils.fixes import sp_version
import time
import matplotlib.pyplot as plt

def wardHierarchical(img):
    connectivity = grid_to_graph(*img.shape)
    print('Compute structured hierarchical clustering...')
    st = time.time()
    n_clusters = 15
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward', connectivity=connectivity)
    face = sp.misc.imresize(img, 0.1) / 255.0
    X = np.reshape(img, (-1, 1))
    ward.fit(X)
    label = np.reshape(ward.labels_, face.shape)
    print('Elapsed time: ', time.time() - st)
    print('Number of pixels: ', label.size)
    print('Number of clusters: ', np.unique(label).size)
    plt.figure(figsize=(5, 5))
    plt.imshow(face, cmap=(plt.cm.gray))
    for l in range(n_clusters):
        plt.contour((label == l), contours=1, colors=[
         plt.cm.spectral(l / float(n_clusters))])

    plt.xticks(())
    plt.yticks(())
    plt.show()