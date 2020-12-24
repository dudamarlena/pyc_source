# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_user_license_management_license_update.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseUpdate(Model):
    """Provides information used to assign or remove licenses from a user.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param licenses_to_assign: Gets or sets the list of licenses to be
     assigned.
    :type licenses_to_assign:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseAssignment]
    :param licenses_to_remove: Gets or sets the list of product SKU
     identifiers of the licenses to remove.
    :type licenses_to_remove: list[str]
    :ivar license_warnings: Gets a list of warnings that occurred during
     license assignment. This is a read-only property.
    :vartype license_warnings:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseWarning]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'license_warnings': {'readonly': True}, 'attributes': {'readonly': True}}
    _attribute_map = {'licenses_to_assign': {'key': 'licensesToAssign', 'type': '[MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseAssignment]'}, 'licenses_to_remove': {'key': 'licensesToRemove', 'type': '[str]'}, 'license_warnings': {'key': 'licenseWarnings', 'type': '[MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseWarning]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, licenses_to_assign=None, licenses_to_remove=None):
        super(MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseUpdate, self).__init__()
        self.licenses_to_assign = licenses_to_assign
        self.licenses_to_remove = licenses_to_remove
        self.license_warnings = None
        self.attributes = None
        return