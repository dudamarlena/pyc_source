# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_user_license_management_product_sku.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1UserLicenseManagementProductSku(Model):
    """Describes product details.

    :param id: Gets or sets the product identifier.
    :type id: str
    :param name: Gets or sets a localized display name for the product SKU.
     The user principal identifier.
    :type name: str
    :param sku_part_number: Gets or sets a SKU part number name for the
     product.
     For example, for Office 365 Plan E3, this value is "EnterprisePack".
     This can be used in place of the ID if the ID is not available.
    :type sku_part_number: str
    :param target_type: Gets or sets the target type of a product.
     This property identifies whether the product is applicable to a "User" or
     a "Tenant".
     For example, to determine all products that are applicable to user, filter
     where TargetType == "User".
    :type target_type: str
    :param license_group_id: Gets or sets a group identifier that indicates
     the authority or service that manages the productSku license.
     Products are separated into license groups for better manageability.
     "group1" - All products whose licenses can be managed by Azure Active
     Directory (AAD).
     "group2" - Minecraft product licenses. Possible values include: 'none',
     'group1', 'group2', 'group3'
    :type license_group_id: str or
     ~microsoft.store.partnercenterservices.models.enum
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'sku_part_number': {'key': 'skuPartNumber', 'type': 'str'}, 'target_type': {'key': 'targetType', 'type': 'str'}, 'license_group_id': {'key': 'licenseGroupId', 'type': 'str'}}

    def __init__(self, id=None, name=None, sku_part_number=None, target_type=None, license_group_id=None):
        super(MicrosoftPartnerSdkContractsV1UserLicenseManagementProductSku, self).__init__()
        self.id = id
        self.name = name
        self.sku_part_number = sku_part_number
        self.target_type = target_type
        self.license_group_id = license_group_id