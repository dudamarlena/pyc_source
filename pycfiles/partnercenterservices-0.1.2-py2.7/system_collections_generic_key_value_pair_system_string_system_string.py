# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/system_collections_generic_key_value_pair_system_string_system_string.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class SystemCollectionsGenericKeyValuePairSystemStringSystemString(Model):
    """SystemCollectionsGenericKeyValuePairSystemStringSystemString.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar key:
    :vartype key: str
    :ivar value:
    :vartype value: str
    """
    _validation = {'key': {'readonly': True}, 'value': {'readonly': True}}
    _attribute_map = {'key': {'key': 'key', 'type': 'str'}, 'value': {'key': 'value', 'type': 'str'}}

    def __init__(self):
        super(SystemCollectionsGenericKeyValuePairSystemStringSystemString, self).__init__()
        self.key = None
        self.value = None
        return