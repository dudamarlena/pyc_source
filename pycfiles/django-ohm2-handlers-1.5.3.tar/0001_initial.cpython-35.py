# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/socialstatistics/migrations/0001_initial.py
# Compiled at: 2016-12-07 10:08:32
# Size of source mod 2**32: 7230 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Facebook', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'name', models.CharField(max_length=512)),
      (
       'account_id', models.CharField(max_length=512)),
      (
       'access_token', models.CharField(max_length=2048)),
      (
       'token_type', models.CharField(max_length=512)),
      (
       'expiration', models.DateTimeField(blank=True, default=None, null=True)),
      (
       'deleted', models.BooleanField(default=False)),
      (
       'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={'abstract': False}),
     migrations.CreateModel(name='FacebookPage', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'name', models.CharField(max_length=512)),
      (
       'page_id', models.CharField(max_length=2048)),
      (
       'deleted', models.BooleanField(default=False)),
      (
       'facebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialstatistics.Facebook'))], options={'abstract': False}),
     migrations.CreateModel(name='FacebookPageSnapshot', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'country_page_likes', models.PositiveIntegerField()),
      (
       'fan_count', models.PositiveIntegerField()),
      (
       'new_like_count', models.PositiveIntegerField()),
      (
       'rating_count', models.PositiveIntegerField()),
      (
       'talking_about_count', models.PositiveIntegerField()),
      (
       'page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialstatistics.FacebookPage'))], options={'abstract': False}),
     migrations.CreateModel(name='LastFacebookPageSnapshot', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='socialstatistics.FacebookPage')),
      (
       'snapshot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='socialstatistics.FacebookPageSnapshot'))], options={'abstract': False}),
     migrations.CreateModel(name='LastTwitterSnapshot', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now))], options={'abstract': False}),
     migrations.CreateModel(name='Twitter', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'name', models.CharField(max_length=512)),
      (
       'account_id', models.CharField(max_length=512)),
      (
       'access_token', models.CharField(max_length=2048)),
      (
       'access_token_secret', models.CharField(max_length=2048)),
      (
       'expiration', models.DateTimeField(blank=True, default=None, null=True)),
      (
       'deleted', models.BooleanField(default=False)),
      (
       'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={'abstract': False}),
     migrations.CreateModel(name='TwitterSnapshot', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'tweets', models.PositiveIntegerField()),
      (
       'following', models.PositiveIntegerField()),
      (
       'followers', models.PositiveIntegerField()),
      (
       'twitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialstatistics.Twitter'))], options={'abstract': False}),
     migrations.AddField(model_name='lasttwittersnapshot', name='snapshot', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='socialstatistics.TwitterSnapshot')),
     migrations.AddField(model_name='lasttwittersnapshot', name='twitter', field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='socialstatistics.Twitter'))]