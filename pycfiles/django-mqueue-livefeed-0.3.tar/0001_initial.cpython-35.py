# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo90/mogo/mqueue_livefeed/migrations/0001_initial.py
# Compiled at: 2018-01-21 03:08:12
# Size of source mod 2**32: 840 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='MonitoredSite', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'slug', models.SlugField(unique=True, verbose_name='Slug')),
      (
       'name', models.CharField(max_length=120, verbose_name='Name'))], options={'verbose_name_plural': 'Monitored sites', 
      'verbose_name': 'Monitored site', 
      'ordering': ['name']})]