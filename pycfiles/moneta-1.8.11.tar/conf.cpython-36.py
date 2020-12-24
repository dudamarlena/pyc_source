# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/conf.py
# Compiled at: 2017-10-30 08:18:03
# Size of source mod 2**32: 1628 bytes
import os
from djangofloor.log import log_configuration
from moneta.repository.signing import get_gpg
__author__ = 'Matthieu Gallet'

def moneta_log_configuration(settings_dict):
    config = log_configuration(settings_dict)
    config['loggers']['gnupg'] = {'handlers':[],  'level':'ERROR',  'propagate':True}
    return config


moneta_log_configuration.required_settings = log_configuration.required_settings

def auto_generate_signing_key(django_ready):
    if not django_ready:
        return
    else:
        from django.conf import settings
        gnupg_home = settings.GNUPG_HOME
        if not os.path.isdir(gnupg_home):
            os.makedirs(gnupg_home)
        os.chmod(gnupg_home, 448)
        for root, dirnames, filenames in os.walk(gnupg_home):
            os.chmod(root, 448)
            for filename in filenames:
                os.chmod(os.path.join(root, filename), 384)

        gpg = get_gpg()
        if len(gpg.list_keys(False)) == 0:
            input_data = gpg.gen_key_input(key_type='RSA', key_length=2048, name_real=('%s GNUPG key' % settings.SERVER_NAME),
              name_comment=('GPG key of the %s repository' % settings.SERVER_NAME),
              name_email=(settings.ADMIN_EMAIL),
              expire_date='10y')
            print('Generating a new private signing key (can take some time…)')
            gpg.gen_key(input_data)
            print('Private key generated.')
        key_id = None
        for key in gpg.list_keys(False):
            key_id = ('{keyid}'.format)(**key)

        return key_id or ''