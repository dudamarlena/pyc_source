# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0004_auto_20160607_1234.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0003_article_category')]
    operations = [
     migrations.AlterModelOptions(name=b'category', options={b'verbose_name_plural': b'categories'}),
     migrations.AlterField(model_name=b'article', name=b'title', field=models.CharField(db_index=True, help_text=b'An article title is restricted to 200 characters.', max_length=200, verbose_name=b'Article Title'))]