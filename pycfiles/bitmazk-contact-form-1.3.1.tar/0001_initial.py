# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/migrations/0001_initial.py
# Compiled at: 2016-04-11 01:51:28
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'ContactFormCategory', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'slug', models.SlugField(max_length=256, verbose_name=b'Slug'))], options={b'abstract': False}),
     migrations.CreateModel(name=b'ContactFormCategoryTranslation', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=256)),
      (
       b'language_code', models.CharField(max_length=15, db_index=True)),
      (
       b'master', models.ForeignKey(related_name=b'translations', editable=False, to=b'contact_form.ContactFormCategory', null=True))], options={b'managed': True, 
        b'abstract': False, 
        b'db_table': b'contact_form_contactformcategory_translation', 
        b'db_tablespace': b''}),
     migrations.AlterUniqueTogether(name=b'contactformcategorytranslation', unique_together=set([('language_code', 'master')]))]