# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/stackdriverlogging/sinks.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 782 bytes
from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade

class Sinks(Resources):

    def __init__(self, facade, project_id):
        super(Sinks, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_sinks = await self.facade.stackdriverlogging.get_sinks(self.project_id)
        for raw_sink in raw_sinks:
            sink_name, sink = self._parse_sink(raw_sink)
            self[sink_name] = sink

    def _parse_sink(self, raw_sink):
        sink_dict = {}
        sink_dict['name'] = raw_sink.name
        sink_dict['filter'] = raw_sink.filter_
        sink_dict['destination'] = raw_sink.destination
        return (sink_dict['name'], sink_dict)