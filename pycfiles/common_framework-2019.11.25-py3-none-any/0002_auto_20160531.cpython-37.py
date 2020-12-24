# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0002_auto_20160531.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 1477 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('common', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='webhook',
       options={'verbose_name':'webhook', 
      'verbose_name_plural':'webhooks'}),
     migrations.AddField(model_name='webhook',
       name='method',
       field=models.CharField(choices=[('post', 'POST'), ('put', 'PUT'), ('patch', 'PATCH')], default='post', max_length=5, verbose_name='method')),
     migrations.AddField(model_name='webhook',
       name='timeout',
       field=models.PositiveSmallIntegerField(default=30, verbose_name="délai d'attente")),
     migrations.AddField(model_name='webhook',
       name='retries',
       field=models.PositiveSmallIntegerField(default=0, verbose_name='tentatives')),
     migrations.AddField(model_name='webhook',
       name='delay',
       field=models.PositiveSmallIntegerField(default=0, verbose_name='délai entre tentatives')),
     migrations.AlterField(model_name='webhook',
       name='token',
       field=models.TextField(blank=True, null=True, verbose_name='token'))]