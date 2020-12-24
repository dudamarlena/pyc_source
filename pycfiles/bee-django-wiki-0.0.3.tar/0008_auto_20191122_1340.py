# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_wiki/migrations/0008_auto_20191122_1340.py
# Compiled at: 2019-11-22 00:40:39
from __future__ import unicode_literals
import bee_django_richtext.custom_fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_wiki', '0007_auto_20190903_1846')]
    operations = [
     migrations.AlterField(model_name=b'topic', name=b'detail', field=bee_django_richtext.custom_fields.RichTextField(app_name=b'bee_django_wiki', emotion=False, image_max_size=2, img=False, model_name=b'Topic', text_min_length=5, undo_redo=False, verbose_name=b'详情'))]