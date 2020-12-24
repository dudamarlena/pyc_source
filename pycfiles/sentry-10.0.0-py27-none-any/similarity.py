# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/receivers/similarity.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry import features as feature_flags
from sentry.signals import event_processed
from sentry.similarity import features as similarity_features

@event_processed.connect(weak=False)
def record(project, event, **kwargs):
    if not feature_flags.has('projects:similarity-indexing', project):
        return
    similarity_features.record([event])