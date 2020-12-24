# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/ranking_mp.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 644 bytes
__doc__ = '\n    Running Most Popular Recommender [Item Recommendation]\n\n    - Cross Validation\n    - Simple\n\n'
from caserec.recommenders.item_recommendation.most_popular import MostPopular
from caserec.utils.cross_validation import CrossValidation
db = '../../datasets/ml-100k/u.data'
folds_path = '../../datasets/ml-100k/'
tr = '../../datasets/ml-100k/folds/0/train.dat'
te = '../../datasets/ml-100k/folds/0/test.dat'
recommender = MostPopular(as_binary=True)
CrossValidation(input_file=db, recommender=recommender, dir_folds=folds_path, header=1, k_folds=5).compute()
MostPopular(tr, te, as_binary=True).compute()