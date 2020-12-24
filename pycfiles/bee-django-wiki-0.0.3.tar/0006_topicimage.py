# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_wiki/migrations/0006_topicimage.py
# Compiled at: 2019-09-03 06:22:28
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_wiki', '0005_auto_20190903_1714')]
    operations = [
     migrations.CreateModel(name=b'TopicImage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'image', models.ImageField(upload_to=b'wiki/%Y/%m/%d', verbose_name=b'图片'))], options={b'db_table': b'bee_django_wiki_toipc_image'})]