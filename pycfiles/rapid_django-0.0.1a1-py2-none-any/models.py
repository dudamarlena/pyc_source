# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/models.py
# Compiled at: 2015-09-03 15:15:45
from django.db import models
from django.contrib.auth.models import User

class CrudModel(models.Model):

    class Meta:
        abstract = True


class Application(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='nome')
    python_name = models.CharField(max_length=255, unique=True, verbose_name='Nome no Python')
    managers = models.ManyToManyField(User, verbose_name='gestores', related_name='managed_applications')
    enabled = models.BooleanField(default=True, verbose_name='ativa')

    def __unicode__(self):
        return self.name

    url_name = 'aplicacao'

    class Meta:
        verbose_name = 'aplicação'
        verbose_name_plural = 'aplicações'


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, verbose_name='aplicação')
    name = models.CharField(max_length=60, verbose_name='nome')
    description = models.TextField(verbose_name='descrição')
    users = models.ManyToManyField(User, verbose_name='usuários', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'