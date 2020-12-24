# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0016_auto_20191021_0958.py
# Compiled at: 2019-11-22 18:06:23
# Size of source mod 2**32: 2205 bytes
from django.db import migrations
import django.db.models.manager

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0015_auto_20191001_0847')]
    operations = [
     migrations.AlterModelManagers(name='displaycolor',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='issuetype',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='projectstatus',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='projecttype',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='queue',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='source',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='subissuetype',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='ticketpriority',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='ticketstatus',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())]),
     migrations.AlterModelManagers(name='tickettype',
       managers=[
      (
       'available_objects', django.db.models.manager.Manager())])]