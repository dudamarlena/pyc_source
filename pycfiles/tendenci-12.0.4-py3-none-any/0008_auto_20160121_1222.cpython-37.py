# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/migrations/0008_auto_20160121_1222.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1259 bytes
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('helpdesk', '0007_max_length_by_integer')]
    operations = [
     migrations.AddField(model_name='ticket',
       name='creator',
       field=models.ForeignKey(related_name='helpdesk_ticket_creator', on_delete=(django.db.models.deletion.SET_NULL), default=None, editable=False, to=(settings.AUTH_USER_MODEL), null=True)),
     migrations.AddField(model_name='ticket',
       name='creator_username',
       field=models.CharField(default='', max_length=50)),
     migrations.AddField(model_name='ticket',
       name='owner',
       field=models.ForeignKey(related_name='helpdesk_ticket_owner', on_delete=(django.db.models.deletion.SET_NULL), default=None, to=(settings.AUTH_USER_MODEL), null=True)),
     migrations.AddField(model_name='ticket',
       name='owner_username',
       field=models.CharField(default='', max_length=50))]