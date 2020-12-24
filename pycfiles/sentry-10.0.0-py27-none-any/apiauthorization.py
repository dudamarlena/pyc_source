# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/apiauthorization.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from django.utils import timezone
from sentry.models.apiscopes import HasApiScopes
from sentry.db.models import Model, FlexibleForeignKey, sane_repr

class ApiAuthorization(Model, HasApiScopes):
    """
    Tracks which scopes a user has authorized for a given application.

    This is used to determine when we need re-prompt a user, as well as track
    overall approved applications (vs individual tokens).
    """
    __core__ = True
    application = FlexibleForeignKey('sentry.ApiApplication', null=True)
    user = FlexibleForeignKey('sentry.User')
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_apiauthorization'
        unique_together = (('user', 'application'), )

    __repr__ = sane_repr('user_id', 'application_id')