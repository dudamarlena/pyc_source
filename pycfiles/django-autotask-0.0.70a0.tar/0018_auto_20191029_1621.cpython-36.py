# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0018_auto_20191029_1621.py
# Compiled at: 2019-10-31 11:47:41
# Size of source mod 2**32: 1697 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0017_auto_20191021_1028')]
    operations = [
     migrations.AlterField(model_name='ticket',
       name='category',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.TicketCategory')),
     migrations.AlterField(model_name='ticket',
       name='issue_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.IssueType')),
     migrations.AlterField(model_name='ticket',
       name='project',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Project')),
     migrations.AlterField(model_name='ticket',
       name='source',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.Source')),
     migrations.AlterField(model_name='ticket',
       name='sub_issue_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.SubIssueType')),
     migrations.AlterField(model_name='ticket',
       name='type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djautotask.TicketType'))]