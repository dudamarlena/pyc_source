# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/migrations/0003_requirement_organisation.py
# Compiled at: 2020-03-01 01:12:02
# Size of source mod 2**32: 510 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('NearBeach', '0002_initialise_data')]
    operations = [
     migrations.AddField(model_name='requirement',
       name='organisation',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='NearBeach.organisation'))]