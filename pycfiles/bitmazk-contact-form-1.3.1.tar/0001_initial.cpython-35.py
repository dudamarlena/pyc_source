# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/migrations/0001_initial.py
# Compiled at: 2016-04-11 01:51:28
# Size of source mod 2**32: 1517 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name='ContactFormCategory', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'slug', models.SlugField(max_length=256, verbose_name='Slug'))], options={'abstract': False}),
     migrations.CreateModel(name='ContactFormCategoryTranslation', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'name', models.CharField(max_length=256)),
      (
       'language_code', models.CharField(max_length=15, db_index=True)),
      (
       'master', models.ForeignKey(related_name='translations', editable=False, to='contact_form.ContactFormCategory', null=True))], options={'managed': True, 
      'abstract': False, 
      'db_table': 'contact_form_contactformcategory_translation', 
      'db_tablespace': ''}),
     migrations.AlterUniqueTogether(name='contactformcategorytranslation', unique_together=set([('language_code', 'master')]))]