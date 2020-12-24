# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/code/django-saltapi/django_saltapi/control.py
# Compiled at: 2013-03-11 13:56:03
from django.conf import settings
import salt.config, salt.client, saltapi

def wildcardtarget(fun):
    """
    Decorator to allow passing 'all' to the `tgt` argument, and it
    will translate into a '*' target which is then passed to Salt.
    """

    def _wildcardtarget(*args, **kwargs):
        if kwargs.get('tgt', '') == 'all':
            kwargs['tgt'] = '*'
        return fun(*args, **kwargs)

    return _wildcardtarget


def get_salt_client():
    client = salt.client.LocalClient(c_path=settings.SALT_CONFIG['master_config'])
    return client


def get_api_client():
    opts = salt.config.client_config(settings.SALT_CONFIG['master_config'])
    client = saltapi.APIClient(opts=opts)
    return client