# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/pairwise.py
# Compiled at: 2015-07-08 07:34:06
"""
.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.

Active learning pairwise search engines
=======================================
.. autofunction:: similar
.. autofunction:: dissimilar
.. autoclass:: PairwiseFeatureLearner
"""
from __future__ import absolute_import, division, print_function
import collections
from itertools import ifilter, imap, islice
import logging
from operator import itemgetter
import math, re
from scipy.spatial.distance import cosine
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.linear_model import LogisticRegression
from dossier.fc import StringCounter
from dossier.label import CorefValue, Label
import dossier.web as web
from dossier.models.folder import Folders
from dossier.models.soft_selectors import find_soft_selectors
logger = logging.getLogger(__name__)

class similar(web.SearchEngine):
    param_schema = dict(web.SearchEngine.param_schema, **{'canopy_limit': {'type': 'int', 'default': 1000, 'min': 0, 
                        'max': 10000}, 
       'label_limit': {'type': 'int', 'default': 1000, 'min': 0, 
                       'max': 10000}})

    def __init__(self, store, label_store):
        super(similar, self).__init__()
        self.store = store
        self.label_store = label_store

    def recommendations(self):
        candidates = self.candidates()
        return add_facets(add_soft_selectors(candidates))

    def candidates(self):
        learner = PairwiseFeatureLearner(self.store, self.label_store, self.query_content_id, subtopic_id=self.query_params.get('subtopic_id'), canopy_limit=self.params['canopy_limit'], label_limit=self.params['label_limit'])
        try:
            candidate_probs = self.ranked_candidates(learner)
        except InsufficientTrainingData:
            logger.info('Falling back to plain index scan...')
            return web.engine_index_scan(self.store).set_query_id(self.query_content_id).set_query_params(self.query_params).recommendations()

        predicate = self.create_filter_predicate()
        ranked = ifilter(lambda t: predicate(t[0]), candidate_probs)
        results = imap(lambda ((cid, fc), p): learner.as_result(cid, fc, p), ranked)
        return {'results': list(islice(results, self.params['limit']))}

    def ranked_candidates(self, learner):
        return sorted(learner.probabilities(), reverse=True, key=itemgetter(1))


class dissimilar(similar):

    def ranked_candidates(self, learner):
        return sorted(learner.probabilities(), key=itemgetter(1))


def add_soft_selectors(engine_result):
    results = engine_result['results']
    ids_and_clean, fcs = [], {}
    for r in results:
        ids_and_clean.append((r[0], r[1].get('meta_clean_visible', '')))
        fcs[r[0]] = r[1]

    suggestions = find_soft_selectors(ids_and_clean)
    for s in suggestions:
        for hit in s['hits']:
            hit['title'] = get_title(fcs[hit['content_id']], default=s['phrase'])

    return dict(engine_result, **{'suggestions': suggestions})


def add_facets(engine_result, facet_features=None):
    """Adds facets to search results.

    Construct a new result payload with `facets` added as a new
    top-level property that carries a mapping from unicode strings to
    lists of content_ids.  The `facet_features` lists the names of
    :class:`~dossier.fc.StringCounter` features in each result
    :class:`~dossier.fc.FeatureCollection` to harvest phrases for the
    facets list.  If not specified, `facet_features` defaults to
    `bowNP_sip`.

    The remainder of the facet logic is handled in the UI.
    """
    if facet_features is None:
        facet_features = [
         'bowNP_sip']
    phrases = collections.defaultdict(list)
    for r in engine_result['results']:
        cid = r[0]
        fc = r[1]
        for fname in facet_features:
            for phrase in fc.get('bowNP_sip', []):
                phrases[phrase].append(cid)

    return dict(engine_result, **{'facets': dict(phrases)})


def get_title(fc, default=None):
    title = fc.get('title')
    if title is None:
        m = re.search('<title>(.*?)</title>', fc.get('meta_clean_html', ''))
        if m is not None:
            title = m.group(1)
    return title or default


class InsufficientTrainingData(Exception):
    pass


class PairwiseFeatureLearner(object):
    """A pairwise active learning model.

    This active learning model applies
    :class:`~sklearn.linear_model.LogisticRegression` on-the-fly
    as a user (or simulated user) interacts with content
    via the web services provided by :mod:`dossier.web`.

    This reads :class:`~dossier.label.Label` objects from
    :class:`~dossier.label.LabelStore` and provides predictions of
    pairwise equivalence, which can be used for coreference resolution,
    clustering, and ranking.

    .. automethod:: dossier.models.PairwiseFeatureLearner.__init__
    .. automethod:: dossier.models.PairwiseFeatureLearner.probabilities
    """

    def __init__(self, store, label_store, content_id, subtopic_id=None, canopy_limit=None, label_limit=None):
        """Build a new model.

        :param store: A store of feature collections.
        :type store: :class:`dossier.store.Store`
        :param label_store: A store of labels (ground truth data).
        :type label_store: :class:`dossier.label.LabelStore`
        :param str content_id: The query content id (which should correspond
                               to a feature collection in the ``store``).
                               If it doesn't, no results are returned.
        :param int canopy_limit: A limit on the number of results to return
                                 in the canopy (the initial index scan).
                                 This is meant to be a mechanism for resource
                                 control.
        :param int label_limit: A limit on the number of labels to use in
                                training. This is meant to be a mechanism for
                                resource control.
        """
        self.store = store
        self.label_store = label_store
        self.folders = Folders(store.kvl)
        self.query_content_id = content_id
        self.query_subtopic_id = subtopic_id
        self.query_fc = None
        self.canopy_limit = canopy_limit
        self.label_limit = label_limit
        return

    def as_result(self, cid, fc, p):
        fnames = sorted(set(self.query_fc.keys()).intersection(fc.keys()))
        intermediates = dict([ (n, {'kernel': 'cosine', 'feature1': n, 'feature2': n, 'kernel_value': None, 'weight': None, 'common_feature_values': []}) for n in fnames
                             ])
        for n in fnames:
            intermediates[n]['weight'] = self.feature_weights.get(n)

        for n, qfeat, cfeat in ((n, self.query_fc[n], fc[n]) for n in fnames):
            if not isinstance(qfeat, StringCounter) or not isinstance(cfeat, StringCounter):
                continue
            vals = set(qfeat.keys()).intersection(cfeat.keys())
            intermediates[n]['common_feature_values'] = sorted(filter(None, vals))
            all_vals = sorted(set(qfeat.keys()).union(cfeat.keys()))
            if len(all_vals) > 0:
                qcounts = [ qfeat.get(v, 0) for v in all_vals ]
                ccounts = [ cfeat.get(v, 0) for v in all_vals ]
                sim = cosine(qcounts, ccounts)
                if not math.isnan(sim):
                    intermediates[n]['kernel_value'] = sim

        return (
         cid, fc,
         {'probability': p, 
            'intermediate_model_results': intermediates.values()})

    def probabilities(self):
        """Trains a model and predicts recommendations.

        If the query feature collection could not be found or if there
        is insufficient training data, an empty list is returned.

        Otherwise, a list of content objects (tuples of content
        id and feature collection) and probabilities is returned.
        The probability is generated from the model, and reflects
        confidence of the model that the corresponding content object
        is related to the query based on the ground truth data.

        On a large database, random samples are used for training, so
        this function is not deterministic.

        :rtype: ``list`` of
          ((``content_id``, :class:`dossier.fc.FeatureCollection`),
          probability)
        """
        self.query_fc = self.store.get(self.query_content_id)
        if self.query_fc is None:
            logger.warning('Could not find FC for %s', self.query_content_id)
            return []
        else:
            candidates = self.canopy(limit=self.canopy_limit)
            if len(candidates) == 0:
                logger.info('Could not find any candidates in a canopy query by scanning the following indexes: %s', (', ').join(self.store.index_names()))
                return []
            logger.info('Fetching labels...')
            labels = list(self.labels_from_query(limit=self.label_limit))
            logger.info('Fetching FCs from labels...')
            content_objs = self.content_objs_from_labels(labels)
            indexed_labels = labels_to_indexed_coref_values(content_objs, labels)
            logger.info('Training...')
            model = self.train(content_objs, indexed_labels)
            if model is None:
                logger.info('Could not train model: insufficient training data. (query content id: %s)', self.query_content_id)
                raise InsufficientTrainingData
            feature_names, classifier, transformer = model
            return zip(candidates, self.classify(feature_names, classifier, transformer, candidates))

    def train(self, content_objs, idx_labels):
        """Trains and returns a model using sklearn.

        If there are new labels to add, they can be added, returns an
        sklearn model which can be used for prediction and getting
        features.

        This method may return ``None`` if there is insufficient
        training data to produce a model.

        :param labels: Ground truth data.
        :type labels: list of ``({-1, 1}, index1, index2)``.
        """
        if len(set([ lab[0] for lab in idx_labels ])) <= 1:
            return None
        else:
            fcs = [ fc for _, fc in content_objs ]
            feature_names = vectorizable_features(fcs)
            dis = dissimilarities(feature_names, fcs)
            phi_dicts, labels = [], []
            for coref_value, i, j in idx_labels:
                labels.append(coref_value)
                phi_dict = dict([ (name, dis[name][(i, j)]) for name in feature_names ])
                phi_dicts.append(phi_dict)

            vec = dict_vector()
            training_data = vec.fit_transform(phi_dicts)
            model = LogisticRegression(class_weight='auto', penalty='l1')
            model.fit(training_data, labels)
            self.feature_weights = dict([ (name, model.coef_[0][i]) for i, name in enumerate(feature_names)
                                        ])
            return (feature_names, model, vec)

    def classify(self, feature_names, classifier, transformer, candidates):
        """Returns ``[probability]`` in correspondence with
        ``candidates``.

        Where each ``probability`` corresponds to the probability that
        the corresponding candidate is classified with a positive label
        given the training data.

        The list returned is in correspondence with the list of
        candidates given.

        N.B. The contract of this method should be simplified by
        bundling ``feature_names``, ``classifier`` and ``transformer``
        into one thing known as "the model." ---AG
        """
        dis = {}
        for name in feature_names:
            vec = dict_vector()
            query = vec.fit_transform([get_feat(self.query_fc, name)])
            cans = vec.transform(get_feat(fc, name) for _, fc in candidates)
            dis[name] = 1 - pairwise_distances(cans, query, metric='cosine', n_jobs=1)[:, 0]

        phi_dicts = transformer.transform([ dict([ (name, dis[name][i]) for name in feature_names ]) for i in xrange(len(candidates))
                                          ])
        return classifier.predict_proba(phi_dicts)[:, 1]

    def canopy(self, limit=None):
        ids = web.streaming_sample(self.canopy_ids(limit_hint=hard_limit(limit)), limit, hard_limit(limit))
        return filter(lambda (_, fc): fc is not None, self.store.get_many(ids))

    def canopy_ids(self, limit_hint=None):
        limit_hint = limit_hint or 1000
        blacklist = set([self.query_content_id])
        cids = set()
        index_names = self.store.index_names()
        batch_size = limit_hint / 10
        progress = {}
        for idx_name in index_names:
            feat = self.query_fc.get(idx_name)
            if isinstance(feat, StringCounter):
                for name in feat:
                    if len(name) > 0:
                        progress[(idx_name, name)] = 0

        logger.info('starting index scan (query content id: %s)', self.query_content_id)
        while len(progress) > 0:
            for idx_name in index_names:
                for name in self.query_fc.get(idx_name, []):
                    key = (
                     idx_name, name)
                    if key not in progress:
                        continue
                    logger.info('[StringCounter index: %s] scanning for "%s"', idx_name, name)
                    scanner = self.store.index_scan(idx_name, name)
                    progressed = 0
                    for cid in islice(scanner, progress[key], None):
                        if progressed >= batch_size:
                            break
                        if cid not in cids and cid not in blacklist:
                            cids.add(cid)
                            progressed += 1
                            yield cid

                    if progressed == 0:
                        progress.pop(key)
                    else:
                        progress[key] += progressed

        return

    def labels_from_query(self, limit=None):
        """ContentId -> [Label]"""
        return self.infer_subtopic_labels(limit=limit)

    def infer_subtopic_labels(self, limit=None):
        cid, subid = self.query_content_id, self.query_subtopic_id
        logger.info('Inferring positive labels for: %r', (cid, subid))
        pos_labels = self.label_store.expand((cid, subid)) + list(self.positive_subtopic_labels())
        logger.info('Inferring negative labels for: %r', (cid, subid))
        neg_labels = self.negative_subtopic_labels()
        pos_sample = web.streaming_sample(pos_labels, limit, limit=hard_limit(limit))
        neg_sample = web.streaming_sample(neg_labels, limit, limit=hard_limit(limit))
        print('-' * 79)
        print('POSITIVES\n', ('\n').join(map(repr, pos_sample)), '\n')
        print('-' * 79)
        print('NEGATIVES\n', ('\n').join(map(repr, neg_sample)))
        print('-' * 79)
        return pos_sample + neg_sample

    def positive_subtopic_labels(self):
        cid, subid = self.query_content_id, self.query_subtopic_id
        subfolders = list(self.folders.parent_subfolders((cid, subid)))
        for fid, subfolder_id in subfolders:
            for cid2, subid2 in self.folders.items(fid, subfolder_id):
                yield Label(cid, cid2, Folders.DEFAULT_ANNOTATOR_ID, CorefValue.Positive, subid, subid2)
                for lab in self.label_store.directly_connected(cid2):
                    if lab.value == CorefValue.Positive and lab.subtopic_for(cid2) == subid2:
                        yield lab

    def negative_subtopic_labels(self):
        cid, subid = self.query_content_id, self.query_subtopic_id
        for lab in negative_subtopic_labels(self.label_store, self.folders, cid, subid):
            yield lab

    def content_objs_from_labels(self, labels):
        """[Label] -> [(content_id, FeatureCollection)]"""
        is_mapping = lambda obj: isinstance(obj, collections.Mapping)

        def is_valid_fc((cid, fc)):
            if fc is None:
                return False
            else:
                if sum(1 for name in fc if is_mapping(fc[name])) == 0:
                    return False
                return True

        ids = set()
        for lab in labels:
            ids.add(lab.content_id1)
            ids.add(lab.content_id2)

        return list(ifilter(is_valid_fc, self.store.get_many(ids)))


def labels_to_indexed_coref_values(content_objs, labels):
    """[(content_id, FeatureCollection)] -> [Label] -> [({-1,1}, i, j)]

    where 0 <= i, j < len(content_objs).
    """
    cids_to_idx = {}
    for i, (content_id, _) in enumerate(content_objs):
        cids_to_idx[content_id] = i

    idx = lambda cid: cids_to_idx[cid]
    labs = []
    for lab in labels:
        if lab.content_id1 in cids_to_idx and lab.content_id2 in cids_to_idx:
            labs.append((lab.value.value, idx(lab.content_id1), idx(lab.content_id2)))

    return labs


def vectorizable_features(fcs):
    """Discovers the ordered set of vectorizable features in ``fcs``.

    Returns a list of feature names, sorted lexicographically.
    Feature names are only included if the corresponding
    features are vectorizable (i.e., they are an instance of
    :class:`collections.Mapping`).
    """
    is_mapping = lambda obj: isinstance(obj, collections.Mapping)
    return sorted(set([ name for fc in fcs for name in fc if is_mapping(fc[name]) ]))


def dissimilarities(feature_names, fcs):
    """Computes the pairwise dissimilarity matrices.

    This returns a dictionary mapping each name in ``feature_names``
    to a pairwise dissimilarities matrix. The dissimilaritiy scores
    correspond to ``1 - kernel`` between each feature of each
    pair of feature collections in ``fcs``.

    (The kernel used is currently fixed to ``cosine`` distance.)
    """
    dis = {}
    for count, name in enumerate(feature_names, 1):
        logger.info('computing pairwise dissimilarity matrix for %d of %d features (current feature: %s)', count, len(feature_names), name)
        dis[name] = 1 - pairwise_distances(dict_vector().fit_transform([ get_feat(fc, name) for fc in fcs ]), metric='cosine', n_jobs=1)

    return dis


def dict_vector():
    return DictVectorizer(sparse=False)


def hard_limit(limit):
    if limit is None:
        return limit
    else:
        return limit * 10


def get_feat(fc, name):
    if len(fc[name]) == 0:
        return StringCounter({'': 0})
    else:
        return fc[name]


def str_to_max_int(s, maximum):
    try:
        return min(maximum, int(s))
    except (ValueError, TypeError):
        return maximum


def negative_subtopic_labels(label_store, folders, cid, subid):
    subfolders = list(folders.parent_subfolders((cid, subid)))
    for fid, subfolder_id in subfolders:
        for cid2, subid2 in folders.items(fid, subfolder_id):
            for lab in label_store.directly_connected(cid2):
                if lab.value == CorefValue.Negative and lab.subtopic_for(cid2) == subid2:
                    yield lab

    in_fids = set()
    for fid, subfolder_id in subfolders:
        in_fids.add(fid)
        for cousin_subid in folders.subfolders(fid):
            if cousin_subid == subfolder_id:
                continue
            for cid2, subid2 in folders.items(fid, cousin_subid):
                yield Label(cid, cid2, Folders.DEFAULT_ANNOTATOR_ID, CorefValue.Negative, subid, subid2)

    for other_fid in folders.folders():
        if other_fid in in_fids:
            continue
        for other_subid in folders.subfolders(other_fid):
            for cid2, subid2 in folders.items(other_fid, other_subid):
                yield Label(cid, cid2, Folders.DEFAULT_ANNOTATOR_ID, CorefValue.Negative, subid, subid2)


def negative_subfolder_ids(label_store, folders, fid, subid):
    for cousin_subid in folders.subfolders(fid):
        if cousin_subid == subid:
            continue
        for cid2, subid2 in folders.items(fid, cousin_subid):
            yield (
             cid2, subid2)

    for other_fid in folders.folders():
        if other_fid == fid:
            continue
        for other_subid in folders.subfolders(other_fid):
            for cid2, subid2 in folders.items(other_fid, other_subid):
                yield (
                 cid2, subid2)