# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/migrations/0002_privatedownload.py
# Compiled at: 2019-07-04 10:14:06
# Size of source mod 2**32: 653 bytes
from django.db import migrations, models
import znbdownload.fields

class Migration(migrations.Migration):
    dependencies = [
     ('znbdownload', '0001_initial')]
    operations = [
     migrations.CreateModel(name='PrivateDownload',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=200)),
      (
       'private_file', znbdownload.fields.S3PrivateFileField(blank=True, null=True, upload_to=''))])]