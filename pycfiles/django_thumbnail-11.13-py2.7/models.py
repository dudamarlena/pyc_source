# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sorl/thumbnail/models.py
# Compiled at: 2012-12-12 10:05:53
from django.db import models
from sorl.thumbnail.conf import settings

class KVStore(models.Model):
    key = models.CharField(max_length=200, primary_key=True, db_column=settings.THUMBNAIL_KEY_DBCOLUMN)
    value = models.TextField()