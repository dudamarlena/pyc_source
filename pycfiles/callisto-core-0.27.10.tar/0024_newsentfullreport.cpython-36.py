# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0024_newsentfullreport.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1170 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0023_auto_20171122_1435')]
    operations = [
     migrations.CreateModel(name='NewSentFullReport',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'sent', models.DateTimeField(auto_now_add=True)),
      (
       'to_address', models.TextField(null=True)),
      (
       'report',
       models.ForeignKey(blank=True,
         null=True,
         on_delete=(django.db.models.deletion.SET_NULL),
         to='delivery.Report'))])]