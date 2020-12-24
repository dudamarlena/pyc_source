# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/taar/recommenders/collaborative_recommender.py
# Compiled at: 2018-02-13 11:08:06
# Size of source mod 2**32: 4433 bytes
import logging, numpy as np, operator as op
from .base_recommender import BaseRecommender
from .utils import fetch_json
ADDON_MODEL_URL = 'https://s3-us-west-2.amazonaws.com/telemetry-public-analysis-2/telemetry-ml/addon_recommender/item_matrix.json'
ADDON_MAPPING_URL = 'https://s3-us-west-2.amazonaws.com/telemetry-public-analysis-2/telemetry-ml/addon_recommender/addon_mapping.json'
logger = logging.getLogger(__name__)

def java_string_hashcode(s):
    h = 0
    for c in s:
        h = 31 * h + ord(c) & 4294967295

    return (h + 2147483648 & 4294967295) - 2147483648


def positive_hash(s):
    return java_string_hashcode(s) & 8388607


class CollaborativeRecommender(BaseRecommender):
    __doc__ = ' The addon recommendation interface to the collaborative filtering model.\n\n    Usage example::\n\n        recommender = CollaborativeRecommender()\n        dists = recommender.recommend(client_info)\n    '

    def __init__(self):
        self.addon_mapping = fetch_json(ADDON_MAPPING_URL)
        if self.addon_mapping is None:
            logger.error('Cannot download the addon mapping file {}'.format(ADDON_MAPPING_URL))
        self.raw_item_matrix = fetch_json(ADDON_MODEL_URL)
        if self.addon_mapping is None:
            logger.error('Cannot download the model file {}'.format(ADDON_MODEL_URL))
        self.model = None
        self._build_model()

    def _build_model(self):
        if self.raw_item_matrix is None:
            return
        num_rows = len(self.raw_item_matrix)
        num_cols = len(self.raw_item_matrix[0]['features'])
        self.model = np.zeros(shape=(num_rows, num_cols))
        for index, row in enumerate(self.raw_item_matrix):
            self.model[index, :] = row['features']

    def can_recommend(self, client_data, extra_data={}):
        if self.raw_item_matrix is None or self.model is None or self.addon_mapping is None:
            return False
        if len(client_data.get('installed_addons', [])) > 0:
            return True
        return False

    def recommend(self, client_data, limit, extra_data={}):
        installed_addons_as_hashes = [positive_hash(addon_id) for addon_id in client_data.get('installed_addons', [])]
        query_vector = np.array([1.0 if entry.get('id') in installed_addons_as_hashes else 0.0 for entry in self.raw_item_matrix])
        user_factors = np.matmul(query_vector, self.model)
        user_factors_transposed = np.transpose(user_factors)
        distances = {}
        for addon in self.raw_item_matrix:
            hashed_id = addon.get('id')
            str_hashed_id = str(hashed_id)
            if not hashed_id in installed_addons_as_hashes:
                if not str_hashed_id not in self.addon_mapping:
                    if self.addon_mapping[str_hashed_id].get('isWebextension', False) is False:
                        pass
                    else:
                        dist = np.dot(user_factors_transposed, addon.get('features'))
                        addon_id = self.addon_mapping[str_hashed_id].get('id')
                        distances[addon_id] = dist

        sorted_dists = sorted(distances.items(), key=op.itemgetter(1), reverse=True)
        return [(s[0], s[1]) for s in sorted_dists[:limit]]