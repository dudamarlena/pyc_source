# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/migrations/0019_auto_20170127_1717.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 891 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_organizations', '0018_auto_20170127_1513')]
    operations = [
     migrations.AlterField(model_name='organization', name='cover', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='ovp_uploads.UploadedImage', verbose_name='cover')),
     migrations.AlterField(model_name='organization', name='image', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ovp_uploads.UploadedImage', verbose_name='image'))]