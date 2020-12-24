# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/migrations/0001_initial.py
# Compiled at: 2017-01-30 12:18:04
# Size of source mod 2**32: 3192 bytes
from __future__ import unicode_literals
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='Attribute', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=256)),
      (
       'long_name', models.CharField(blank=True, max_length=512)),
      (
       'index', models.IntegerField()),
      (
       'choices', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), null=True, size=None)),
      (
       'default', models.CharField(blank=True, max_length=256)),
      (
       'required', models.BooleanField(default=False)),
      (
       'omit', models.BooleanField(default=False))], options={'ordering': ('schema', 'index')}),
     migrations.CreateModel(name='AttributeType', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=256)),
      (
       'label', models.CharField(max_length=512)),
      (
       'form_field', models.CharField(max_length=256)),
      (
       'widget', models.CharField(blank=True, max_length=256, null=True)),
      (
       'validator_re', models.CharField(blank=True, max_length=512, null=True)),
      (
       'validator_type', models.CharField(blank=True, max_length=256, null=True))]),
     migrations.CreateModel(name='Schema', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'selectors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=256), blank=True, default=list, size=None)),
      (
       'content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'))]),
     migrations.AddField(model_name='attribute', name='attr_type', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsonattrs.AttributeType')),
     migrations.AddField(model_name='attribute', name='schema', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='jsonattrs.Schema')),
     migrations.AlterUniqueTogether(name='schema', unique_together=set([('content_type', 'selectors')])),
     migrations.AlterUniqueTogether(name='attribute', unique_together=set([('schema', 'name'), ('schema', 'index')]))]