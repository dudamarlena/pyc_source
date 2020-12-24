# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/system_security_secure_string.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class SystemSecuritySecureString(Model):
    """SystemSecuritySecureString.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar length:
    :vartype length: int
    """
    _validation = {'length': {'readonly': True}}
    _attribute_map = {'length': {'key': 'length', 'type': 'int'}}

    def __init__(self):
        super(SystemSecuritySecureString, self).__init__()
        self.length = None
        return