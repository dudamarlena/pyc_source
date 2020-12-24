# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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