# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /www/PelicanAdmin/pelican_admin/settings.py
# Compiled at: 2012-11-24 19:02:40
__author__ = 'Flavio'
from django.db import models

class Settings(models.Model):
    name = models.CharField(max_length=32, unique=True, primary_key=True)
    value = models.TextField()