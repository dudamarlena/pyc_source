# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0007_auto_20190613_1829.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 770 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('reviews', '0006_auto_20190613_1815'),
     ('questionanswers', '0005_auto_20190613_1815')]
    operations = [
     migrations.RemoveField(model_name='basereview',
       name='model_obj'),
     migrations.AlterField(model_name='review',
       name='model_obj2',
       field=models.ForeignKey(default=1, on_delete=(django.db.models.deletion.CASCADE), related_name='reviews_set', to='basemodels.BaseModel', verbose_name='Model'),
       preserve_default=False)]