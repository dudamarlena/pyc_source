# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0020_auto_20170412_1609.py
# Compiled at: 2017-04-12 12:11:31
# Size of source mod 2**32: 973 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0019_auto_20170127_1717')]
    operations = [
     migrations.AddField(model_name='organization', name='contact_email', field=models.EmailField(blank=True, max_length=150, null=True, verbose_name='Responsible email')),
     migrations.AddField(model_name='organization', name='contact_name', field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Responsible name')),
     migrations.AddField(model_name='organization', name='contact_phone', field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Responsible phone'))]