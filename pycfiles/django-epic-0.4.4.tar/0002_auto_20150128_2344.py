# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidm/egauge/web/www/django/egauge_django/epic/migrations/0002_auto_20150128_2344.py
# Compiled at: 2015-01-29 12:39:49
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('epic', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'part', name=b'last_bom_mod_name', field=models.CharField(default=b'', help_text=b'Name of entity which last modified this part.', max_length=31, blank=True), preserve_default=True),
     migrations.AddField(model_name=b'part', name=b'last_bom_mod_type', field=models.IntegerField(default=0, choices=[(0, 'user'), (1, 'tool')]), preserve_default=True),
     migrations.AddField(model_name=b'vendor_part', name=b'status', field=models.IntegerField(default=1, help_text=b'The life-time status of this vendor part.', verbose_name=b'Life-time Status', choices=[(0, 'preview'), (1, 'active'), (2, 'deprecated'), (3, 'obsolete')]), preserve_default=True)]