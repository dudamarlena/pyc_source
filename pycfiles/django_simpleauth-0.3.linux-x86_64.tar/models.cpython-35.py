# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratheek/msc/pythons/lib/python3.5/site-packages/simpleauth/models.py
# Compiled at: 2017-02-09 05:20:29
# Size of source mod 2**32: 179 bytes
from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)