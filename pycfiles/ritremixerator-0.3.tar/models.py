# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eitan/Documents/code/RITRemixerator/dorrie/comps/models.py
# Compiled at: 2012-02-06 13:58:25
from django.db import models

class Spin(models.Model):
    """Class for the releases"""
    name = models.TextField(help_text='The name of the spin.')
    language = models.TextField()
    timezone = models.TextField()
    rootpwd = models.TextField()
    baseks = models.TextField()
    gplus = models.ManyToManyField('Group', related_name='gplus_set')
    gminus = models.ManyToManyField('Group', related_name='gminus_set')
    pplus = models.ManyToManyField('Package', related_name='pplus_set')
    pminus = models.ManyToManyField('Package', related_name='pminus_set')
    pid = models.IntegerField(default=0)
    uploaded = models.BooleanField()


class Group(models.Model):
    """Package Groups"""
    name = models.TextField(help_text='The name of the package group.')


class Package(models.Model):
    """A Package."""
    name = models.TextField(help_text='The name of the package.')