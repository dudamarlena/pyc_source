# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/precision_recall_at_k.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 2123 bytes
"""
This module illustrates how to compute Precision at k and Recall at k metrics.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
from surprise import Dataset
from surprise import SVD
from surprise.model_selection import KFold

def precision_recall_at_k(predictions, k=10, threshold=3.5):
    """Return precision and recall at k metrics for each user."""
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=(lambda x: x[0]), reverse=True)
        n_rel = sum(true_r >= threshold for _, true_r in user_ratings)
        n_rec_k = sum(est >= threshold for est, _ in user_ratings[:k])
        n_rel_and_rec_k = sum(true_r >= threshold and est >= threshold for est, true_r in user_ratings[:k])
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1

    return (precisions, recalls)


data = Dataset.load_builtin('ml-100k')
kf = KFold(n_splits=5)
algo = SVD()
for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)
    precisions, recalls = precision_recall_at_k(predictions, k=5, threshold=4)
    print(sum(prec for prec in precisions.values()) / len(precisions))
    print(sum(rec for rec in recalls.values()) / len(recalls))