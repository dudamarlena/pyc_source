# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caserec/recommenders/item_recommendation/ensemble_average.py
# Compiled at: 2019-08-20 09:47:28
# Size of source mod 2**32: 656 bytes
__doc__ = '"\n    Ensemble Average\n    [Item Recommendation (Ranking)]\n\n    Literature:\n        Arthur Fortes da Costa and Marcelo G. Manzato:\n        Multimodal Interactions in Recommender Systems: An Ensembling Approach\n        BRACIS 2014.\n        https://ieeexplore.ieee.org/document/6984809/\n\n'
from caserec.recommenders.item_recommendation.base_item_recommendation import BaseItemRecommendation
__author__ = 'Arthur Fortes <fortes.arthur@gmail.com>'

class EnsembleAverage(BaseItemRecommendation):
    """EnsembleAverage"""
    raise NotImplemented