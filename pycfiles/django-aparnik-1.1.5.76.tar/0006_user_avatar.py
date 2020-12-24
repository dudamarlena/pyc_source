# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0006_user_avatar.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.core.validators
from aparnik.utils import fields

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0001_initial'),
     ('aparnik_users', '0005_auto_20181025_1601')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'avatar', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'filefields.FileField', verbose_name=b'Avatar'))]