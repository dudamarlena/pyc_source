# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/tests/models.py
# Compiled at: 2017-10-20 11:35:08
from django.core.urlresolvers import reverse
from django.db import models

class DummyModel1(models.Model):
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('dummymodel1-detail', args=(self.pk,))


class DummyModel2(models.Model):
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('dummymodel2-detail', args=(self.pk,))