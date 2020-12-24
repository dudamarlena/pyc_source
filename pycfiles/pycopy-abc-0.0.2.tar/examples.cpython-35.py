# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/pycopula/examples.py
# Compiled at: 2018-11-05 17:32:30
# Size of source mod 2**32: 695 bytes
import numpy as np, matplotlib.pyplot as plt
from matplotlib import cm
from copula import GaussianCopula
from mpl_toolkits.mplot3d import Axes3D
from pycopula.visualization import pdf_2d, cdf_2d
clayton = GaussianCopula(dim=2)
u, v, C = cdf_2d(clayton)
u, v, c = pdf_2d(clayton)
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d', title='Clayton copula CDF')
X, Y = np.meshgrid(u, v)
ax.set_zlim(0, 5)
ax.plot_surface(X, Y, c, cmap=cm.Blues)
ax.plot_wireframe(X, Y, c, color='black', alpha=0.3)
ax = fig.add_subplot(122, title='Clayton copula PDF')
ax.contour(X, Y, c, levels=np.arange(0, 5, 0.15))
plt.show()