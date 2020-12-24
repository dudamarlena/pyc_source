# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0004_auto_20190913_1425.py
# Compiled at: 2019-10-01 19:08:49
# Size of source mod 2**32: 1430 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0003_auto_20190913_0941')]
    operations = [
     migrations.CreateModel(name='Resource', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'user_name', models.CharField(max_length=32)),
      (
       'email', models.CharField(max_length=50)),
      (
       'first_name', models.CharField(max_length=50)),
      (
       'last_name', models.CharField(max_length=50)),
      (
       'active', models.BooleanField(default=False))], options={'ordering': ('first_name', 'last_name')}),
     migrations.AddField(model_name='ticket', name='assigned_resource', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Resource'))]