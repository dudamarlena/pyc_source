# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/migrations/0004_add_per_queue_staff_membership.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1009 bytes
from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('helpdesk', '0003_initial_data_import')]
    operations = [
     migrations.CreateModel(name='QueueMembership',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'queues', models.ManyToManyField(to='helpdesk.Queue', verbose_name='Authorized Queues')),
      (
       'user', models.OneToOneField(verbose_name='User', on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))],
       options={'verbose_name':'Queue Membership', 
      'verbose_name_plural':'Queue Memberships'},
       bases=(
      models.Model,))]