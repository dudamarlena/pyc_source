# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0003_article_category.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0002_category')]
    operations = [
     migrations.AddField(model_name=b'article', name=b'category', field=models.ForeignKey(blank=True, help_text=b'The parent category for the article.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'helpcenter.Category', verbose_name=b'Article Category'))]