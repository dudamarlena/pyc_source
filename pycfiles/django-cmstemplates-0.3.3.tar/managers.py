# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/managers.py
# Compiled at: 2015-03-22 09:31:33
from __future__ import print_function, unicode_literals
from django.db import models

class TemplateQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)