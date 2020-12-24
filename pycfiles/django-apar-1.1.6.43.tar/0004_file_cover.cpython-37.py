# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0004_file_cover.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 677 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0004_filefield_title'),
     ('files', '0003_remove_file_is_preview')]
    operations = [
     migrations.AddField(model_name='file',
       name='cover',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_cover', to='filefields.FileField', verbose_name='\\u062a\\u0635\\u0648\\u06cc\\u0631 \\u062c\\u0644\\u062f'))]