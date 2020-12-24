# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/agents.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'agents'

    def basic(self, agents):
        if not agents.get('host', ''):
            agents['host'] = ''
            return agents
        return {'agents': {'id': agents.get('id', ''), 
                      'host': agents.get('host', ''), 
                      'primary_public_ip': agents.get('primary_public_ip', ''), 
                      'secondary_public_ip': agents.get('secondary_public_ip', ''), 
                      'cluster_ip': agents.get('cluster_ip', ''), 
                      'cluster_id': agents.get('cluster_id', ''), 
                      'data_drives_number': agents.get('data_drives_number', ''), 
                      'id_rsa_pub': agents.get('id_rsa_pub', ''), 
                      'raw_ip': agents.get('raw_ip', ''), 
                      'zone_id': agents.get('zone_id', ''), 
                      'type': agents.get('type', ''), 
                      'status': agents.get('status', ''), 
                      'service_id': agents.get('service_id', '')}}

    def index(self, agentss):
        """Show a list of agentss without many details."""
        return self._list_view(self.basic, agentss)

    def _list_view(self, func, agentss):
        """Provide a view for a list of agentss."""
        agents_list = [ func(agents)['agents'] for agents in agentss ]
        agentss_dict = dict(agentss=agents_list)
        return agentss_dict