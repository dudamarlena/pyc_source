# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-core/lucterios/CORE/migrations/0002_savedcriteria.py
# Compiled at: 2020-03-26 06:35:14
# Size of source mod 2**32: 904 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('CORE', '0001_initial')]
    operations = [
     migrations.CreateModel(name='SavedCriteria',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
      (
       'name', models.CharField(verbose_name='name', max_length=100)),
      (
       'modelname', models.CharField(verbose_name='model', max_length=100)),
      (
       'criteria', models.TextField(verbose_name='criteria', blank=True))],
       options={'verbose_name':'Saved criteria', 
      'default_permissions':[],  'verbose_name_plural':'Saved criterias'})]