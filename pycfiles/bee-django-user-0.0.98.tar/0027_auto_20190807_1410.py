# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0027_auto_20190807_1410.py
# Compiled at: 2019-08-07 02:10:07
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0026_auto_20190630_1758')]
    operations = [
     migrations.AddField(model_name=b'userprofile', name=b'agent', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'agent_user', to=b'bee_django_user.UserProfile')),
     migrations.AddField(model_name=b'userprofile', name=b'gensee_room_id', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'直播间ID')),
     migrations.AddField(model_name=b'userprofile', name=b'wxservice_openid', field=models.CharField(blank=True, max_length=180, null=True))]