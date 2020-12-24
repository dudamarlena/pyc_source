# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_query_filters_field_filter.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1QueryFiltersFieldFilter(Model):
    """Represents a filter that can be applied to a search results field.

    :param operator: Gets or sets the filter operator. Possible values
     include: 'equals', 'not_equals', 'greater_than', 'greater_than_or_equals',
     'less_than', 'less_than_or_equals', 'substring', 'and', 'or',
     'starts_with', 'not_starts_with'
    :type operator: str or ~microsoft.store.partnercenterservices.models.enum
    """
    _attribute_map = {'operator': {'key': 'operator', 'type': 'str'}}

    def __init__(self, operator=None):
        super(MicrosoftPartnerSdkContractsV1QueryFiltersFieldFilter, self).__init__()
        self.operator = operator