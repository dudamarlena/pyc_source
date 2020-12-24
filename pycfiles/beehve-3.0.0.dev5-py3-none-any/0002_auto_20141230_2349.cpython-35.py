# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/workers/migrations/0002_auto_20141230_2349.py
# Compiled at: 2016-08-07 14:40:53
# Size of source mod 2**32: 923 bytes
from django.db import models, migrations
import django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('workers', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='position', options={'ordering': ('order', )}),
     migrations.AddField(model_name='position', name='order', field=models.IntegerField(default=0, verbose_name='Order'), preserve_default=True),
     migrations.AlterField(model_name='position', name='slug', field=django_extensions.db.fields.AutoSlugField(allow_duplicates=False, separator=b'\'"u\\\'-\\\'"\'', blank=True, populate_from=b'\'"\\\'title\\\'"\'', editable=False, verbose_name='slug', overwrite=False), preserve_default=True)]