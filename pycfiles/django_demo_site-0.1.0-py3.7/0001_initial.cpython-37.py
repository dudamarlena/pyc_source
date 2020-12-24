# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\demo_site\migrations\0001_initial.py
# Compiled at: 2018-10-03 09:19:15
# Size of source mod 2**32: 2445 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='AccessToken',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'token', models.CharField(max_length=20, verbose_name='Access token')),
      (
       'success_url', models.URLField(verbose_name='Success url')),
      (
       'valid', models.BooleanField(default=True, verbose_name='Valid')),
      (
       'feature_access', models.CharField(blank=True, max_length=20, null=True, verbose_name='Feature access'))]),
     migrations.CreateModel(name='DemoSiteSettings',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(default='Demo site', max_length=100, verbose_name='Title')),
      (
       'text', models.TextField(default='This is a demo site', verbose_name='Text')),
      (
       'status', models.CharField(blank=True, choices=[('alpha', 'Alpha'), ('beta', 'Beta'), ('rc', 'Release candidate'), ('final', 'Final release')], max_length=50, null=True, verbose_name='Status')),
      (
       'version', models.CharField(blank=True, default='0.1.0', max_length=50, null=True, verbose_name='Version')),
      (
       'final_release_date', models.DateTimeField(blank=True, null=True, verbose_name='Final release date')),
      (
       'demo_available_until_date', models.DateTimeField(blank=True, null=True, verbose_name='Demo available until date')),
      (
       'contact_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Contact email')),
      (
       'issue_handler', models.URLField(blank=True, null=True, verbose_name='Issue handler')),
      (
       'project_page', models.URLField(blank=True, null=True, verbose_name='Project page')),
      (
       'requires_access_token', models.BooleanField(default=False, verbose_name='Requires access token')),
      (
       'default_success_url', models.CharField(default='/demo/', max_length=50, verbose_name='Default success url'))])]