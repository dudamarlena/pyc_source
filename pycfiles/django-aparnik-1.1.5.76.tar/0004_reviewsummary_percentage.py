# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0004_reviewsummary_percentage.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('reviews', '0003_reviewsummary')]
    operations = [
     migrations.AddField(model_name=b'reviewsummary', name=b'percentage', field=models.FloatField(default=10, verbose_name=b'Percentage'), preserve_default=False)]