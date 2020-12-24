# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/migrations/0002_observationalert.py
# Compiled at: 2019-08-13 09:00:38
# Size of source mod 2**32: 749 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('tom_observations', '0003_auto_20190503_2318'),
     ('tom_education', '0001_initial')]
    operations = [
     migrations.CreateModel(name='ObservationAlert',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'email', models.EmailField(max_length=254)),
      (
       'observation', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='tom_observations.ObservationRecord'))])]