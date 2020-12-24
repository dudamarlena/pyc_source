# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangopost\src\djangopost\migrations\0003_auto_20200330_0717.py
# Compiled at: 2020-03-29 21:47:07
# Size of source mod 2**32: 1159 bytes
from django.db import migrations, models
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
     ('djangopost', '0002_articlemodel_tags')]
    operations = [
     migrations.AlterModelOptions(name='articlemodel',
       options={'ordering':[
       '-pk'], 
      'verbose_name':'Djangopost article',  'verbose_name_plural':'Djangopost articles'}),
     migrations.AlterModelOptions(name='categorymodel',
       options={'ordering':[
       '-pk'], 
      'verbose_name':'Djangopost category',  'verbose_name_plural':'Djangopost categories'}),
     migrations.AddField(model_name='articlemodel',
       name='is_promotional',
       field=models.BooleanField(default=False)),
     migrations.AlterField(model_name='articlemodel',
       name='tags',
       field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'))]