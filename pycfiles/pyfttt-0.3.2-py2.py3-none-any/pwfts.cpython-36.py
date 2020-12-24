# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/tests/pwfts.py
# Compiled at: 2018-07-02 17:52:15
# Size of source mod 2**32: 2220 bytes
import os, numpy as np, pandas as pd, matplotlib as plt, matplotlib.pyplot as plt, importlib
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pyFTS.common import Util
from pyFTS.data import TAIEX
taiex = TAIEX.get_data()
train = taiex[:3000]
test = taiex[3000:3200]
from pyFTS.common import Transformations
tdiff = Transformations.Differential(1)
from pyFTS.benchmarks import benchmarks as bchmk, Measures
from pyFTS.models import pwfts, hofts, ifts
from pyFTS.partitioners import Grid, Util as pUtil
fs = Grid.GridPartitioner(data=train, npart=30)
model1 = hofts.HighOrderFTS(partitioner=fs, lags=[1, 2])
model1.shortname = '1'
model2 = pwfts.ProbabilisticWeightedFTS(partitioner=fs, lags=[1, 2])
model2.shortname = '2'
model1.fit(train)
model2.fit(train)
for model in [model1, model2]:
    print(model.shortname)
    print(Measures.get_point_statistics(test, model))