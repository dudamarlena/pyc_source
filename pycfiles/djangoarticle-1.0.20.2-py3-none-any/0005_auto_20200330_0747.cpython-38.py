# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoarticle\src\djangoarticle\migrations\0005_auto_20200330_0747.py
# Compiled at: 2020-03-29 22:17:42
# Size of source mod 2**32: 1204 bytes
from django.db import migrations, models
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
     ('djangoarticle', '0004_articlemodelscheme_tags')]
    operations = [
     migrations.AlterModelOptions(name='articlemodelscheme',
       options={'ordering':[
       '-pk'], 
      'verbose_name':'Djangoarticle article',  'verbose_name_plural':'Djangoarticle articles'}),
     migrations.AlterModelOptions(name='categorymodelscheme',
       options={'ordering':[
       '-pk'], 
      'verbose_name':'Djangoarticle category',  'verbose_name_plural':'Djangoarticle categories'}),
     migrations.AddField(model_name='articlemodelscheme',
       name='is_promotional',
       field=models.BooleanField(default=False)),
     migrations.AlterField(model_name='articlemodelscheme',
       name='tags',
       field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'))]