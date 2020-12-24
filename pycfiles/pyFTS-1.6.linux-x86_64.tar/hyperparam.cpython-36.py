# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/tests/hyperparam.py
# Compiled at: 2019-03-20 10:17:36
# Size of source mod 2**32: 3212 bytes
import numpy as np, pandas as pd
from pyFTS.hyperparam import GridSearch, Evolutionary

def get_dataset():
    from pyFTS.data import SONDA
    data = pd.read_csv('https://query.data.world/s/6xfb5useuotbbgpsnm5b2l3wzhvw2i', sep=';')
    return (
     'SONDA.glo_avg', data['glo_avg'].values)


hyperparams = {'order':[
  3], 
 'partitions':np.arange(10, 100, 3), 
 'partitioner':[
  1], 
 'mf':[
  1], 
 'lags':np.arange(2, 7, 1), 
 'alpha':np.arange(0.0, 0.5, 0.05)}
nodes = [
 '192.168.0.106', '192.168.0.110', '192.168.0.107']
datsetname, dataset = get_dataset()
ret = Evolutionary.execute(datsetname, dataset, ngen=30,
  npop=20,
  pcruz=0.5,
  pmut=0.3,
  window_size=10000,
  train_rate=0.9,
  increment_rate=1,
  experiments=1,
  distributed='dispy',
  nodes=nodes)