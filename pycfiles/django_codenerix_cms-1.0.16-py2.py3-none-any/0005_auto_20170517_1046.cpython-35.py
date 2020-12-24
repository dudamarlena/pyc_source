# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/migrations/0005_auto_20170517_1046.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 1182 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_cms', '0004_auto_20170428_0850')]
    operations = [
     migrations.CreateModel(name='StaticPageAuthor', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated'))], options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 
      'abstract': False}),
     migrations.AddField(model_name='staticpage', name='author', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staticpages', to='codenerix_cms.StaticPageAuthor'))]