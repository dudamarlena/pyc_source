# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/migrations/0002_auto_20151022_1637.py
# Compiled at: 2015-10-22 12:37:46
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('luhublog', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'author', name=b'linkedin_plus_url', field=models.URLField(verbose_name=b'URL Perfil Linkedin', blank=True)),
     migrations.AlterField(model_name=b'author', name=b'twitter_url', field=models.URLField(verbose_name=b'URL Perfil Twitter', blank=True))]