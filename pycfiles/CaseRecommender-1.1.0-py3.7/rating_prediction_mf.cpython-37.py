# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/rating_prediction_mf.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 1091 bytes
"""
    Running MF / SVD Recommenders [Rating Prediction]

    - Cross Validation
    - Simple

"""
from caserec.recommenders.rating_prediction.svdplusplus import SVDPlusPlus
from caserec.recommenders.rating_prediction.nnmf import NNMF
from caserec.recommenders.rating_prediction.matrixfactorization import MatrixFactorization
from caserec.utils.cross_validation import CrossValidation
db = '../../datasets/ml-100k/u.data'
folds_path = '../../datasets/ml-100k/'
metadata_item = '../../datasets/ml-100k/db_item_subject.dat'
sm_item = '../../datasets/ml-100k/sim_item.dat'
metadata_user = '../../datasets/ml-100k/metadata_user.dat'
sm_user = '../../datasets/ml-100k/sim_user.dat'
tr = '../../datasets/ml-100k/folds/0/train.dat'
te = '../../datasets/ml-100k/folds/0/test.dat'
NNMF(tr, te, factors=20).compute()