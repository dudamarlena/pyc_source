# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/tests/general.py
# Compiled at: 2019-04-26 15:45:08
# Size of source mod 2**32: 4240 bytes
import os, numpy as np, matplotlib.pylab as plt, pandas as pd
from pyFTS.common import Util as cUtil, FuzzySet
from pyFTS.partitioners import Grid, Entropy, Util as pUtil, Simple
from pyFTS.benchmarks import benchmarks as bchmk, Measures
from pyFTS.models import chen, yu, cheng, ismailefendi, hofts, pwfts, tsaur, song, sadaei
from pyFTS.common import Transformations, Membership
from pyFTS.fcm import fts, common, GA
from pyFTS.data import Enrollments, TAIEX
import pandas as pd
df = pd.read_csv('https://query.data.world/s/7zfy4d5uep7wbgf56k4uu5g52dmvap', sep=';')
data = df['glo_avg'].values[:12000]
fs = Grid.GridPartitioner(data=data, npart=35, func=(Membership.trimf))
GA.parameters['num_concepts'] = 35
GA.parameters['order'] = 2
GA.parameters['partitioner'] = fs
GA.execute('TAIEX', data)