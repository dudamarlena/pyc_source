# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0006_auto_20180706_1552.py
# Compiled at: 2018-07-06 03:52:49
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_referral', '0005_auto_20180706_1545')]
    operations = [
     migrations.AlterUniqueTogether(name=b'useractivity', unique_together=set([('activity', 'user')]))]