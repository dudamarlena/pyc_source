# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gabriel.faleiro/.virtualenvs/test_save/saveall/saveall/tests/models.py
# Compiled at: 2016-03-11 14:01:48
from django.db import models

class Table01(models.Model):
    nome = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'table01'


class Table02(models.Model):
    nome = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'table02'


class Table03(models.Model):
    nome = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    dono = models.ForeignKey(Table01)
    raca = models.ForeignKey(Table02)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'table03'