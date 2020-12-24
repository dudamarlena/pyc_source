# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Utilities/plotproj.py
# Compiled at: 2017-06-20 08:49:49
from __future__ import print_function
import matplotlib.pyplot as plt, numpy as np

def plot_projections(projections):
    plt.ion()
    min_val = np.amin(projections)
    max_val = np.amax(projections)
    total_projections = projections.shape[2]
    for i in range(total_projections):
        plt.clf()
        plt.imshow(np.squeeze(projections[:, :, i]), cmap=plt.cm.gray, origin='lower', vmin=min_val, vmax=max_val)
        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])
        plt.xlabel('-> U')
        plt.ylabel('-> V')
        plt.title('Projection angle : ' + str(i * 360 / total_projections))
        plt.colorbar()
        plt.pause(0.001)


def ppslice(projections, slice=None, Dim=2):
    if slice == None:
        slice = projections.shape[2] / 2
    print(slice)
    min_val = np.amin(projections)
    max_val = np.amax(projections)
    plt.clf()
    if Dim == 0:
        plt.imshow(np.squeeze(projections[slice]), cmap=plt.cm.gray, origin='lower', vmin=min_val, vmax=max_val)
    if Dim == 1:
        plt.imshow(np.squeeze(projections[:, slice]), cmap=plt.cm.gray, origin='lower', vmin=min_val, vmax=max_val)
    if Dim == 2:
        plt.imshow(np.squeeze(projections[:, :, slice]), cmap=plt.cm.gray, origin='lower', vmin=min_val, vmax=max_val)
    plt.colorbar()
    plt.show()
    return