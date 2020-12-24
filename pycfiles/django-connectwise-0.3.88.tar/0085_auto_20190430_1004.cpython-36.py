# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0085_auto_20190430_1004.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 740 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0084_auto_20190404_1532')]
    operations = [
     migrations.AddField(model_name='timeentry',
       name='email_cc_flag',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='timeentry',
       name='email_contact_flag',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='timeentry',
       name='email_resource_flag',
       field=models.BooleanField(default=False))]