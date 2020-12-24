# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/clustermgmt/rest.py
# Compiled at: 2012-04-30 10:51:15
import json
from five import grok
from infrae.rest import REST
from .interfaces import IHealthReporter

class NodeStatus(REST):
    """Returns the status of all nodes as a json dict.  Accessible via
       ++rest++nodestatus.  format: 
       {"nodeA": {"status": "online"}, "nodeB": {"status": "offline"}}
    """
    grok.context(IHealthReporter)
    grok.require('bethel.clustermgmt.rest')

    def GET(self):
        nodes = dict([ (n, {}) for n in self.context.nodes_in_cluster ])
        for n in nodes:
            status = 'online'
            if n in self.context.offline_nodes:
                status = 'offline'
            nodes[n]['status'] = status

        return self.json_response(nodes)


class SetStatus(REST):
    """Update the status of one or more nodes.  Accepts a json-encoded POST
       parameter named 'change', with the following format:
       {"nodeA": {"status": "online"}, "nodeB": ...}
       
       Due to infrae.REST's lack of support for accepting json, the json
       input is passed in via a parameter named "change"
    """
    grok.context(IHealthReporter)
    grok.require('bethel.clustermgmt.rest')

    def POST(self, *args, **kwargs):
        json_input = json.loads(self.request['change'])
        for (k, v) in json_input.items():
            self.context.set_node_status(k, v['status'])

        return self.json_response({'status': 'OK'})