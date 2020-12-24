# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sss/managers.py
# Compiled at: 2010-11-29 16:06:55
from django.db import models

class CurrentSprintManager(models.Manager):

    def get_query_set(self):
        return super(CurrentSprintManager, self).get_query_set().filter(current_sprint=True)