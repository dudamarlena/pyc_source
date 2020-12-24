# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sbarnett/Dropbox/Dev/Django/the_cake_club/teamgroups/migrations/0001_initial.py
# Compiled at: 2015-07-27 14:39:03
from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'TeamGroup', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=100)),
      (
       b'slug', models.SlugField(unique=True))], options={b'permissions': (('view_teamgroup', 'Can view teamgroup'), )}),
     migrations.CreateModel(name=b'TeamGroupInvitation', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'email', models.EmailField(max_length=254)),
      (
       b'accepted', models.BooleanField(default=False)),
      (
       b'key', models.CharField(unique=True, max_length=64)),
      (
       b'date_invited', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'inviter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
      (
       b'teamgroup', models.ForeignKey(related_name=b'invitations', to=b'teamgroups.TeamGroup'))]),
     migrations.CreateModel(name=b'TeamGroupMembership', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'role', models.CharField(default=b'member', max_length=20, choices=[('owner', '<strong>Owner</strong><br>The person who is            the primary contact for the team group. Owners can modify or            delete the team group.'), ('manager', '<strong>Manager</strong><br>Allowed to            modify the team group.'), ('member', '<strong>Member</strong><br>Can view the             team group but is not allowed to modify it.')])),
      (
       b'active', models.BooleanField(default=True)),
      (
       b'member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
      (
       b'teamgroup', models.ForeignKey(related_name=b'memberships', to=b'teamgroups.TeamGroup'))]),
     migrations.AddField(model_name=b'teamgroup', name=b'members', field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through=b'teamgroups.TeamGroupMembership'))]