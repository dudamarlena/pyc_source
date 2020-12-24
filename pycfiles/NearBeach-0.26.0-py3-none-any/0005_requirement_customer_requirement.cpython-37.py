# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/migrations/0005_requirement_customer_requirement.py
# Compiled at: 2020-03-01 01:12:02
# Size of source mod 2**32: 546 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('NearBeach', '0004_requirement_customer')]
    operations = [
     migrations.AddField(model_name='requirement_customer',
       name='requirement',
       field=models.ForeignKey(default=1, on_delete=(django.db.models.deletion.CASCADE), to='NearBeach.requirement'),
       preserve_default=False)]