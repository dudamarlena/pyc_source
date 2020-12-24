# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/dev/django-billjobs/billjobs/migrations/0004_auto_20160321_1256.py
# Compiled at: 2016-03-22 05:48:15
# Size of source mod 2**32: 844 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0003_billline_note')]
    operations = [
     migrations.AddField(model_name='bill', name='issuer_address', field=models.CharField(default='\n            Your Coworking Space Name<br/>Building name<br/>\n            Number & Street<br/>Postal Code Town\n            ', max_length=1024)),
     migrations.AlterField(model_name='billline', name='note', field=models.CharField(blank=True, help_text='Write a simple note which will be added in your bill', max_length=1024, verbose_name='Note'))]