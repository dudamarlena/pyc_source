# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_message/migrations/0008_auto_20191119_1623.py
# Compiled at: 2019-11-19 03:23:08
from __future__ import unicode_literals
import bee_django_richtext.custom_fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_message', '0007_auto_20190816_1757')]
    operations = [
     migrations.AlterField(model_name=b'sendrecord', name=b'info', field=bee_django_richtext.custom_fields.RichTextField(blank=True, default=b'', image_max_size=1, null=True, verbose_name=b'内容'))]