# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/pycopula/main.py
# Compiled at: 2018-11-05 17:36:10
# Size of source mod 2**32: 3931 bytes
import sys
sys.path.insert(0, '..')
from pycopula.copula import *
import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from matplotlib import cm
from pycopula.visualization import pdf_2d, cdf_2d, concentrationFunction
from pycopula.simulation import simulate
data = pd.read_csv('mydata.csv').values[:, 1:]
clayton = ArchimedeanCopula(family='clayton', dim=2)
indep = Copula(dim=2, name='frechet_up')
student = StudentCopula(dim=2)
gaussian = GaussianCopula(dim=2)
opti, params = clayton.fit(data, method='mle', marginals=[scipy.stats.gamma, scipy.stats.expon], hyper_param=[{'a': None, 'scale': 1.2}, {'scale': None}], hyper_param_bounds=[[0, None], [0, None]])
print(clayton)
gaussian.fit(data, method='cmle')
print(gaussian)
print(params)
clayton = ArchimedeanCopula(family='clayton', dim=2)
boundAlpha = [0, None]
boundGamma = [0, None]
bounds = [boundAlpha, boundGamma]
paramX1 = {'a': None, 'scale': 1.2}
paramX2 = {'scale': None}
hyperParams = [paramX1, paramX2]
gamma = scipy.stats.gamma
clayton.fit(data, method='cmle')
u, v, carchi = pdf_2d(clayton, zclip=5)
u, v, Carchi = cdf_2d(clayton)
u, v, Cgauss = cdf_2d(gaussian)
u, v, cgauss = pdf_2d(gaussian, zclip=5)
u, v, Cstudent = cdf_2d(student)
u, v, cstudent = pdf_2d(student)
print(indep)
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d', title='Student copula CDF')
X, Y = np.meshgrid(u, v)
ax.set_zlim(0, 1)
ax.plot_surface(X, Y, Cstudent, cmap=cm.Blues)
ax.plot_wireframe(X, Y, Cstudent, color='black', alpha=0.3)
ax = fig.add_subplot(122, projection='3d', title='Student copula PDF')
X, Y = np.meshgrid(u, v)
ax.set_zlim(0, 5)
ax.plot_surface(X, Y, cstudent, cmap=cm.Blues)
ax.plot_wireframe(X, Y, cstudent, color='black', alpha=0.3)
ax = fig.add_subplot(122, title='Student copula PDF')
ax.contour(X, Y, cstudent, levels=np.arange(0, 5, 0.15))
gaussian.setCovariance([[1, 0.8], [0.8, 1]])
clayton.setParameter(0.85)
sim = simulate(student, 3000)
fig = plt.figure()
plt.contour(X, Y, cstudent, levels=np.arange(0, 5, 0.15), alpha=0.4)
plt.scatter([s[0] for s in sim], [s[1] for s in sim], alpha=0.4, edgecolors='none')
plt.title('Simulation of 1000 points with Clayton copula')
plt.xlim(0, 1)
plt.ylim(0, 1)
downI, upI, tailDown, tailUp = concentrationFunction(sim)
ClaytonDown = [student.concentrationDown(x) for x in downI]
ClaytonUp = [student.concentrationUp(x) for x in upI]
plt.figure()
plt.plot(downI, tailDown, color='red', linewidth=3, label='Empirical concentration')
plt.plot(upI, tailUp, color='red', linewidth=3)
plt.plot(downI, ClaytonDown, color='blue', linewidth=1, label='Clayton concentration')
plt.plot(upI, ClaytonUp, color='blue', linewidth=1)
plt.plot([0.5, 0.5], [0, 1], color='gray', alpha=0.6, linestyle='--', linewidth=1)
plt.title('Lower-Upper tail dependence Coefficients')
plt.xlabel('Lower Tail      Upper Tail')
plt.legend(loc=0)
plt.show()