# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0002_auto_20181026_1745.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1580 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='file',
       options={'ordering':[
       '-created_at'], 
      'verbose_name':'\\u0641\\u0627\\u06cc\\u0644',  'verbose_name_plural':'\\u0641\\u0627\\u06cc\\u0644 \\u0647\\u0627'}),
     migrations.AlterField(model_name='file',
       name='banner',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_banner', to='filefields.FileField', verbose_name='\\u0628\\u0646\\u0631')),
     migrations.AlterField(model_name='file',
       name='description',
       field=models.TextField(blank=True, null=True, verbose_name='\\u062a\\u0648\\u0636\\u06cc\\u062d\\u0627\\u062a')),
     migrations.AlterField(model_name='file',
       name='file_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_obj', to='filefields.FileField', verbose_name='\\u0641\\u0627\\u06cc\\u0644')),
     migrations.AlterField(model_name='file',
       name='is_preview',
       field=models.BooleanField(default=False, verbose_name='\\u067e\\u06cc\\u0634 \\u0646\\u0645\\u0627\\u06cc\\u0634\\u061f'))]