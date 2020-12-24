# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/migrations/0001_initial.py
# Compiled at: 2016-08-21 23:09:38
# Size of source mod 2**32: 1575 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Attachment', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'file', models.FileField(upload_to=''))]),
     migrations.CreateModel(name='Email', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'headers', models.TextField()),
      (
       'text', models.TextField()),
      (
       'html', models.TextField()),
      (
       'to', models.TextField()),
      (
       'cc', models.TextField()),
      (
       'subject', models.TextField()),
      (
       'dkim', jsonfield.fields.JSONField()),
      (
       'SPF', jsonfield.fields.JSONField()),
      (
       'envelope', jsonfield.fields.JSONField()),
      (
       'charsets', models.CharField(max_length=255)),
      (
       'spam_score', models.FloatField()),
      (
       'spam_report', models.TextField()),
      (
       'attachments', models.ManyToManyField(related_name='email', to='django_sendgrid_parse.Attachment'))])]