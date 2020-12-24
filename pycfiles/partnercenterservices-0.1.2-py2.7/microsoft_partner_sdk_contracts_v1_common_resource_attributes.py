# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_common_resource_attributes.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1CommonResourceAttributes(Model):
    """Refers to the common object attributes.

    :param etag: Gets or sets the etag.
     The object version in providers.
    :type etag: str
    :param object_type: The type of object.
    :type object_type: str
    """
    _attribute_map = {'etag': {'key': 'etag', 'type': 'str'}, 'object_type': {'key': 'objectType', 'type': 'str'}}

    def __init__(self, etag=None, object_type=None):
        super(MicrosoftPartnerSdkContractsV1CommonResourceAttributes, self).__init__()
        self.etag = etag
        self.object_type = object_type