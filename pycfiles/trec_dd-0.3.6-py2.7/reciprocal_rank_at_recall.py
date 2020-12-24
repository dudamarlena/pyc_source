# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trec_dd/scorer/reciprocal_rank_at_recall.py
# Compiled at: 2015-07-22 16:10:03
"""trec_dd.scorer.reciprocal_rank_at_recall provides a the
   reciprocal rank at full recall score for TREC DD

   This assumes binary relevance, but can be easily upgraded.

.. This software is released under an MIT/X11 open source license.
   Copyright 2015 Diffeo, Inc.

"""
from __future__ import division
from operator import attrgetter
from trec_dd.utils import get_all_subtopics, get_best_subtopics

def mean(l):
    if len(l) == 0:
        return 0.0
    s = sum(l)
    return s / len(l)


def reciprocal_rank_at_recall(run, label_store):
    scores_by_topic = dict()
    for topic_id, results in run['results'].items():
        subtopic_ids = set(get_all_subtopics(label_store, topic_id))
        seen_subtopics = set()
        for idx, result in enumerate(results):
            assert idx == result['rank'] - 1
            for subtopic, conf in get_best_subtopics(result['subtopics']):
                seen_subtopics.add(subtopic)

            if len(seen_subtopics) == len(subtopic_ids):
                break

        scores_by_topic[topic_id] = 1 / (idx + 1)

    macro_avg = mean(scores_by_topic.values())
    run['scores']['reciprocal_rank_at_recall'] = {'scores_by_topic': scores_by_topic, 'macro_average': macro_avg}