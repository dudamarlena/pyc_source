# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0006_basesegment_model_obj.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 663 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0008_auto_20181211_1552'),
     ('segments', '0005_remove_basesegment_model_obj')]
    operations = [
     migrations.AddField(model_name='basesegment',
       name='model_obj',
       field=models.ManyToManyField(through='segments.SegmentSort', to='basemodels.BaseModel', verbose_name='\\u0686\\u0647 \\u0686\\u06cc\\u0632 \\u0631\\u0627 \\u0646\\u0645\\u0627\\u06cc\\u0634 \\u062f\\u0647\\u062f\\u061f'))]