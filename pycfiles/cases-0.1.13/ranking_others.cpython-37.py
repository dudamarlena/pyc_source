# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/ranking_others.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 255 bytes
__doc__ = '\n\n    Running item recommendation algorithms\n\n'
from caserec.recommenders.item_recommendation.bprmf import BprMF
tr = '../../datasets/ml-100k/folds/0/train.dat'
te = '../../datasets/ml-100k/folds/0/test.dat'
BprMF(tr, te, batch_size=30).compute()