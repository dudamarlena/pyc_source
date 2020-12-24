# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/Develop/django-feedly/feedly/migrations/0001_initial.py
# Compiled at: 2017-02-28 14:13:34
from __future__ import unicode_literals
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Basket', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(default=b'++', max_length=2)),
      (
       b'deliverable', models.BooleanField(default=False)),
      (
       b'product', models.IntegerField(default=1)),
      (
       b'date', models.DateTimeField(auto_now_add=True)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'+', to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name=b'Followed', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'followed', models.IntegerField(default=1)),
      (
       b'follower', models.IntegerField(default=2)),
      (
       b'date', models.DateTimeField(auto_now_add=True))]),
     migrations.CreateModel(name=b'Page', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(default=b'!#', max_length=50)),
      (
       b'content', models.TextField(default=b'')),
      (
       b'date', models.DateTimeField(auto_now_add=True)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'+', to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name=b'Profile', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'coins', models.IntegerField(default=0)),
      (
       b'visual', models.CharField(default=b'', max_length=100)),
      (
       b'career', models.CharField(default=b'', max_length=50)),
      (
       b'birthday', models.DateTimeField(default=datetime.date(2017, 2, 28))),
      (
       b'google_token', models.TextField(default=b'', max_length=120)),
      (
       b'twitter_token', models.TextField(default=b'', max_length=120)),
      (
       b'facebook_token', models.TextField(default=b'', max_length=120)),
      (
       b'bio', models.TextField(default=b'', max_length=140)),
      (
       b'date', models.DateTimeField(auto_now_add=True)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'+', to=settings.AUTH_USER_MODEL, unique=True))]),
     migrations.CreateModel(name=b'Sellable', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(default=b'$$', max_length=100)),
      (
       b'paid', models.BooleanField(default=False)),
      (
       b'returnable', models.BooleanField(default=False)),
      (
       b'value', models.FloatField(default=1.0)),
      (
       b'visual', models.CharField(default=b'', max_length=150)),
      (
       b'sellid', models.IntegerField(default=1)),
      (
       b'date', models.DateTimeField(auto_now_add=True)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'+', to=settings.AUTH_USER_MODEL))])]