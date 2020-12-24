# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_flight_insider_program.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1FlightInsiderProgram(Model):
    """Flight details.

    :param id: The flight name
    :type id: str
    :param name: The flight display name
    :type name: str
    :param enrollment_status: Enrollment status of the partner in the flight
    :type enrollment_status: bool
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'enrollment_status': {'key': 'enrollmentStatus', 'type': 'bool'}}

    def __init__(self, id=None, name=None, enrollment_status=None):
        super(MicrosoftPartnerSdkContractsV1FlightInsiderProgram, self).__init__()
        self.id = id
        self.name = name
        self.enrollment_status = enrollment_status