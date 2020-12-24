# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0002_auto_20170512_1459.py
# Compiled at: 2019-04-03 22:56:25
# Size of source mod 2**32: 1445 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0001_initial')]
    operations = [
     migrations.AddField(model_name='instructorlistpluginmodel',
       name='title',
       field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Listing Title')),
     migrations.AlterField(model_name='instructorlistpluginmodel',
       name='template',
       field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Template')),
     migrations.AlterField(model_name='locationlistpluginmodel',
       name='template',
       field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Template')),
     migrations.AlterField(model_name='locationpluginmodel',
       name='location',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='core.Location', verbose_name='Location')),
     migrations.AlterField(model_name='locationpluginmodel',
       name='template',
       field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Template'))]