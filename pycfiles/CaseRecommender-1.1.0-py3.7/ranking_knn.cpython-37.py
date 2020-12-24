# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/ranking_knn.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 1627 bytes
"""
    Running KNN Recommenders [Item Recommendation]

    - Cross Validation
    - Simple

"""
from caserec.recommenders.item_recommendation.user_attribute_knn import UserAttributeKNN
from caserec.recommenders.item_recommendation.item_attribute_knn import ItemAttributeKNN
from caserec.recommenders.item_recommendation.itemknn import ItemKNN
from caserec.recommenders.item_recommendation.userknn import UserKNN
from caserec.utils.cross_validation import CrossValidation
db = '../../datasets/ml-100k/u.data'
folds_path = '../../datasets/ml-100k/'
metadata_item = '../../datasets/ml-100k/db_item_subject.dat'
sm_item = '../../datasets/ml-100k/sim_item.dat'
metadata_user = '../../datasets/ml-100k/metadata_user.dat'
sm_user = '../../datasets/ml-100k/sim_user.dat'
tr = '../../datasets/ml-100k/folds/0/train.dat'
te = '../../datasets/ml-100k/folds/0/test.dat'
UserAttributeKNN(tr, te, metadata_file=metadata_user).compute()