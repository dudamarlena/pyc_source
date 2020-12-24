# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/migrations/0008_auto_20180315_0857.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 3211 bytes
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     ('memberships', '0007_membershipdefault_auto_renew')]
    operations = [
     migrations.AlterField(model_name='membershipdefault',
       name='action_taken_user',
       field=models.ForeignKey(related_name='action_taken_set', on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='application_abandoned_user',
       field=models.ForeignKey(related_name='application_abandond_set', on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='application_approved_denied_user',
       field=models.ForeignKey(related_name='application_approved_denied_set', on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='application_approved_user',
       field=models.ForeignKey(related_name='application_approved_set', on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='application_complete_user',
       field=models.ForeignKey(related_name='application_complete_set', on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='directory',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), blank=True, to='directories.Directory', null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='industry',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), blank=True, to='industries.Industry', null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='payment_method',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), to='payments.PaymentMethod', null=True)),
     migrations.AlterField(model_name='membershipdefault',
       name='region',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), blank=True, to='regions.Region', null=True)),
     migrations.AlterField(model_name='notice',
       name='notice_type',
       field=models.CharField(max_length=20, verbose_name='For Notice Type', choices=[('join', 'Join Date'), ('renewal', 'Renewal Date'), ('expiration', 'Expiration Date'), ('approve', 'Join Approval Date'), ('disapprove', 'Join Disapproval Date'), ('approve_renewal', 'Renewal Approval Date'), ('disapprove_renewal', 'Renewal Disapproval Date')]))]