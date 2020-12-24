# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/rp/authorization.py
# Compiled at: 2019-01-17 05:12:29
# Size of source mod 2**32: 143 bytes
from oidcservice.oidc.authorization import Authorization

class FedAuthorization(Authorization):
    default_authn_method = 'private_key_jwt'