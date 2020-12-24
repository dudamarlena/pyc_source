# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\vryhofa\workspace\django-wordpress-rss\htdocs\django_blogconnector\migrations\0003_auto_20190510_1517.py
# Compiled at: 2019-05-10 15:17:28
# Size of source mod 2**32: 623 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogconnector', '0002_auto_20190510_1258')]
    operations = [
     migrations.AddField(model_name='blogcategory',
       name='slug',
       field=models.SlugField(blank=True, max_length=200, null=True)),
     migrations.AddField(model_name='blogpost',
       name='slug',
       field=models.SlugField(blank=True, max_length=200, null=True))]