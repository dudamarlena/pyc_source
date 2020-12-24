# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/kms/keyrings.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1356 bytes
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources
from ScoutSuite.providers.gcp.resources.kms.keys import Keys

class KeyRings(GCPCompositeResources):
    _children = [
     (
      Keys, 'keys')]

    def __init__(self, facade, project_id):
        super(KeyRings, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_keyrings = await self.facade.kms.list_key_rings(self.project_id)
        for location in raw_keyrings.keys():
            for raw_keyring in raw_keyrings.get(location, []):
                keyring_id, keyring = self._parse_keyring(raw_keyring, location)
                self[keyring_id] = keyring

        await self._fetch_children_of_all_resources(resources=self,
          scopes={keyring_id:{'project_id':self.project_id,  'keyring_name':keyring['name'],  'location':keyring['location']} for keyring_id, keyring in self.items()})

    def _parse_keyring(self, raw_keyring, location):
        keyring_dict = {}
        keyring_dict['id'] = raw_keyring.name
        keyring_dict['name'] = raw_keyring.name.split('/')[(-1)]
        keyring_dict['location'] = location
        return (keyring_dict['id'], keyring_dict)