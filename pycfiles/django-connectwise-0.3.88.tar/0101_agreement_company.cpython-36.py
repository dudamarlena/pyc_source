# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0101_agreement_company.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 496 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0100_auto_20190718_1417')]
    operations = [
     migrations.AddField(model_name='agreement',
       name='company',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.Company'))]