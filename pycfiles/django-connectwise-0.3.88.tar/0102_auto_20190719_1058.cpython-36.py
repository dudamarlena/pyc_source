# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0102_auto_20190719_1058.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 574 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0101_agreement_company')]
    operations = [
     migrations.AddField(model_name='agreement',
       name='agreement_type',
       field=models.CharField(max_length=50, null=True)),
     migrations.AddField(model_name='agreement',
       name='cancelled_flag',
       field=models.BooleanField(default=False))]