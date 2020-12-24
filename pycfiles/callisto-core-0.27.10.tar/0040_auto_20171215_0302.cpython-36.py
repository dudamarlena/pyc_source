# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0040_auto_20171215_0302.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1619 bytes
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0039_auto_20171208_0039')]
    operations = [
     migrations.CreateModel(name='RecordHistorical',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       'encrypted_eval', models.BinaryField(null=True))]),
     migrations.AddField(model_name='report',
       name='encrypted_eval',
       field=models.BinaryField(blank=True)),
     migrations.AlterField(model_name='report',
       name='encode_prefix',
       field=models.TextField(null=True)),
     migrations.AlterField(model_name='report',
       name='encrypted',
       field=models.BinaryField(blank=True)),
     migrations.AlterField(model_name='report',
       name='last_edited',
       field=models.DateTimeField(null=True)),
     migrations.AddField(model_name='recordhistorical',
       name='record',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       to='delivery.Report'))]