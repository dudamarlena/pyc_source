# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/migrations/0005_queues_no_null.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1167 bytes
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('helpdesk', '0004_add_per_queue_staff_membership')]
    operations = [
     migrations.AlterField(model_name='escalationexclusion',
       name='queues',
       field=models.ManyToManyField(help_text='Leave blank for this exclusion to be applied to all queues, or select those queues you wish to exclude with this entry.', to='helpdesk.Queue', blank=True)),
     migrations.AlterField(model_name='ignoreemail',
       name='queues',
       field=models.ManyToManyField(help_text='Leave blank for this e-mail to be ignored on all queues, or select those queues you wish to ignore this e-mail for.', to='helpdesk.Queue', blank=True)),
     migrations.AlterField(model_name='presetreply',
       name='queues',
       field=models.ManyToManyField(help_text='Leave blank to allow this reply to be used for all queues, or select those queues you wish to limit this reply to.', to='helpdesk.Queue', blank=True))]