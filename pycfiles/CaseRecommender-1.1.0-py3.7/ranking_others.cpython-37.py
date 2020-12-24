# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/ranking_others.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 255 bytes
"""

    Running item recommendation algorithms

"""
from caserec.recommenders.item_recommendation.bprmf import BprMF
tr = '../../datasets/ml-100k/folds/0/train.dat'
te = '../../datasets/ml-100k/folds/0/test.dat'
BprMF(tr, te, batch_size=30).compute()