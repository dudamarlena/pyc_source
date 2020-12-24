# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/bundles/team.py
# Compiled at: 2012-08-06 20:13:18
from snurtle.cmd2 import options, make_option
from clibundle import CLIBundle
LIST_TEAM_TEMPLATE = "<%objectid='{:<12}'.format(report['objectid'])\nname='{:<45}'.format(report['name'])\nif report['objectid'] == 10003:\n    count='{:^8}'.format('-')\nelse:\n    count='{:^8}'.format(len(report['memberObjectIds']))%>${objectid} ${name} ${count}"
TEAM_TEMPLATE = '    OGo#${report[\'objectid\']} "${report[\'name\']}"\n    ================================================================= \n    Version: ${report[\'objectversion\']}\n    OwnerId: ${report[\'ownerobjectid\']}'

class TeamCLIBundle(CLIBundle):

    def do_list_teams(self, arg, opts=None):
        callid = self.server.search_for_objects(entity='Team', criteria='all', detail=128, callback=self.callback)
        response = self.get_response(callid)
        if response:
            self.set_result(response.payload, template=LIST_TEAM_TEMPLATE)

    @options([make_option('--objectid', type='int', help='objectId [Contact] to display.')])
    def do_get_team(self, arg, opts=None):
        response = self._get_entity(opts.objectid, expected_type='Team', detail_level=65535)
        if response:
            self.set_result(response, template=TEAM_TEMPLATE)