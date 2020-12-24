# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0006_add_billin_address_and_migrate_data.py
# Compiled at: 2016-08-23 16:52:12
# Size of source mod 2**32: 877 bytes
from __future__ import unicode_literals
from django.db import migrations, models

def add_billing_address(apps, schema_editor):
    """ Data migration add billing_address in Bill from user billing_address 
    field
    """
    Bill = apps.get_model('billjobs', 'Bill')
    for bill in Bill.objects.all():
        bill.billing_address = bill.user.userprofile.billing_address
        bill.save()


class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0002_service_is_available_squashed_0005_bill_issuer_address_default')]
    operations = [
     migrations.AddField(model_name='bill', name='billing_address', field=models.CharField(max_length=1024, blank=True)),
     migrations.RunPython(add_billing_address)]