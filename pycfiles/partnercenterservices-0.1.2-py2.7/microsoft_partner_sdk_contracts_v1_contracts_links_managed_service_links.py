# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_links_managed_service_links.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsLinksManagedServiceLinks(Model):
    """Contains the links that allow the partner with delegated admin permissions
    to provide support for the service.

    :param admin_service: Gets or sets the admin service URI.
    :type admin_service:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param service_health: Gets or sets the service health URI.
    :type service_health:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param service_ticket: Gets or sets the service ticket URI.
    :type service_ticket:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param self: The self uri.
    :type self:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param next: The next page of items.
    :type next:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param previous: The previous page of items.
    :type previous:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    """
    _attribute_map = {'admin_service': {'key': 'adminService', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'service_health': {'key': 'serviceHealth', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'service_ticket': {'key': 'serviceTicket', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'itself': {'key': 'self', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'next': {'key': 'next', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'previous': {'key': 'previous', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}}

    def __init__(self, admin_service=None, service_health=None, service_ticket=None, itself=None, next=None, previous=None):
        super(MicrosoftPartnerSdkContractsV1ContractsLinksManagedServiceLinks, self).__init__()
        self.admin_service = admin_service
        self.service_health = service_health
        self.service_ticket = service_ticket
        self.itself = itself
        self.next = next
        self.previous = previous