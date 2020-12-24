# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0003_reviewsummary.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0003_basemodel_update_needed'),
     ('reviews', '0002_auto_20181025_1543')]
    operations = [
     migrations.CreateModel(name=b'ReviewSummary', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'rate', models.CharField(max_length=1, verbose_name=b'Rate')),
      (
       b'count', models.BigIntegerField(default=0, verbose_name=b'Count')),
      (
       b'model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'review_summaries', to=b'basemodels.BaseModel', verbose_name=b'Models'))], options={b'verbose_name': b'Reivew Summary', 
        b'verbose_name_plural': b'Review Summary'})]