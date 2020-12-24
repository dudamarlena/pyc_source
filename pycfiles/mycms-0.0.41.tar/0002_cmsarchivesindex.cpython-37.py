# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/migrations/0002_cmsarchivesindex.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 725 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mycms', '0001_initial')]
    operations = [
     migrations.CreateModel(name='CMSArchivesIndex',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'month', models.IntegerField(default=0)),
      (
       'year', models.IntegerField(default=1975)),
      (
       'entries', models.ManyToManyField(blank=True, to='mycms.CMSEntries'))])]