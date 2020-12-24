# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sites_groups/migrations/0001_initial.py
# Compiled at: 2016-05-25 05:23:19
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('sites', '0002_alter_domain_unique')]
    operations = [
     migrations.CreateModel(name=b'SitesGroup', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'sites', models.ManyToManyField(help_text=b'Sites that belong to this group.', to=b'sites.Site'))], options={b'ordering': ('title', )})]