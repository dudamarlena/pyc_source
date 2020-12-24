# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/tests/sfts.py
# Compiled at: 2018-06-29 13:19:30
# Size of source mod 2**32: 1046 bytes
import os, numpy as np, pandas as pd
from pyFTS.common import Util
from pyFTS.benchmarks import benchmarks as bchmk
os.chdir('/home/petronio/Downloads')
data = pd.read_csv('dress_data.csv', sep=',')
data['date'] = pd.to_datetime((data['date']), format='%Y%m%d')
from pyFTS.models.seasonal import sfts, cmsfts, SeasonalIndexer, common
ix = SeasonalIndexer.DateTimeSeasonalIndexer('date', [common.DateTime.day_of_week], [
 None, None],
  'a', name='weekday')
from pyFTS.partitioners import Grid
fs = Grid.GridPartitioner(data=data, npart=10, indexer=ix)
model = cmsfts.ContextualMultiSeasonalFTS(indexer=ix, partitioner=fs)
model.fit(data)
print(model)
print(model.predict(data))
from pyFTS.benchmarks import Measures
Measures.get_point_statistics(data, model)