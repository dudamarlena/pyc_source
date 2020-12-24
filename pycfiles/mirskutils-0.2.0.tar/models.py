# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./webapp/registration/models.py
# Compiled at: 2014-06-01 18:18:49
from django.db import models
import os, re, time
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User

class Individual(AbstractUser):

    def __unicode__(self):
        if self.first_name and self.last_name:
            return '%s %s.' % (self.first_name, self.last_name[:1])
        if self.first_name:
            return '%s' % self.first_name
        if self.email:
            return '%s' % self.email
        return '%s' % self.username