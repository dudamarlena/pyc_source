# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/keyring_helper.py
# Compiled at: 2015-08-31 08:17:33


class KeyringHelper(object):

    def __init__(self, keyserver_helper, homedir, keyrings, secret_keyrings, primary_keyring, default_key, auto_key_locate, simple_sk_checksum, no_sig_cache, no_sig_create_check, lock_count, no_mdc_warning, try_all_secrets, no_default_keyring, preserve_permissions):
        self.check_permissions()

    def check_permissions(self):
        """Check permissions of keyring files."""
        for keyring in self.keyrings:
            mode = 511
            self.io_helper.permissions_warning(keyring, mode, 448)

    def get_secret_key(self):
        pass

    def find_recipient(self, recipient_string):
        return