# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/parkners_new/avishan/migrations/0007_visitorkey.py
# Compiled at: 2020-02-27 12:00:39
# Size of source mod 2**32: 1040 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0006_auto_20200219_0421')]
    operations = [
     migrations.CreateModel(name='VisitorKey',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'last_used', models.DateTimeField(blank=True, default=None, null=True)),
      (
       'last_login', models.DateTimeField(blank=True, default=None, null=True)),
      (
       'last_logout', models.DateTimeField(blank=True, default=None, null=True)),
      (
       'key', models.CharField(max_length=255, unique=True)),
      (
       'user_user_group', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), to='avishan.UserUserGroup'))],
       options={'abstract': False})]