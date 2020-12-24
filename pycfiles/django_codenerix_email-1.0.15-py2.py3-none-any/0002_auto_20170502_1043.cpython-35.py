# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_email/migrations/0002_auto_20170502_1043.py
# Compiled at: 2017-05-02 12:38:45
# Size of source mod 2**32: 2369 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_email', '0001_initial')]
    operations = [
     migrations.CreateModel(name='EmailTemplateTextEN', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'subject', models.TextField(blank=True, verbose_name='Subject')),
      (
       'body', models.TextField(blank=True, verbose_name='Body'))], options={'abstract': False}),
     migrations.CreateModel(name='EmailTemplateTextES', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'subject', models.TextField(blank=True, verbose_name='Subject')),
      (
       'body', models.TextField(blank=True, verbose_name='Body'))], options={'abstract': False}),
     migrations.RemoveField(model_name='emailtemplate', name='body'),
     migrations.RemoveField(model_name='emailtemplate', name='subject'),
     migrations.AddField(model_name='emailtemplatetextes', name='email_template', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='es', to='codenerix_email.EmailTemplate')),
     migrations.AddField(model_name='emailtemplatetexten', name='email_template', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='en', to='codenerix_email.EmailTemplate'))]