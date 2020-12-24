# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/ranking_mp.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 644 bytes
"""
    Running Most Popular Recommender [Item Recommendation]

    - Cross Validation
    - Simple

"""
from caserec.recommenders.item_recommendation.most_popular import MostPopular
from caserec.utils.cross_validation import CrossValidation
db = '../../datasets/ml-100k/u.data'
folds_path = '../../datasets/ml-100k/'
tr = '../../datasets/ml-100k/folds/0/train.dat'
te = '../../datasets/ml-100k/folds/0/test.dat'
recommender = MostPopular(as_binary=True)
CrossValidation(input_file=db, recommender=recommender, dir_folds=folds_path, header=1, k_folds=5).compute()
MostPopular(tr, te, as_binary=True).compute()