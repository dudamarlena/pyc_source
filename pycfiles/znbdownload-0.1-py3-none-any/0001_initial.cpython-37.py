# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/migrations/0001_initial.py
# Compiled at: 2019-07-03 15:55:12
# Size of source mod 2**32: 718 bytes
from django.db import migrations, models
import znbdownload.storage

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Download',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=200)),
      (
       'private', models.BooleanField(default=False)),
      (
       'private_file', models.FileField(blank=True, null=True, storage=(znbdownload.storage.S3PrivateStorage()), upload_to=''))])]