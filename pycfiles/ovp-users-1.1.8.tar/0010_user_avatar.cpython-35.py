# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-users/ovp_users/migrations/0010_user_avatar.py
# Compiled at: 2016-12-06 14:20:20
# Size of source mod 2**32: 628 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_uploads', '0003_uploadedimage_uuid'),
     ('ovp_users', '0009_user_phone')]
    operations = [
     migrations.AddField(model_name='user', name='avatar', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avatar_user', to='ovp_uploads.UploadedImage'))]