# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/notification/migrations/0002_emailnotification_sites.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 521 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0001_initial'),
     ('notification', '0001_initial_create_email_notification')]
    operations = [
     migrations.AddField(model_name='emailnotification',
       name='sites',
       field=models.ManyToManyField(to='sites.Site'))]