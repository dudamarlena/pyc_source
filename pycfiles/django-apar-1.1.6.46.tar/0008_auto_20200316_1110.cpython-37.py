# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0008_auto_20200316_1110.py
# Compiled at: 2020-03-16 03:40:40
# Size of source mod 2**32: 1786 bytes
import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0007_auto_20190615_1430')]
    operations = [
     migrations.AlterModelOptions(name='button',
       options={'verbose_name':'Button', 
      'verbose_name_plural':'Buttons'}),
     migrations.AlterModelOptions(name='buttonsegment',
       options={'verbose_name':'Button Segment', 
      'verbose_name_plural':'Button Segments'}),
     migrations.AlterField(model_name='button',
       name='background_color',
       field=colorfield.fields.ColorField(default='#2672DF', max_length=18, verbose_name='Background Color')),
     migrations.AlterField(model_name='button',
       name='icon',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='filefields.FileField', verbose_name='Icon')),
     migrations.AlterField(model_name='button',
       name='icon_color',
       field=colorfield.fields.ColorField(default='#2672DF', max_length=18, verbose_name='Icon color')),
     migrations.AlterField(model_name='button',
       name='model_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='button_model', to='basemodels.BaseModel', verbose_name='Model')),
     migrations.AlterField(model_name='button',
       name='title',
       field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'))]