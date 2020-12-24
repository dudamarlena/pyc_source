# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0009_auto_20200316_1110.py
# Compiled at: 2020-03-16 03:40:40
# Size of source mod 2**32: 1721 bytes
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0008_auto_20190615_1430')]
    operations = [
     migrations.AlterModelOptions(name='file',
       options={'ordering':[
       '-created_at'], 
      'verbose_name':'File',  'verbose_name_plural':'Files'}),
     migrations.AlterField(model_name='file',
       name='banner',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_banner', to='filefields.FileField', verbose_name='Banner Image')),
     migrations.AlterField(model_name='file',
       name='cover',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_cover', to='filefields.FileField', verbose_name='Cover Image')),
     migrations.AlterField(model_name='file',
       name='description',
       field=models.TextField(blank=True, null=True, verbose_name='Description')),
     migrations.AlterField(model_name='file',
       name='file_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_obj', to='filefields.FileField', verbose_name='File')),
     migrations.AlterField(model_name='file',
       name='publish_date',
       field=models.DateTimeField(default=(django.utils.timezone.now), verbose_name='Publish Date'))]