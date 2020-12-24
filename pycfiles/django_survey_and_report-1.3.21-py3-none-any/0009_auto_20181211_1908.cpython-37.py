# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/migrations/0009_auto_20181211_1908.py
# Compiled at: 2019-03-02 04:36:34
# Size of source mod 2**32: 1040 bytes
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('survey', '0008_translated_name_for_models')]
    operations = [
     migrations.AlterField(model_name='question',
       name='category',
       field=models.ForeignKey(blank=True,
       null=True,
       on_delete=(django.db.models.deletion.SET_NULL),
       related_name='questions',
       to='survey.Category',
       verbose_name='Category')),
     migrations.AlterField(model_name='response',
       name='user',
       field=models.ForeignKey(blank=True,
       null=True,
       on_delete=(django.db.models.deletion.SET_NULL),
       to=(settings.AUTH_USER_MODEL),
       verbose_name='User'))]