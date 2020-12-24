# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/distributed/requests/migrate.py
# Compiled at: 2014-10-18 19:15:55
from pyage_forams.solutions.distributed.request import Request

class MigrateRequest(Request):

    def __init__(self, agent_address, cell_address, foram):
        super(MigrateRequest, self).__init__(agent_address)
        self.cell_address = cell_address
        self.foram = foram

    def execute(self, agent):
        agent.import_foram(self.cell_address, self.foram)

    def __repr__(self):
        return 'MigrateRequest[%s, %s, %s]' % (self.agent_address, self.cell_address, self.foram)