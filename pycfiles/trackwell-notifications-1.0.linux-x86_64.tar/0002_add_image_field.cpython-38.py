# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/notifications/migrations/0002_add_image_field.py
# Compiled at: 2020-01-31 08:32:40
# Size of source mod 2**32: 624 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0001_initial')]
    operations = [
     migrations.AddField(model_name='notification',
       name='image',
       field=models.ImageField(upload_to='notification_imgs',
       null=True,
       blank=True,
       help_text='Image to accompany notification (optional)'))]