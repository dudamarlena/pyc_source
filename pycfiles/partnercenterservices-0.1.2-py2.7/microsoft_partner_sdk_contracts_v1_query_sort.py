# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_query_sort.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1QuerySort(Model):
    """Specifies sort field and direction.

    :param sort_field: Gets or sets the sort field.
    :type sort_field: str
    :param sort_direction: Gets or sets the sort direction. Possible values
     include: 'ascending', 'descending'
    :type sort_direction: str or
     ~microsoft.store.partnercenterservices.models.enum
    """
    _attribute_map = {'sort_field': {'key': 'sortField', 'type': 'str'}, 'sort_direction': {'key': 'sortDirection', 'type': 'str'}}

    def __init__(self, sort_field=None, sort_direction=None):
        super(MicrosoftPartnerSdkContractsV1QuerySort, self).__init__()
        self.sort_field = sort_field
        self.sort_direction = sort_direction