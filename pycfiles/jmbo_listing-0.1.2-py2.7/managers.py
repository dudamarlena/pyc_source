# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/listing/managers.py
# Compiled at: 2016-08-21 15:36:59
from django.db import models
from django.conf import settings

class PermittedManager(models.Manager):

    def get_query_set(self):
        return super(PermittedManager, self).get_query_set().filter(sites__id__exact=settings.SITE_ID)