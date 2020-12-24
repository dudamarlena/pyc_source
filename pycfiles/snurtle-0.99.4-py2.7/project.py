# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/bundles/project.py
# Compiled at: 2012-08-03 08:35:35
from snurtle.cmd2 import options, make_option
from clibundle import CLIBundle
PROJECT_TEMPLATE = '\n  objectId#${report[\'objectid\']} version: ${report[\'version\']} status: ${report[\'status\']} \n    placeHolder: ${report[\'placeholder\']} ownerId: ${report[\'ownerobjectid\']}\n    =================================================================\n    name:           "${report[\'name\']}" \n    number:         "${report[\'number\']}" \n    parentObjectId: "${report[\'parentobjectid\']}"\n    folderObjectId  "${report[\'folderobjectid\']}"\n    startDate:      "${report[\'startdate\']}"\n    --enterprises--\n    %if len(report[\'_enterprises\']) == 0:\n      No enterprises are assigned to project.\n    %else:\n      %for assignment in report[\'_enterprises\']:\n      ${assignment[\'targetobjectid\']}\n      %endfor\n    %endif\n    --projects--\n    %if len(report[\'_contacts\']) == 0:\n      No contacts are assigned to project..\n    %else:\n      %for assignment in report[\'_contacts\']:\n      ${assignment[\'targetobjectid\']}\n      %endfor\n    %endif    \n'

class ProjectCLIBundle(CLIBundle):

    @options([make_option('--favorite', action='store_true', help='List favorite projects.'),
     make_option('--name', type='string', help='List favorite projects.')])
    def do_list_projects(self, arg, opts=None):
        if opts.favorite:
            callid = self.server.get_favorites(entity_name='Project', detail_level=0, callback=self.callback)
        elif opts.name:
            callid = self.server.search_for_objects(entity='Project', criteria={'conjunction': 'AND', 'name': opts.name}, detail=0, callback=self.callback)
        else:
            callid = self.server.search_for_objects(entity='Project', criteria='list', detail=16, callback=self.callback)
        response = self.get_response(callid)
        if response:
            self.set_result(response)

    @options([
     make_option('--projectid', type='int', help='objectId [Project] to reparent.'),
     make_option('--parentid', type='int', help='objectId [Project] of new parent, or zero to remove parent.')])
    def do_reparent_project(self, arg, opts=None):
        response = self._get_entity(opts.projectid, expected_type='Project')
        if response:
            project = response.payload
            if opts.parentid:
                parent = self._get_entity(opts.parentid, expected_type='Project')
                if parent:
                    parentid = parent.payload['objectid']
                else:
                    return
            else:
                parentid = None
            project['parentprojectid'] = parentid
            callid = self.server.put_object(payload=project, callback=self.callback)
            response = self.get_response(callid)
            if response:
                self.set_result(response)
            else:
                self.set_result('Specified parent is not a project.')
        return

    @options([make_option('--parentid', type='int', help='List favorite projects.'),
     make_option('--name', type='string', help='List favorite projects.'),
     make_option('--number', type='string', help=''),
     make_option('--kind', type='string', help=''),
     make_option('--url', type='string', help=''),
     make_option('--isfake', action='store_true', help='')])
    def do_create_project(self, arg, opts=None):
        values = {}
        if not opts.name:
            self.set_result('Project name must be specified', error=True)
        values = {'name': opts.name, 'objectid': 0, 'entityname': 'Project'}
        if opts.number:
            values['number'] = opts.number
        if opts.kind:
            values['kind'] = opts.kind
        if opts.parentid:
            values['parentobjectid'] = opts.parentid
        if opts.url:
            values['url'] = opts.url
        if opts.isfake:
            values['placeholder'] = 1
        callid = self.server.put_object(values, callback=self.callback)
        response = self.get_response(callid)
        if response:
            self.set_result(response)

    @options([make_option('--objectid', type='int', help='objectId [Project] to display.')])
    def do_get_project(self, arg, opts=None):
        response = self._get_entity(opts.objectid, expected_type='Project', detail_level=65535)
        if response:
            self.set_result(response, template=PROJECT_TEMPLATE)