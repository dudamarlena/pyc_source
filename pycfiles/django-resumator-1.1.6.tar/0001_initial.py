# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/AmmsA/django-resumator/resumator/migrations/0001_initial.py
# Compiled at: 2015-11-23 01:31:40
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'BasicInformation', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(default=b'John Smith', max_length=25)),
      (
       b'short_bio', models.CharField(default=b'My short bio', max_length=100, verbose_name=b'short bio', blank=True)),
      (
       b'long_bio', models.TextField(default=b'My long bio', verbose_name=b'long bio', blank=True)),
      (
       b'email', models.EmailField(default=b'email@example.com', max_length=254)),
      (
       b'github', models.URLField(blank=True)),
      (
       b'linkedin', models.URLField(blank=True)),
      (
       b'image', models.ImageField(upload_to=b'media/images', blank=True))], options={b'abstract': False}),
     migrations.CreateModel(name=b'Education', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=50, verbose_name=b'University name')),
      (
       b'abbreviation', models.CharField(default=None, max_length=10, verbose_name=b'Degree abbreviation', blank=True)),
      (
       b'start_date', models.DateField(null=True, verbose_name=b'start date', blank=True)),
      (
       b'end_date', models.DateField(null=True, verbose_name=b'end date', blank=True)),
      (
       b'major', models.CharField(default=None, max_length=50, blank=True)),
      (
       b'gpa', models.CharField(default=None, max_length=10, verbose_name=b'GPA', blank=True))], options={b'ordering': [
                    b'-end_date']}),
     migrations.CreateModel(name=b'Experience', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'company', models.CharField(max_length=50)),
      (
       b'role', models.CharField(max_length=150)),
      (
       b'start_date', models.DateField(null=True, verbose_name=b'start date', blank=True)),
      (
       b'end_date', models.DateField(null=True, verbose_name=b'end date', blank=True)),
      (
       b'description', models.TextField(default=None, verbose_name=b'description')),
      (
       b'link', models.URLField(blank=True)),
      (
       b'image', models.ImageField(upload_to=b'', blank=True))], options={b'ordering': [
                    b'-end_date']}),
     migrations.CreateModel(name=b'Language', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=50)),
      (
       b'experience', models.ManyToManyField(to=b'resumator.Experience', blank=True))]),
     migrations.CreateModel(name=b'Project', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=50)),
      (
       b'description', models.TextField(default=None, verbose_name=b'description', blank=True)),
      (
       b'start_date', models.DateField(null=True, verbose_name=b'start date', blank=True)),
      (
       b'end_date', models.DateField(null=True, verbose_name=b'end date', blank=True)),
      (
       b'link', models.URLField(blank=True))]),
     migrations.CreateModel(name=b'Publication', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'title', models.CharField(max_length=100)),
      (
       b'authors', models.CharField(max_length=200, blank=True)),
      (
       b'conference', models.CharField(max_length=200, blank=True)),
      (
       b'abstract', models.TextField(blank=True)),
      (
       b'year', models.CharField(max_length=4, blank=True)),
      (
       b'link', models.URLField(blank=True))], options={b'ordering': [
                    b'-year']}),
     migrations.AddField(model_name=b'language', name=b'projects', field=models.ManyToManyField(to=b'resumator.Project', blank=True))]