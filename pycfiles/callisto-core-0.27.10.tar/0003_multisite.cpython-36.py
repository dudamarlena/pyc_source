# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0003_multisite.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1206 bytes
from __future__ import unicode_literals
import django.db.models.deletion, django.db.models.manager
from django.db import migrations, models
import callisto_core.wizard_builder.models

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0001_initial'),
     ('wizard_builder', '0002_remove_formquestion_example')]
    operations = [
     migrations.AlterModelManagers(name='questionpage',
       managers=[
      (
       'objects', django.db.models.manager.Manager()),
      (
       'base_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='textpage',
       managers=[
      (
       'objects', django.db.models.manager.Manager()),
      (
       'base_objects', django.db.models.manager.Manager())]),
     migrations.AddField(model_name='pagebase',
       name='site',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
       to='sites.Site',
       null=True))]