# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_enrolled_program.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1EnrolledProgram(Model):
    """Represents an enrollment in a program.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param program_name: The program name. Possible values include: 'none',
     'reseller', 'advisor', 'partner_network', 'partner_network_local',
     'value_added_reseller', 'value_added_reseller_partner_network',
     'partner_incentives'
    :type program_name: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param program: The program name.
    :type program: str
    :param status: The program enrollment status. Possible values include:
     'none', 'not_registered', 'initialized', 'pending_qualification',
     'qualified', 'denied', 'active', 'disabled', 'suspended', 'evicted',
     'closed', 'expired', 'offboarding'
    :type status: str or ~microsoft.store.partnercenterservices.models.enum
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'program_name': {'key': 'programName', 'type': 'str'}, 'program': {'key': 'program', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, program_name=None, program=None, status=None):
        super(MicrosoftPartnerSdkContractsV1EnrolledProgram, self).__init__()
        self.program_name = program_name
        self.program = program
        self.status = status
        self.attributes = None
        return