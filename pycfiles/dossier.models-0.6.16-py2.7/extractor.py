# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/extractor.py
# Compiled at: 2015-07-08 07:34:06
"""
Create a keyword searches from an entity profile.
"""
from __future__ import absolute_import, division
import json, logging, os, sys, time, datetime, argparse, dblogger, json, yakonfig, streamcorpus
from streamcorpus import Chunk, make_stream_item
import streamcorpus_pipeline
from streamcorpus_pipeline.stages import PipelineStages
from streamcorpus_pipeline._pipeline import PipelineFactory
from dossier.fc import FeatureCollectionChunk as FCChunk
from dossier.fc import FeatureCollection, StringCounter
import operator
try:
    from collections import Counter, defaultdict
except ImportError:
    from backport_collections import Counter, defaultdict

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
logger = logging.getLogger(__name__)

def extract(positive_fcs, negative_fcs, features=None):
    """Takes a labeled set of feature collections (positive and negative)
       and the features wanted. And trains a Naive Bayes classifier on
       the underlying keys of the set of selected features features.
       If no features are selected, all are used.

       Returns two list of (keywords, strength) tuples ordered by strength. The
       first are feature keys that were predictive of the positive
       label and the second are the feature keys are were predictive
       of the negative label. 

    `*_fcs' is the list of feature collections, positive label and
            negative label respectively.

    `features' designates which specific feature gets vectorized the
               other features are ignored.

    """
    labels = np.array([1] * len(positive_fcs) + [0] * len(negative_fcs))
    v = DictVectorizer(sparse=False)
    D = list()
    for fc in positive_fcs + negative_fcs:
        feat = StringCounter()
        for f in features:
            feat += fc[f]

        D.append(feat)

    X = v.fit_transform(D)
    clf = BernoulliNB()
    clf.fit(X, labels)
    positive_keywords = v.inverse_transform(clf.feature_log_prob_[1])[0]
    negative_keywords = v.inverse_transform(clf.feature_log_prob_[0])[0]
    pos_words = Counter(positive_keywords)
    neg_words = Counter(negative_keywords)
    pos_ordered = sorted(pos_words.items(), key=operator.itemgetter(1), reverse=True)
    neg_ordered = sorted(neg_words.items(), key=operator.itemgetter(1), reverse=True)
    return (
     pos_ordered, neg_ordered)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python extractor.py corpus.fc', description=__doc__)
    parser.add_argument('corpus', help='path feature collection chunk that contains the corpus')
    args = parser.parse_args()
    positive_fcs = list()
    negative_fcs = list()
    for i, fc in enumerate(FCChunk(args.corpus)):
        if i % 2:
            positive_fcs.append(fc)
        else:
            negative_fcs.append(fc)

    keywords = extract(positive_fcs, negative_fcs, features=[
     'both_bow_3',
     'both_con_3',
     'both_co_LOC_3',
     'both_co_ORG_3'])
    print 'Predictive of positive labels:'
    print keywords[0]
    print 'Predictive of positive labels:'
    print keywords[1]