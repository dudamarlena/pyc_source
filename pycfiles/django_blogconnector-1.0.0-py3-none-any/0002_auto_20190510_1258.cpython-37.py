# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\vryhofa\workspace\django-wordpress-rss\htdocs\django_blogconnector\migrations\0002_auto_20190510_1258.py
# Compiled at: 2019-05-10 12:58:39
# Size of source mod 2**32: 905 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogconnector', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='blogcategory',
       options={'verbose_name':'Category', 
      'verbose_name_plural':'Categories'}),
     migrations.AlterModelOptions(name='blogpost',
       options={'verbose_name':'Post', 
      'verbose_name_plural':'Posts'}),
     migrations.AlterModelOptions(name='blogsource',
       options={'verbose_name':'Blog', 
      'verbose_name_plural':'Blogs'}),
     migrations.AlterModelOptions(name='bloguser',
       options={'verbose_name':'Blog User', 
      'verbose_name_plural':'Blog Users'})]