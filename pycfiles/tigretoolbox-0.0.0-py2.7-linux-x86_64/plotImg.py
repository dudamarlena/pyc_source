# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Utilities/plotImg.py
# Compiled at: 2017-06-20 08:49:49
from __future__ import division
from matplotlib import pyplot as plt
import numpy as np

class plotImg:
    """
plotImg(cube, dim) 
    plots figure 
default: progressive in slices following
    axis (dim)
Parameters 
---------- 
cube : Any 3D numpy array 

dim : ("X","Y","Z","x","y","z"), optional 
       default is "Z"
       NOTE: string arguments!
slice: int, optional
     returns page of matrix according to index
Examples:
---------
a=np.ones([3,3,3])
plotImg(a)
>>>returns plot along dim Z
plotImg(a,dim="X")
>>>returns plot along dim X
"""

    def __init__(self, cube, dim=None, slice=None):
        self.cube = cube
        self.dim = dim
        self.slice = slice
        self.dimint = None
        self.dimlist = ['X', 'Y', 'Z', 'x', 'y', 'z', None]
        if self.slice == None:
            self.run()
        if self.slice != None:
            self.slicer()
        return

    def run(self):
        if self.dim not in self.dimlist:
            raise NameError('check inputs for dim, should be string.')
        if self.dim in (None, 'Z', 'z'):
            self.dimint = 2
            self.dimlist = ['X', 'Y', 'Z']
            self.run_plot()
        if self.dim in ('X', 'x'):
            self.dimint = 0
            self.dimlist = ['Y', 'Z', 'X']
            self.run_plot()
        if self.dim in ('Y', 'y'):
            self.dimint = 1
            self.dimlist = ['X', 'Z', 'Y']
            self.run_plot()
        return

    def run_plot(self):
        plt.ion()
        min_val = np.amin(self.cube)
        max_val = np.amax(self.cube)
        dim = self.cube.shape
        for i in range(dim[self.dimint]):
            plt.clf()
            if self.dimint == 2:
                plt.imshow(np.squeeze(self.cube[:, :, i]), cmap=plt.cm.gray, origin='lower', vmin=min_val, vmax=max_val)
            if self.dimint == 1:
                plt.imshow(np.squeeze(self.cube[:, i].transpose()), cmap=plt.cm.gray, origin='lower', vmin=min_val, vmax=max_val)
            if self.dimint == 0:
                plt.imshow(np.squeeze(self.cube[i].transpose()), cmap=plt.cm.gray, origin='lower', vmin=min_val, vmax=max_val)
            plt.gca().get_xaxis().set_ticks([])
            plt.gca().get_yaxis().set_ticks([])
            plt.xlabel(self.dimlist[0])
            plt.ylabel(self.dimlist[1])
            plt.title(self.dimlist[2] + ':' + str(i))
            plt.colorbar()
            plt.pause(0.01)

    def slicer(self):
        if self.dim in (None, 'Z', 'z'):
            plt.matshow(self.cube[self.slice], cmap=plt.cm.gray)
            plt.show()
        if self.dim in ('X', 'x'):
            plt.matshow(self.cube[:, :, self.slice], cmap=plt.cm.gray)
            plt.show()
        if self.dim in ('Y', 'y'):
            plt.matshow(self.cube[:, self.slice], cmap=plt.cm.gray)
            plt.show()
        return