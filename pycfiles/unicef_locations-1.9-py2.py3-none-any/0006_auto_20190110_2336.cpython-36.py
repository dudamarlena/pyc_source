# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/migrations/0006_auto_20190110_2336.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 1779 bytes
import django.utils.timezone, model_utils.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('locations', '0005_auto_20181206_1127')]
    operations = [
     migrations.AddField(model_name='cartodbtable',
       name='created',
       field=model_utils.fields.AutoCreatedField(default=(django.utils.timezone.now), editable=False,
       verbose_name='created')),
     migrations.AddField(model_name='cartodbtable',
       name='modified',
       field=model_utils.fields.AutoLastModifiedField(default=(django.utils.timezone.now), editable=False,
       verbose_name='modified')),
     migrations.AddField(model_name='gatewaytype',
       name='created',
       field=model_utils.fields.AutoCreatedField(default=(django.utils.timezone.now), editable=False,
       verbose_name='created')),
     migrations.AddField(model_name='gatewaytype',
       name='modified',
       field=model_utils.fields.AutoLastModifiedField(default=(django.utils.timezone.now), editable=False,
       verbose_name='modified')),
     migrations.AddField(model_name='locationremaphistory',
       name='modified',
       field=model_utils.fields.AutoLastModifiedField(default=(django.utils.timezone.now), editable=False,
       verbose_name='modified'))]