# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/core/models.py
# Compiled at: 2018-11-08 07:12:47
# Size of source mod 2**32: 596 bytes
from django.db import models
from pkg_resources import working_set

def choices():
    for entry in working_set.iter_entry_points('exporter'):
        yield (entry.module_name, entry.name)


class ApiKey(models.Model):
    owner = models.ForeignKey('auth.User',
      on_delete=(models.CASCADE),
      related_name='+',
      help_text='Django user object')
    service = models.CharField(max_length=64,
      help_text='Service identifier',
      choices=(choices()))
    key = models.CharField(max_length=60,
      help_text='Service API Key')