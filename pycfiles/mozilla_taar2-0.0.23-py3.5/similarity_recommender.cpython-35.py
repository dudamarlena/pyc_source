# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/taar/recommenders/similarity_recommender.py
# Compiled at: 2018-02-19 13:09:33
# Size of source mod 2**32: 9400 bytes
import logging, numpy as np
from ..recommenders import utils
from .base_recommender import BaseRecommender
from scipy.spatial import distance
FLOOR_DISTANCE_ADJUSTMENT = 0.001
CATEGORICAL_FEATURES = [
 'geo_city', 'locale', 'os']
CONTINUOUS_FEATURES = ['subsession_length', 'bookmark_count', 'tab_open_count', 'total_uri', 'unique_tlds']
S3_BUCKET = 'telemetry-parquet'
DONOR_LIST_KEY = 'taar/similarity/donors.json'
LR_CURVES_SIMILARITY_TO_PROBABILITY = 'taar/similarity/lr_curves.json'
logger = logging.getLogger(__name__)

class SimilarityRecommender(BaseRecommender):
    __doc__ = ' A recommender class that returns top N addons based on the\n    client similarity with a set of candidate addon donors.\n\n    Several telemetry fields are used to compute pairwise similarity\n    with the donors and similarities are converted into a likelihood\n    ratio of being a good match versus not being a good match. These\n    quantities are then used to rank specific addons for\n    recommendation.\n\n    This will load a json file containing updated list of addon donors\n    updated periodically by a separate weekly process using\n    Longitdudinal Telemetry data.\n\n    This recommender may provide useful recommendations when\n    collaborative_recommender may not work.\n    '

    def __init__(self):
        self.donors_pool = utils.get_s3_json_content(S3_BUCKET, DONOR_LIST_KEY)
        if self.donors_pool is None:
            logger.error('Cannot download the donor list: {}'.format(DONOR_LIST_KEY))
        self.lr_curves = utils.get_s3_json_content(S3_BUCKET, LR_CURVES_SIMILARITY_TO_PROBABILITY)
        if self.lr_curves is None:
            logger.error('Cannot download the lr curves: {}'.format(LR_CURVES_SIMILARITY_TO_PROBABILITY))
        self.build_features_caches()

    def build_features_caches(self):
        """This function build two feature cache matrices.

        One matrix is for the continuous features and the other is for
        the categorical features. This is needed to speed up the similarity
        recommendation process."""
        if self.donors_pool is None or self.lr_curves is None:
            return
        self.num_donors = len(self.donors_pool)
        self.continuous_features = np.zeros((self.num_donors, len(CONTINUOUS_FEATURES)))
        for idx, d in enumerate(self.donors_pool):
            features = [d.get(specified_key) for specified_key in CONTINUOUS_FEATURES]
            self.continuous_features[idx] = features

        self.categorical_features = np.zeros((self.num_donors, len(CATEGORICAL_FEATURES)), dtype='object')
        for idx, d in enumerate(self.donors_pool):
            features = [d.get(specified_key) for specified_key in CATEGORICAL_FEATURES]
            self.categorical_features[idx] = np.array([features], dtype='object')

    def can_recommend(self, client_data, extra_data={}):
        if self.donors_pool is None or self.lr_curves is None:
            return False
        REQUIRED_FIELDS = CATEGORICAL_FEATURES + CONTINUOUS_FEATURES
        has_fields = all([client_data.get(f, None) is not None for f in REQUIRED_FIELDS])
        if not has_fields:
            logger.error('Unusable client data encountered')
        return has_fields

    def get_lr(self, score):
        """Compute a :float: likelihood ratio from a provided similarity score when compared
        to two probability density functions which are computed and pre-loaded during init.

        The numerator indicates the probability density that a particular similarity score
        corresponds to a 'good' addon donor, i.e. a client that is similar in the sense of
        telemetry variables. The denominator indicates the probability density that a particular
        similarity score corresponds to a 'poor' addon donor

        :param score: A similarity score between a pair of objects.
        :returns: The approximate float likelihood ratio corresponding to provided score.
        """
        lr_curves_cache = np.array([s[0] for s in self.lr_curves])
        idx = np.argmin(abs(score - lr_curves_cache))
        numer_val = self.lr_curves[idx][1][0]
        denum_val = self.lr_curves[idx][1][1]
        return float(numer_val) / float(denum_val)

    def compute_clients_dist(self, client_data):
        client_categorical_feats = [client_data.get(specified_key) for specified_key in CATEGORICAL_FEATURES]
        client_continuous_feats = [client_data.get(specified_key) for specified_key in CONTINUOUS_FEATURES]
        cont_features = distance.cdist(self.continuous_features, np.array([client_continuous_feats]), 'canberra')
        cat_features = distance.cdist(self.categorical_features, np.array([client_categorical_feats]), lambda x, y: distance.hamming(x, y))
        return (cont_features + FLOOR_DISTANCE_ADJUSTMENT) * cat_features

    def get_similar_donors(self, client_data):
        """Computes a set of :float: similarity scores between a client and a set of candidate
        donors for which comparable variables have been measured.

        A custom similarity metric is defined in this function that combines the Hamming distance
        for categorical variables with the Canberra distance for continuous variables into a
        univariate similarity metric between the client and a set of candidate donors loaded during
        init.

        :param client_data: a client data payload including a subset fo telemetry fields.
        :return: the sorted approximate likelihood ratio (np.array) corresponding to the
                 internally computed similarity score and a list of indices that link
                 each LR score with the related donor in the |self.donors_pool|.
        """
        distances = self.compute_clients_dist(client_data)
        lrs_from_scores = np.array([self.get_lr(distances[i]) for i in range(self.num_donors)])
        indices = (-lrs_from_scores).argsort()
        return (lrs_from_scores[indices], indices)

    def recommend(self, client_data, limit, extra_data={}):
        donor_set_ranking, indices = self.get_similar_donors(client_data)
        donor_log_lrs = np.log(donor_set_ranking)
        if donor_log_lrs[0] < 0.1:
            logger.warning('Addons recommended with very low similarity score, perhaps donor set is unrepresentative', extra={'maximum_similarity': donor_set_ranking[0]})
        index_lrs_iter = zip(indices[(donor_log_lrs > 0.0)], donor_log_lrs)
        recommendations = []
        for index, lrs in index_lrs_iter:
            for term in self.donors_pool[index]['active_addons']:
                candidate = (
                 term, lrs)
                recommendations.append(candidate)

            if len(recommendations) > limit:
                break

        return recommendations[:limit]