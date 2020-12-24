# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0003_delete_qrcode.py
# Compiled at: 2018-05-02 03:55:02
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0004_auto_20180502_1555'),
     ('bee_django_crm', '0002_qrcode')]
    operations = [
     migrations.DeleteModel(name=b'QrCode')]