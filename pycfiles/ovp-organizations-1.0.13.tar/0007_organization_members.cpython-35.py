# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0007_organization_members.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 623 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('ovp_organizations', '0006_auto_20161206_1612')]
    operations = [
     migrations.AddField(model_name='organization', name='members', field=models.ManyToManyField(related_name='organizations_member', to=settings.AUTH_USER_MODEL))]