# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/iam/bindings.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 747 bytes
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.base.resources.base import Resources

class Bindings(Resources):

    def __init__(self, facade, project_id, service_account_email):
        super(Bindings, self).__init__(facade)
        self.project_id = project_id
        self.service_account_email = service_account_email

    async def fetch_all(self):
        raw_bindings = await self.facade.iam.get_bindings(self.project_id, self.service_account_email)
        for raw_binding in raw_bindings:
            binding_id, binding = self._parse_binding(raw_binding)
            self[binding_id] = binding

    def _parse_binding(self, raw_binding):
        return (len(self), raw_binding)