# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_user_license_management_license.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1UserLicenseManagementLicense(Model):
    """Describes a user license.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param service_plans: Gets or sets the collection of service plans that
     correspond to the license. Service plans refer to services that a user is
     assigned to use.
     For example, Delve is a service plan which a user is either assigned to
     use or can be assigned to use.
    :type service_plans:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1UserLicenseManagementServicePlan]
    :param product_sku: Gets or sets the SKU of the product that corresponds
     to the license.
    :type product_sku:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1UserLicenseManagementProductSku
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'service_plans': {'key': 'servicePlans', 'type': '[MicrosoftPartnerSdkContractsV1UserLicenseManagementServicePlan]'}, 'product_sku': {'key': 'productSku', 'type': 'MicrosoftPartnerSdkContractsV1UserLicenseManagementProductSku'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, service_plans=None, product_sku=None):
        super(MicrosoftPartnerSdkContractsV1UserLicenseManagementLicense, self).__init__()
        self.service_plans = service_plans
        self.product_sku = product_sku
        self.attributes = None
        return