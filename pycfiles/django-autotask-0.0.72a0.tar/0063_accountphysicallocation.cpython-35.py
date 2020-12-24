# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0063_accountphysicallocation.py
# Compiled at: 2020-05-12 14:17:57
# Size of source mod 2**32: 822 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0062_task_department')]
    operations = [
     migrations.CreateModel(name='AccountPhysicalLocation', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100)),
      (
       'active', models.BooleanField(default=True)),
      (
       'account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djautotask.Account'))], options={'ordering': ('name', )})]