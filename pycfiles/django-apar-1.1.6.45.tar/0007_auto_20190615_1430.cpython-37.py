# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0007_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1851 bytes
import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0006_auto_20190120_1724')]
    operations = [
     migrations.AlterModelOptions(name='button',
       options={'verbose_name':'باتن', 
      'verbose_name_plural':'باتن ها'}),
     migrations.AlterModelOptions(name='buttonsegment',
       options={'verbose_name':'بخش باتن', 
      'verbose_name_plural':'بخش باتن ها'}),
     migrations.AlterField(model_name='button',
       name='background_color',
       field=colorfield.fields.ColorField(default='#2672DF', max_length=18, verbose_name='رنگ پس زمینه')),
     migrations.AlterField(model_name='button',
       name='icon',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='filefields.FileField', verbose_name='آیکن')),
     migrations.AlterField(model_name='button',
       name='icon_color',
       field=colorfield.fields.ColorField(default='#2672DF', max_length=18, verbose_name='رنگ آیکن')),
     migrations.AlterField(model_name='button',
       name='model_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='button_model', to='basemodels.BaseModel', verbose_name='چه چیز را نمایش دهد؟')),
     migrations.AlterField(model_name='button',
       name='title',
       field=models.CharField(blank=True, max_length=255, null=True, verbose_name='عنوان'))]