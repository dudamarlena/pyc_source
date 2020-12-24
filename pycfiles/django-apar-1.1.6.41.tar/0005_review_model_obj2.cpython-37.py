# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0005_review_model_obj2.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 635 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0011_auto_20190612_1035'),
     ('reviews', '0004_reviewsummary_percentage')]
    operations = [
     migrations.AddField(model_name='review',
       name='model_obj2',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='reviews_set', to='basemodels.BaseModel', verbose_name='Model'))]