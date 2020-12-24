# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdjango/db/models/managers.py
# Compiled at: 2016-06-20 12:45:24
from django.db import models

class SafeManager(models.Manager):

    def safe_get(self, **kwargs):
        try:
            return super(SafeManager, self).get(**kwargs)
        except:
            return

        return

    def get_or_create(self, **kwargs):
        return self.safe_get(**kwargs) or self.create(**kwargs)