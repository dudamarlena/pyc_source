# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/rating_prediction_mf.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 1091 bytes
__doc__ = '\n    Running MF / SVD Recommenders [Rating Prediction]\n\n    - Cross Validation\n    - Simple\n\n'
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