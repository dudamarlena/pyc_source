# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/zin/kerk/eventcalendar/managers.py
# Compiled at: 2018-08-31 10:54:42
# Size of source mod 2**32: 222 bytes
from django.db import models

class CategoryManager(models.Manager):

    def with_uses(self, announcements):
        entries = announcements.get_entries()
        return self.filter(announcements__in=entries).distinct()