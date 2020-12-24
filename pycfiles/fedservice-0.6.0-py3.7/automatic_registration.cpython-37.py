# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/op/add_on/automatic_registration.py
# Compiled at: 2020-01-23 05:31:42
# Size of source mod 2**32: 625 bytes
from oidcendpoint.oidc import registration

def add_automatic_registration_support(endpoint, **kwargs):
    """

    :param endpoint:
    :param kwargs:
    :return:
    """
    auth_endpoint = endpoint['authorization']
    auto_reg = (registration.Registration)((auth_endpoint.endpoint_context), **kwargs)
    auth_endpoint.automatic_registration_endpoint = auto_reg
    if auth_endpoint.client_authn_method:
        if 'private_key_jwt' not in auth_endpoint.client_authn_method:
            auth_endpoint.client_authn_method.append('private_key_jwt')
    else:
        auth_endpoint.client_authn_method = [
         'private_key_jwt']