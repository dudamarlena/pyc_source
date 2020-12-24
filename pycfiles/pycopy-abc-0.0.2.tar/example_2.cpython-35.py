# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/pycopula/example_2.py
# Compiled at: 2018-11-08 17:34:29
# Size of source mod 2**32: 1538 bytes
import sys, time
sys.path.insert(0, '..')
import scipy, pandas as pd
from pycopula.visualization import pdf_2d, cdf_2d, concentrationFunction
from pycopula.simulation import simulate
from pycopula.copula import ArchimedeanCopula, GaussianCopula, StudentCopula
import numpy as np, matplotlib.pyplot as plt
data = pd.read_csv('mydata.csv', sep=';').values[:, 1:]
data = [[x.replace(',', '.') for x in row] for row in data]
data = np.random.normal(size=1000)
data = np.vstack((data, np.cos(data))).T
data = np.asarray(data).astype(np.float)
print(data.shape)
print('Begin')
archimedean = StudentCopula(dim=2)
elapsedTime = time.time()
archimedean.fit(data, method='cmle', df_fixed=False)
elapsedTime = time.time() - elapsedTime
print(elapsedTime)
print(archimedean)
sys.exit()
print('End')
clayton = ArchimedeanCopula(family='clayton', dim=2)
boundAlpha = [0, None]
boundLambda = [0, 0.5]
bounds = [boundAlpha, boundLambda]
paramX1 = {'a': None, 'scale': 1.2}
paramX2 = {'scale': None}
hyperParams = [paramX1, paramX2]
gamma = scipy.stats.gamma
expon = scipy.stats.expon
print(clayton.fit(data, method='ifm', marginals=[gamma, expon], hyper_param=hyperParams, hyper_param_bounds=bounds))
print(clayton)