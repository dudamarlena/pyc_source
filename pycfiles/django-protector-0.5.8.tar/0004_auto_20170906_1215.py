# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0004_auto_20170906_1215.py
# Compiled at: 2017-09-06 09:45:46
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0008_alter_user_username_max_length'),
     ('protector', '0003_auto_20160607_0838')]
    operations = [
     migrations.CreateModel(name=b'PermissionInfo', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'description', models.TextField(blank=True, null=True, verbose_name=b'description')),
      (
       b'permission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=b'auth.Permission'))], options={b'verbose_name': b'Permission Info', 
        b'verbose_name_plural': b'Permissions Info'}),
     migrations.AlterModelManagers(name=b'restriction', managers=[])]