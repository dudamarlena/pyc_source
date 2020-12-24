# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/managers.py
# Compiled at: 2012-08-07 13:42:33
from django.utils.timezone import now
from django.db.models import Manager

class PublicManager(Manager):

    def public(self):
        """Return public posts."""
        return self.get_query_set().filter(status__gte=2)

    def published(self):
        """Return public posts that are not in the future."""
        return self.get_query_set().filter(status__gte=2, publish__lte=now())