# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/migrations/0004_auto_20200329_1013.py
# Compiled at: 2020-03-29 06:13:14
# Size of source mod 2**32: 762 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('NearBeach', '0003_auto_20200308_0542')]
    operations = [
     migrations.AddField(model_name='object_assignment',
       name='customer',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='NearBeach.customer')),
     migrations.AddField(model_name='object_assignment',
       name='organisation',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='NearBeach.organisation'))]