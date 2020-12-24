# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/taar/recommenders/ensemble_recommender.py
# Compiled at: 2018-02-21 21:46:01
# Size of source mod 2**32: 3461 bytes
import logging, itertools
from ..recommenders import utils
from .base_recommender import BaseRecommender
S3_BUCKET = 'telemetry-parquet'
ENSEMBLE_WEIGHTS = 'taar/ensemble/ensemble_weight.json'
logger = logging.getLogger(__name__)

class EnsembleRecommender(BaseRecommender):
    __doc__ = '\n    The EnsembleRecommender is a collection of recommenders where the\n    results from each recommendation is amplified or dampened by a\n    factor.  The aggregate results are combines and used to recommend\n    addons for users.\n    '

    def __init__(self, recommender_map):
        tmp = utils.get_s3_json_content(S3_BUCKET, ENSEMBLE_WEIGHTS)
        self._ensemble_weights = tmp['ensemble_weights']
        self.RECOMMENDER_KEYS = [
         'legacy', 'collaborative', 'similarity', 'locale']
        self._recommender_map = recommender_map

    def can_recommend(self, client_data, extra_data={}):
        """The ensemble recommender is always going to be
        available if at least one recommender is available"""
        return sum([self._recommender_map[rkey].can_recommend(client_data) for rkey in self.RECOMMENDER_KEYS])

    def recommend(self, client_data, limit, extra_data={}):
        """
        Ensemble recommendations are aggregated from individual
        recommenders.  The ensemble recommender applies a weight to
        the recommendation outputs of each recommender to reorder the
        recommendations to be a better fit.

        The intuitive understanding is that the total space of
        recommended addons across all recommenders will include the
        'true' addons that should be recommended better than any
        individual recommender.  The ensemble method simply needs to
        weight each recommender appropriate so that the ordering is
        correct.
        """
        flattened_results = []
        for rkey in self.RECOMMENDER_KEYS:
            recommender = self._recommender_map[rkey]
            if recommender.can_recommend(client_data):
                raw_results = recommender.recommend(client_data, limit, extra_data)
                reweighted_results = []
                for guid, weight in raw_results:
                    item = (guid, weight * self._ensemble_weights[rkey])
                    reweighted_results.append(item)

                flattened_results.extend(reweighted_results)

        flattened_results.sort(key=lambda item: item[0])
        guid_grouper = itertools.groupby(flattened_results, lambda item: item[0])
        ensemble_suggestions = []
        for guid, guid_group in guid_grouper:
            weight_sum = sum([v for g, v in guid_group])
            item = (guid, weight_sum)
            ensemble_suggestions.append(item)

        ensemble_suggestions.sort(key=lambda x: -x[1])
        results = ensemble_suggestions[:limit]
        print(results, flattened_results)
        return results