# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0070_mycompanyother.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 654 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0069_auto_20180815_1116')]
    operations = [
     migrations.CreateModel(name='MyCompanyOther',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'default_calendar', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.Calendar'))])]