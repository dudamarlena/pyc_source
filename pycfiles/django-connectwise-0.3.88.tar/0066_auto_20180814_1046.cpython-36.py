# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0066_auto_20180814_1046.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 554 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0065_auto_20180809_1124')]
    operations = [
     migrations.AlterField(model_name='sla',
       name='based_on',
       field=models.CharField(choices=[('MyCalendar', 'My Company Calendar'), ('Customer', "Customer's Calendar"), ('AllHours', '24 Hours'), ('Custom', 'Custom Calendar')], default='MyCalendar', max_length=50))]