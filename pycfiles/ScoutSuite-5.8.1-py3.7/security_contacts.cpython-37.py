# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/resources/securitycenter/security_contacts.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1296 bytes
from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources

class SecurityContacts(AzureResources):

    def __init__(self, facade, subscription_id):
        super(SecurityContacts, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_contact in await self.facade.securitycenter.get_security_contacts(self.subscription_id):
            id, security_contact = self._parse_security_contact(raw_contact)
            self[id] = security_contact

    def _parse_security_contact(self, security_contact):
        security_contact_dict = {}
        security_contact_dict['id'] = security_contact.id
        security_contact_dict['name'] = security_contact.name
        security_contact_dict['email'] = security_contact.email
        security_contact_dict['phone'] = security_contact.phone
        security_contact_dict['alert_notifications'] = security_contact.alert_notifications == 'On'
        security_contact_dict['alerts_to_admins'] = security_contact.alerts_to_admins == 'On'
        security_contact_dict['additional_properties'] = security_contact.additional_properties
        return (
         security_contact_dict['id'], security_contact_dict)