# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_user_license_management_license_assignment.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseAssignment(Model):
    """Provides the information needed for a license update operation.

    :param excluded_plans: Gets or sets the service plan identifiers to be
     excluded from availability to the user.
    :type excluded_plans: list[str]
    :param sku_id: Gets or sets the product SKU identifier for the license.
    :type sku_id: str
    """
    _attribute_map = {'excluded_plans': {'key': 'excludedPlans', 'type': '[str]'}, 'sku_id': {'key': 'skuId', 'type': 'str'}}

    def __init__(self, excluded_plans=None, sku_id=None):
        super(MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseAssignment, self).__init__()
        self.excluded_plans = excluded_plans
        self.sku_id = sku_id