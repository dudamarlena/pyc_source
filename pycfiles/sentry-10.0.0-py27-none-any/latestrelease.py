# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/latestrelease.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from sentry.db.models import BoundedBigIntegerField, Model, sane_repr

class LatestRelease(Model):
    """
    Tracks the latest release of a given repository for a given environment.
    """
    __core__ = False
    repository_id = BoundedBigIntegerField()
    environment_id = BoundedBigIntegerField()
    release_id = BoundedBigIntegerField()
    deploy_id = BoundedBigIntegerField(null=True)
    commit_id = BoundedBigIntegerField(null=True)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_latestrelease'
        unique_together = (('repository_id', 'environment_id'), )

    __repr__ = sane_repr('repository_id', 'environment_id')