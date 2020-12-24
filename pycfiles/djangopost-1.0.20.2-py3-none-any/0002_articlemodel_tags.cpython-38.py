# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangopost\src\djangopost\migrations\0002_articlemodel_tags.py
# Compiled at: 2020-03-08 00:29:23
# Size of source mod 2**32: 581 bytes
from django.db import migrations
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0003_taggeditem_add_unique_index'),
     ('djangopost', '0001_initial')]
    operations = [
     migrations.AddField(model_name='articlemodel',
       name='tags',
       field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'))]