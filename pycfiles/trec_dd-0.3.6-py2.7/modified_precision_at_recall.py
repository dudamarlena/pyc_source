# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trec_dd/scorer/modified_precision_at_recall.py
# Compiled at: 2015-07-22 16:10:03
"""trec_dd.scorer.modified_precision_at_recall provides the
   precision at full recall score for TREC DD, where in this 
   case a document is counted towards precision in terms of
   the fraction of new subtopics (out of total subtopics) 
   it provides. This may or may not be a good idea.

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


def modified_precision_at_recall(run, label_store):
    scores_by_topic = dict()
    for topic_id, results in run['results'].items():
        subtopic_ids = set(get_all_subtopics(label_store, topic_id))
        seen_subtopics = set()
        relevant_docs = 0
        for idx, result in enumerate(results):
            assert idx == result['rank'] - 1
            result_subtopics = {subtopic for subtopic, conf in get_best_subtopics(result['subtopics'])}
            if len(result_subtopics) > 0:
                frac = len(result_subtopics.difference(seen_subtopics)) / len(result_subtopics)
            else:
                frac = 0
            relevant_docs += frac
            seen_subtopics.update(result_subtopics)
            if len(seen_subtopics) == len(subtopic_ids):
                break

        p = relevant_docs / (idx + 1)
        scores_by_topic[topic_id] = p

    macro_avg = mean(scores_by_topic.values())
    run['scores']['modified_precision_at_recall'] = {'scores_by_topic': scores_by_topic, 'macro_average': macro_avg}