# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0014_auto_20170712_1018.py
# Compiled at: 2017-07-12 10:19:38
# Size of source mod 2**32: 871 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('neurobank', '0013_auto_20170627_1226')]
    operations = [
     migrations.RenameField(model_name='resource', old_name='registered', new_name='created_on'),
     migrations.AddField(model_name='resource', name='created_by', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='resources', to=settings.AUTH_USER_MODEL), preserve_default=False)]