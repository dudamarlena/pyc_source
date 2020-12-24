# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_marketplace_services_core_service_fault.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftMarketplaceServicesCoreServiceFault(Model):
    """MicrosoftMarketplaceServicesCoreServiceFault.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param code:
    :type code: int
    :param description:
    :type description: str
    :ivar data:
    :vartype data: list[str]
    :param source:
    :type source: str
    """
    _validation = {'data': {'readonly': True}}
    _attribute_map = {'code': {'key': 'code', 'type': 'int'}, 'description': {'key': 'description', 'type': 'str'}, 'data': {'key': 'data', 'type': '[str]'}, 'source': {'key': 'source', 'type': 'str'}}

    def __init__(self, code=None, description=None, source=None):
        super(MicrosoftMarketplaceServicesCoreServiceFault, self).__init__()
        self.code = code
        self.description = description
        self.data = None
        self.source = source
        return