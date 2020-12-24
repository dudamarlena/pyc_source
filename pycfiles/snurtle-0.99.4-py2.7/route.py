# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/bundles/route.py
# Compiled at: 2012-08-24 10:58:54
from snurtle.cmd2 import options, make_option
from clibundle import CLIBundle
ROUTE_LIST_TEMPLATE = "<%\n    group = report['name']\n    \n    flags = ''\n    for prop in report['_PROPERTIES']:\n        if prop['propertyname'] == '{http://www.opengroupware.us/oie}preserveAfterCompletion':\n            if prop['value'].upper() == 'YES':\n                flags += 'p'\n        elif prop['propertyname'] == '{http://www.opengroupware.us/oie}singleton':\n            if prop['value'].upper() == 'YES':\n                flags += 's'\n        elif prop['propertyname'] == '{http://www.opengroupware.us/oie}routeGroup':\n            group = prop['value']\n    \n    flags = '{:^6}'.format( flags )\n    name = '{:<30}'.format(report['name'])\n    group = '{:<30}'.format(group)\n    objectid = '{:<10}'.format(report['objectid'])\n\n%>${objectid} ${name} ${group} ${flags}"
ROUTE_TEMPLATE = '<%%>objectId#${report[\'objectid\']} version: ${report[\'version\']}\n=================================================================\n  Name:      "${report[\'name\']}"\n     \n__Properties__\n%for prop in report[\'_properties\']:\n  ${prop[\'propertyName\']} = ${prop[\'value\']}\n%endfor\n\n'

class RouteCLIBundle(CLIBundle):

    def do_list_routes(self, arg, opts=None):
        """List available OIE routes"""
        if self.server_ok():
            callid = self.server.search_for_objects(entity='Route', criteria='list', detail=16, callback=self.callback)
            response = self.get_response(callid)
            if response:
                self.set_result(response, template=ROUTE_LIST_TEMPLATE)

    @options([make_option('--objectid', type='int', help='ObjectId of Route to display.')])
    def do_get_route(self, arg, opts=None):
        """Retrieve route entity from the server."""
        response = self._get_entity(opts.objectid, detail_level=16, expected_type='Route')
        if response:
            self.set_result(response, template=ROUTE_TEMPLATE)