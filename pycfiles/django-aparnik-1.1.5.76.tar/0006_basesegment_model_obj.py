# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0006_basesegment_model_obj.py
# Compiled at: 2018-12-14 08:14:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0008_auto_20181211_1552'),
     ('segments', '0005_remove_basesegment_model_obj')]
    operations = [
     migrations.AddField(model_name=b'basesegment', name=b'model_obj', field=models.ManyToManyField(through=b'segments.SegmentSort', to=b'basemodels.BaseModel', verbose_name=b'چه چیز را نمایش دهد؟'))]