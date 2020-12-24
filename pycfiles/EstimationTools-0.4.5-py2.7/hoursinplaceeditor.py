# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/estimationtools/hoursinplaceeditor.py
# Compiled at: 2011-09-05 07:25:07
from estimationtools.utils import EstimationToolsBase
from pkg_resources import resource_filename
from trac.core import implements, Component
from trac.web.api import IRequestFilter, IRequestHandler
from trac.web.chrome import ITemplateProvider, add_script

class HoursInPlaceEditor(EstimationToolsBase):
    """A filter to implement in-place editing for estimated hours field in query page.
    
    Requires Trac XML-RPC Plug-in.
    """
    implements(IRequestFilter, IRequestHandler, ITemplateProvider)

    def match_request(self, req):
        return req.path_info == '/estimationtools/edithours.js'

    def process_request(self, req):
        data = {}
        data['field'] = self.estimation_field
        return ('edithours.html', {'data': data}, 'text/javascript')

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        try:
            realm = data['context'].resource.realm
        except:
            realm = None

        if realm in ('query', 'report', 'wiki', 'milestone') and 'preview' not in req.args and req.perm.has_permission('TICKET_MODIFY') and req.perm.has_permission('XML_RPC'):
            add_script(req, 'estimationtools/jquery.jeditable.mini.js')
            add_script(req, '/estimationtools/edithours.js')
        return (
         template, data, content_type)

    def get_htdocs_dirs(self):
        return [
         (
          'estimationtools', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return [
         resource_filename(__name__, 'templates')]