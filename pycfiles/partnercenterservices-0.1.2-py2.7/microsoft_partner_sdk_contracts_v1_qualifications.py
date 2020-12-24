# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_qualifications.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1Qualifications(Model):
    """Reseller Qualification.

    :param reselling: TODO : Remove this property when code is migrated to use
     CustomerQualifications
     Gets or sets Reselling such as Education, Nonprofit etc
    :type reselling: list[str]
    :param customer_qualifications: Gets or sets Reseller - Customer
     Qualifications
    :type customer_qualifications: list[str]
    :param special_pricing: Gets or sets Special Pricing such as Syndication,
     Syndication GoDaddy etc.
    :type special_pricing: list[str]
    """
    _attribute_map = {'reselling': {'key': 'reselling', 'type': '[str]'}, 'customer_qualifications': {'key': 'customerQualifications', 'type': '[str]'}, 'special_pricing': {'key': 'specialPricing', 'type': '[str]'}}

    def __init__(self, reselling=None, customer_qualifications=None, special_pricing=None):
        super(MicrosoftPartnerSdkContractsV1Qualifications, self).__init__()
        self.reselling = reselling
        self.customer_qualifications = customer_qualifications
        self.special_pricing = special_pricing