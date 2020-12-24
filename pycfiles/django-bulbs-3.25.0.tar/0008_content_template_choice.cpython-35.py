# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/content/migrations/0008_content_template_choice.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 434 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0007_content_evergreen')]
    operations = [
     migrations.AddField(model_name='content', name='template_choice', field=models.IntegerField(choices=[(0, 'Default')], default=0))]