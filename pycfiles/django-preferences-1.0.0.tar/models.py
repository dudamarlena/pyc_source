# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/tests/models.py
# Compiled at: 2018-12-20 02:32:17
from django.db import models
from preferences.models import Preferences

class MyPreferences(Preferences):
    portal_contact_email = models.EmailField()