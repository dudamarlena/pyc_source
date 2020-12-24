# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superhero/models.py
# Compiled at: 2015-05-05 00:01:33
from django.utils.translation import ugettext as _
from django.db import models
from jmbo.models import ModelBase

class Superhero(ModelBase):
    name = models.CharField(max_length=256, editable=False)

    class Meta:
        verbose_name_plural = _('Superheroes')