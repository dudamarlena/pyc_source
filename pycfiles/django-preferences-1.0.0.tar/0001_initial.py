# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/tests/migrations/0001_initial.py
# Compiled at: 2018-12-20 03:13:26
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('preferences', '0002_auto_20181220_0803')]
    operations = [
     migrations.CreateModel(name=b'MyPreferences', fields=[
      (
       b'preferences_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'preferences.Preferences')),
      (
       b'portal_contact_email', models.EmailField(max_length=254))], bases=('preferences.preferences', ))]