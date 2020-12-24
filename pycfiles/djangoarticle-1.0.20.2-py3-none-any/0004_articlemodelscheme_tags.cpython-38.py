# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoarticle\src\djangoarticle\migrations\0004_articlemodelscheme_tags.py
# Compiled at: 2020-03-09 03:42:44
# Size of source mod 2**32: 601 bytes
from django.db import migrations
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0003_taggeditem_add_unique_index'),
     ('djangoarticle', '0003_auto_20191122_1605')]
    operations = [
     migrations.AddField(model_name='articlemodelscheme',
       name='tags',
       field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'))]