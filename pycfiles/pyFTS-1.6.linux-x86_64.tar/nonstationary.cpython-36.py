# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/tests/nonstationary.py
# Compiled at: 2018-10-09 08:50:19
# Size of source mod 2**32: 6358 bytes
import os, numpy as np
from pyFTS.common import Membership, Transformations
from pyFTS.models.nonstationary import common, perturbation, partitioners as nspart, util
from pyFTS.models.nonstationary import nsfts, cvfts
from pyFTS.partitioners import Grid, Entropy
import matplotlib.pyplot as plt
from pyFTS.common import Util as cUtil
import pandas as pd
from pyFTS.data import TAIEX, NASDAQ, SP500, artificial, mackey_glass
datasets = {'TAIEX':TAIEX.get_data()[:4000], 
 'SP500':SP500.get_data()[10000:14000], 
 'NASDAQ':NASDAQ.get_data()[:4000], 
 'IMIV':artificial.generate_gaussian_linear(1, 0.2, 0.2, 0.05, it=100, num=40), 
 'IMIV0':artificial.generate_gaussian_linear(1, 0.2, 0.0, 0.05, vmin=0, it=100, num=40), 
 'CMIV':artificial.generate_gaussian_linear(5, 0.1, 0, 0.02, it=100, num=40), 
 'IMCV':artificial.generate_gaussian_linear(1, 0.6, 0.1, 0, it=100, num=40)}
train_split = 2000
test_length = 200
from pyFTS.common import Transformations
tdiff = Transformations.Differential(1)
boxcox = Transformations.BoxCox(0)
transformations = {'None':None, 
 'Differential(1)':tdiff, 
 'BoxCox(0)':boxcox}
from pyFTS.partitioners import Grid, Util as pUtil
from pyFTS.benchmarks import benchmarks as bchmk
from pyFTS.models import chen, hofts, pwfts, hwang
partitions = {'CMIV':{'BoxCox(0)':36, 
  'Differential(1)':11,  'None':8}, 
 'IMCV':{'BoxCox(0)':36, 
  'Differential(1)':20,  'None':16}, 
 'IMIV':{'BoxCox(0)':39, 
  'Differential(1)':12,  'None':6}, 
 'IMIV0':{'BoxCox(0)':39, 
  'Differential(1)':12,  'None':3}, 
 'NASDAQ':{'BoxCox(0)':39, 
  'Differential(1)':13,  'None':36}, 
 'SP500':{'BoxCox(0)':33, 
  'Differential(1)':7,  'None':33}, 
 'TAIEX':{'BoxCox(0)':39, 
  'Differential(1)':31,  'None':33}}
from pyFTS.models.nonstationary import partitioners as nspart, cvfts, util as nsUtil

def model_details(ds, tf, train_split, test_split):
    data = datasets[ds]
    train = data[:train_split]
    test = data[train_split:test_split]
    transformation = transformations[tf]
    fs = nspart.simplenonstationary_gridpartitioner_builder(data=train, npart=15, transformation=transformation)
    model = nsfts.NonStationaryFTS(partitioner=fs)
    model.fit(train)
    print(model)
    forecasts = model.predict(test)
    residuals = np.array(test[1:]) - np.array(forecasts[:-1])
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=[15, 10])
    axes[0].plot((test[1:]), label='Original')
    axes[0].plot((forecasts[:-1]), label='Forecasts')
    axes[0].set_ylabel('Univ. of Discourse')
    axes[1].plot(residuals)
    axes[1].set_ylabel('Error')
    handles0, labels0 = axes[0].get_legend_handles_labels()
    lgd = axes[0].legend(handles0, labels0, loc=2)
    nsUtil.plot_sets_conditional(model, test, step=10, size=[10, 7], save=True,
      file='fig.png',
      axes=(axes[2]),
      fig=fig)


model_details('SP500', 'None', 200, 400)
print('ts')