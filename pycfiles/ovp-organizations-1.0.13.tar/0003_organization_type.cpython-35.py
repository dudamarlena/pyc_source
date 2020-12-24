# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0003_organization_type.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 616 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0002_organization')]
    operations = [
     migrations.AddField(model_name='organization', name='type', field=models.PositiveSmallIntegerField(choices=[(0, 'Organization'), (1, 'School'), (2, 'Company'), (3, 'Group of volunteers')], default=0, verbose_name='Type'), preserve_default=False)]