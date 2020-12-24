# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/features/surface.py
# Compiled at: 2019-04-03 05:50:04
# Size of source mod 2**32: 1912 bytes
"""
Feature extraction with Word2Vec, as explained in

"Enhancing deep learning sentiment analysis with ensemble techniques in social applications",
http://dx.doi.org/10.1016/j.eswa.2017.02.002

Needs a Word2Vec model previously trained. Compatible with Gensim and Google word2vec format.
"""
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import normalize, scale
z_features = [
 '!', '#', '?', 'pos', 'neu', 'neg', 'total_score', 'words_all_caps', 'words_elong',
 'nrc_pos', 'nrc_neg', 'nrc_total']
desired_feats = ('!', '#', '?', 'total_score', 'words_all_caps', 'words_elong', 'nrc_pos',
                 'nrc_neg', 'nrc_total')

def dict_merge(a, b):
    c = a.copy()
    c.update(b)
    return c


def parse_feats(d, contains):
    f = {k:v for k, v in d.items() if contains in k}
    v = f.values()
    v_l, v_s = list(v), set(v)
    f = defaultdict(lambda : 0)
    for feat in v_s:
        f[feat] += v_l.count(feat)

    return dict(f)


def convert2uniform(d):
    cnlp_feats = list()
    for cnlp_feat_raw in d:
        cnlp_feat = {k:v for k, v in cnlp_feat_raw.items() if k in desired_feats if k in desired_feats}
        cnlp_feat_plus = parse_feats(cnlp_feat_raw, 'sentiment')
        cnlp_feat = dict_merge(cnlp_feat, cnlp_feat_plus)
        cnlp_feats.append(cnlp_feat)

    return cnlp_feats


def to_z(feats):
    Z = np.zeros((len(feats), len(z_features)))
    for f_i, feat in enumerate(feats):
        z_i = [feat.get(k, 0) for k in z_features]
        Z[f_i] = np.array(z_i)

    return Z


def transform(X):
    """Extract the features.
    This considers X to be a list of lists of texts.
    [
        ['my', 'dog', 'run', 'in', 'the', 'rain']
    ]
    """
    raise NotImplementedError