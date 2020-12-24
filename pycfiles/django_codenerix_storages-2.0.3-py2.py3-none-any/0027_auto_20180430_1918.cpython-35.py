# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0027_auto_20180430_1918.py
# Compiled at: 2018-04-30 13:18:51
# Size of source mod 2**32: 1118 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0026_auto_20180430_1909')]
    operations = [
     migrations.AddField(model_name='incomingalbaran', name='date', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'), preserve_default=False),
     migrations.AddField(model_name='outgoingalbaran', name='date', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'), preserve_default=False),
     migrations.AddField(model_name='requeststock', name='date', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'), preserve_default=False)]