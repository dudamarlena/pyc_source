# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0003_reviewsummary.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1057 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0003_basemodel_update_needed'),
     ('reviews', '0002_auto_20181025_1543')]
    operations = [
     migrations.CreateModel(name='ReviewSummary',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'rate', models.CharField(max_length=1, verbose_name='Rate')),
      (
       'count', models.BigIntegerField(default=0, verbose_name='Count')),
      (
       'model', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='review_summaries', to='basemodels.BaseModel', verbose_name='Models'))],
       options={'verbose_name':'Reivew Summary', 
      'verbose_name_plural':'Review Summary'})]