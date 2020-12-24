# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/tests/spark.py
# Compiled at: 2019-01-23 10:21:41
# Size of source mod 2**32: 4708 bytes
import numpy as np, pandas as pd, time
from pyFTS.data import Enrollments, TAIEX, SONDA
from pyFTS.partitioners import Grid, Simple
from pyFTS.common import Util
from pyspark import SparkConf
from pyspark import SparkContext
import os
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/bin/python3'
data = SONDA.get_dataframe()
data = data[['datahora', 'glo_avg']]
data = data[(~(np.isnan(data['glo_avg']) | np.equal(data['glo_avg'], 0.0)))]
train = data.iloc[:1500000]
test = data.iloc[1500000:]
from pyFTS.models.multivariate import common, variable, wmvfts
from pyFTS.models.seasonal import partitioner as seasonal
from pyFTS.models.seasonal.common import DateTime
from pyFTS.partitioners import Grid
import matplotlib.pyplot as plt
sp = {'seasonality':DateTime.day_of_year, 
 'names':['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}
vmonth = variable.Variable('Month', data_label='datahora', partitioner=(seasonal.TimeGridPartitioner), npart=12, alpha_cut=0.25, data=train,
  partitioner_specific=sp)
sp = {'seasonality':DateTime.minute_of_day, 
 'names':[str(k) for k in range(0, 24)]}
vhour = variable.Variable('Hour', data_label='datahora', partitioner=(seasonal.TimeGridPartitioner), npart=24, alpha_cut=0.2, data=train,
  partitioner_specific=sp)
vavg = variable.Variable('Radiation', data_label='glo_avg', alias='R', partitioner=(Grid.GridPartitioner),
  npart=35,
  alpha_cut=0.3,
  data=train)
model = wmvfts.WeightedMVFTS(explanatory_variables=[vmonth, vhour, vavg], target_variable=vavg)
_s1 = time.time()
model.fit(data, distributed='spark', url='spark://192.168.0.106:7077', num_batches=5)
_s2 = time.time()
print(_s2 - _s1)
Util.persist_obj(model, 'sonda_wmvfts')
from pyFTS.benchmarks import Measures