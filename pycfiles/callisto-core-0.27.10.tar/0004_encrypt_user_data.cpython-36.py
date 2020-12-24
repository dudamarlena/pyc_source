# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/accounts/migrations/0004_encrypt_user_data.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 1490 bytes
import logging
from hashlib import sha256
import bcrypt
from django.db import migrations, models
from callisto_core.accounts.auth import index
logger = logging.getLogger(__name__)

def encrypt_user_data(apps, schema_editor):
    Account = apps.get_model('accounts.Account')
    for account in Account.objects.all():
        username = account.user.username
        userhash = sha256(username.lower().encode('utf-8')).hexdigest()
        usercrypt = bcrypt.hashpw(userhash.encode('utf-8'), bcrypt.gensalt())
        userindex = index(userhash)
        account.encrypted_username = usercrypt.decode()
        account.username_index = userindex
        email = account.user.email
        if email:
            emailhash = sha256(email.lower().encode('utf-8')).hexdigest()
            emailcrypt = bcrypt.hashpw(emailhash.encode('utf-8'), bcrypt.gensalt())
            emailindex = index(emailhash)
            account.encrypted_email = emailcrypt.decode()
            account.email_index = emailindex
        account.save()


class Migration(migrations.Migration):
    dependencies = [
     ('accounts', '0003_auto_20190607_1540')]
    operations = [
     migrations.RunPython(encrypt_user_data, reverse_code=(migrations.RunPython.noop))]