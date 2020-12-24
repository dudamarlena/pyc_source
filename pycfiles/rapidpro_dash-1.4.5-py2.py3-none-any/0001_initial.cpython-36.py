# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/testapp/migrations/0001_initial.py
# Compiled at: 2017-04-17 16:26:07
# Size of source mod 2**32: 746 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('orgs', '0015_auto_20160209_0926')]
    operations = [
     migrations.CreateModel(name='Contact',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'uuid', models.CharField(unique=True, max_length=36)),
      (
       'name', models.CharField(max_length=128, verbose_name='Name')),
      (
       'is_active', models.BooleanField(default=True)),
      (
       'org', models.ForeignKey(to='orgs.Org'))])]