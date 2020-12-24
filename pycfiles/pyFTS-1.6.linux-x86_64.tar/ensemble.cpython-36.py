# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/tests/ensemble.py
# Compiled at: 2019-03-21 15:53:44
# Size of source mod 2**32: 4383 bytes
import os, numpy as np, pandas as pd
from pyFTS.partitioners import Grid
from pyFTS.common import Transformations
from pyFTS.models import chen, hofts
from pyFTS.models.incremental import IncrementalEnsemble, TimeVariant
from pyFTS.data import AirPassengers, artificial
from pyFTS.models.ensemble import ensemble
from pyFTS.models import hofts
from pyFTS.data import TAIEX
data = TAIEX.get_data()
model = ensemble.EnsembleFTS()
for k in (15, 25, 35):
    for order in (1, 2):
        fs = Grid.GridPartitioner(data=data, npart=k)
        tmp = hofts.WeightedHighOrderFTS(partitioner=fs)
        tmp.fit(data)
        model.append_model(tmp)

forecasts = model.predict(data, type='interval', method='quantile', alpha=0.05)
from pyFTS.benchmarks import benchmarks as bchmk
print(forecasts)