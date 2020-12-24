# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/listing/tests/migrations/0001_initial.py
# Compiled at: 2017-05-06 10:55:04
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('jmbo', '0003_auto_20160530_1247')]
    operations = [
     migrations.CreateModel(name=b'ModelA', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase'))], bases=('jmbo.modelbase', )),
     migrations.CreateModel(name=b'ModelB', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase'))], bases=('jmbo.modelbase', ))]