# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0007_auto_20191211_1501.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 1058 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('explore', '0006_transfer_language')]
    operations = [
     migrations.AlterField(model_name='corpus',
       name='date',
       field=models.DateField(blank=True, null=True)),
     migrations.AlterField(model_name='corpus',
       name='desc',
       field=models.TextField(blank=True, default='')),
     migrations.AlterField(model_name='corpus',
       name='initial_query',
       field=models.TextField(blank=True, null=True)),
     migrations.AlterField(model_name='corpus',
       name='initial_table',
       field=models.TextField(blank=True, null=True)),
     migrations.AlterField(model_name='corpus',
       name='url',
       field=models.URLField(blank=True, max_length=255, null=True))]