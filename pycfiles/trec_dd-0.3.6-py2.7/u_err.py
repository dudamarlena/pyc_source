# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trec_dd/scorer/u_err.py
# Compiled at: 2015-07-22 16:10:03
"""trec_dd.scorer.u_err provides a u-ERR scorer for TREC DD

.. This software is released under an MIT/X11 open source license.
   Copyright 2015 Diffeo, Inc.

"""
from __future__ import division
from operator import attrgetter
from trec_dd.utils import get_all_subtopics

def mean(l):
    if len(l) == 0:
        return 0.0
    s = sum(l)
    return s / len(l)


def u_err(run, label_store):
    scores_by_topic = dict()
    for topic_id, results in run['results'].items():
        subtopic_ids = set(get_all_subtopics(label_store, topic_id))
        scores_by_topic[topic_id] = len(results) / len(subtopic_ids)

    macro_avg = mean(scores_by_topic.values())
    run['scores']['u_err'] = {'scores_by_topic': scores_by_topic, 'macro_average': macro_avg}