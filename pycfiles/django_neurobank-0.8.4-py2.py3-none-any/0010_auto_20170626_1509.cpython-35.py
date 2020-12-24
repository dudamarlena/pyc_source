# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0010_auto_20170626_1509.py
# Compiled at: 2017-06-26 15:09:47
# Size of source mod 2**32: 1233 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0009_auto_20170626_1458')]
    operations = [
     migrations.RemoveField(model_name='datatype', name='spec'),
     migrations.RemoveField(model_name='domain', name='remote'),
     migrations.RemoveField(model_name='domain', name='url'),
     migrations.AddField(model_name='datatype', name='content_type', field=models.CharField(blank=True, max_length=128, null=True)),
     migrations.AddField(model_name='domain', name='root', field=models.CharField(default='', help_text='Root path for resources.', max_length=512), preserve_default=False),
     migrations.AddField(model_name='domain', name='scheme', field=models.CharField(default='neurobank', max_length=16), preserve_default=False)]