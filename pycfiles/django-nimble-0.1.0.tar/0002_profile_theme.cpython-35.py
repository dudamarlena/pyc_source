# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\migrations\0002_profile_theme.py
# Compiled at: 2016-12-18 13:13:20
# Size of source mod 2**32: 856 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nimble', '0001_initial')]
    operations = [
     migrations.AddField(model_name='profile', name='theme', field=models.CharField(choices=[
      ('1', 'Cerulean'), ('2', 'Cosmo'), ('3', 'Cyborg'),
      ('4', 'Darkly'), ('5', 'Flatly'), ('6', 'Journal'),
      ('7', 'Lumen'), ('8', 'Paper'), ('9', 'Readable'),
      ('10', 'Sandstone'), ('11', 'Simplex'), ('12', 'Slate'),
      ('13', 'Spacelab'), ('14', 'Superhero'), ('15', 'United'),
      ('16', 'Yeti')], default='1', max_length=2))]