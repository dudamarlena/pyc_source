# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/migrations/0012_questionpage_to_page.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1599 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sites', '0002_alter_domain_unique'),
     ('wizard_builder', '0011_rename_questionpage_attrs')]
    operations = [
     migrations.CreateModel(name='Page',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'position',
       models.PositiveSmallIntegerField(default=0,
         verbose_name='position')),
      (
       'section',
       models.IntegerField(choices=[
        (1, 'When'), (2, 'Where'), (3, 'What'), (4, 'Who')],
         default=1)),
      (
       'infobox',
       models.TextField(blank=True,
         verbose_name='why is this asked? wrap additional titles in [[double brackets]]')),
      (
       'sites', models.ManyToManyField(to='sites.Site'))],
       options={'ordering': ['position']})]