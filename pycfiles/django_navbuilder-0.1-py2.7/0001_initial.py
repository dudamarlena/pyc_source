# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/migrations/0001_initial.py
# Compiled at: 2017-01-25 06:30:30
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('link', '__first__')]
    operations = [
     migrations.CreateModel(name=b'Menu', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'slug', models.SlugField(max_length=256))], options={b'ordering': [
                    b'title']}),
     migrations.CreateModel(name=b'MenuItem', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'slug', models.SlugField(max_length=256)),
      (
       b'position', models.PositiveIntegerField()),
      (
       b'link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'link.Link')),
      (
       b'menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'menuitems', to=b'navbuilder.Menu')),
      (
       b'parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'submenuitems', to=b'navbuilder.MenuItem'))], options={b'ordering': [
                    b'title']})]