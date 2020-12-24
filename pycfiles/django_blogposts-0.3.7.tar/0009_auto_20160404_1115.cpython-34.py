# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/migrations/0009_auto_20160404_1115.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 728 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogposts', '0008_auto_20160301_1015')]
    operations = [
     migrations.AlterField(model_name='blogpost', name='image', field=models.ImageField(blank=True, null=True, upload_to=b'blog/%Y/%m/%d', verbose_name='Image')),
     migrations.AlterField(model_name='blogpost', name='short_content', field=models.TextField(blank=True, null=True, verbose_name='Short content for preview'))]