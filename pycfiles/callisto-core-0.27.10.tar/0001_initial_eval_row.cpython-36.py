# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/evaluation/migrations/0001_initial_eval_row.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1527 bytes
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('delivery', '0039_auto_20171208_0039')]
    operations = [
     migrations.CreateModel(name='EvalRow',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'action', models.TextField(null=True)),
      (
       'record_encrypted', models.BinaryField(null=True)),
      (
       'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       'record',
       models.ForeignKey(null=True,
         on_delete=(django.db.models.deletion.SET_NULL),
         to='delivery.Report')),
      (
       'user',
       models.ForeignKey(null=True,
         on_delete=(django.db.models.deletion.SET_NULL),
         to=(settings.AUTH_USER_MODEL)))])]