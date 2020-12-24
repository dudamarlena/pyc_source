# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_domain_management_signing_certificate_update_status.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1DomainManagementSigningCertificateUpdateStatus(Model):
    """Represents Signing Certificate Update Status.

    :param last_run_at: Last Run At
    :type last_run_at: datetime
    :param result: Result
    :type result: int
    """
    _attribute_map = {'last_run_at': {'key': 'lastRunAt', 'type': 'iso-8601'}, 'result': {'key': 'result', 'type': 'int'}}

    def __init__(self, last_run_at=None, result=None):
        super(MicrosoftPartnerSdkContractsV1DomainManagementSigningCertificateUpdateStatus, self).__init__()
        self.last_run_at = last_run_at
        self.result = result