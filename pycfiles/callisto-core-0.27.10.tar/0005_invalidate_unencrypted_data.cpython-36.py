# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/accounts/migrations/0005_invalidate_unencrypted_data.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1097 bytes
import logging
from django.db import migrations, models
logger = logging.getLogger(__name__)
SUFFIX = ':unsafe'

def invalidate_unencrypted_data(apps, schema_editor):
    Account = apps.get_model('accounts.Account')
    for account in Account.objects.all():
        account.user.username = f"{account.user.username}{SUFFIX}"
        if account.user.email:
            account.user.email = f"{account.user.email}{SUFFIX}"
        account.user.save()


def revalidate_unencrypted_data(apps, schema_editor):
    Account = apps.get_model('accounts.Account')
    for account in Account.objects.all():
        account.user.username = account.user.username.rstrip(SUFFIX)
        if account.user.email:
            account.user.email = account.user.email.rstrip(SUFFIX)
        account.user.save()


class Migration(migrations.Migration):
    dependencies = [
     ('accounts', '0004_encrypt_user_data')]
    operations = [
     migrations.RunPython(invalidate_unencrypted_data,
       reverse_code=revalidate_unencrypted_data)]