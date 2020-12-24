# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/condfields/web_ui.py
# Compiled at: 2009-02-18 03:01:48
from trac.core import *
from trac.config import ListOption, BoolOption
from trac.web.api import IRequestFilter, IRequestHandler
from trac.web.chrome import ITemplateProvider, add_script
from trac.ticket.model import Type
from trac.ticket.api import TicketSystem
from trac.util.compat import sorted, set
import urllib
from pkg_resources import resource_filename

class CondFieldsModule(Component):
    """A filter to implement conditional fields on the ticket page."""
    __module__ = __name__
    implements(IRequestHandler, IRequestFilter, ITemplateProvider)
    include_std = BoolOption('condfields', 'include_standard', default='true', doc='Include the standard fields for all types.')
    forced_fields = set(['type', 'summary', 'reporter', 'description', 'status', 'resolution', 'priority'])

    def __init__(self):
        self.types = [ t.name for t in Type.select(self.env) ]
        for t in self.types:
            setattr(self.__class__, '%s_fields' % t, ListOption('condfields', t, doc='Fields to include for type "%s"' % t))

    def match_request(self, req):
        return req.path_info.startswith('/condfields')

    def process_request(self, req):
        data = {}
        data['types'] = {}
        mode = req.path_info[12:-3]
        if mode != 'new' and mode != 'view':
            raise TracError('Invalid condfields view')
        all_fields = []
        standard_fields = set()
        for f in TicketSystem(self.env).get_ticket_fields():
            all_fields.append(f['name'])
            if not f.get('custom'):
                standard_fields.add(f['name'])

        if 'owner' in all_fields:
            curr_idx = all_fields.index('owner')
            if 'cc' in all_fields:
                insert_idx = all_fields.index('cc')
            else:
                insert_idx = len(all_fields)
            if curr_idx < insert_idx:
                all_fields.insert(insert_idx, all_fields[curr_idx])
                del all_fields[curr_idx]
        for t in self.types:
            fields = set(getattr(self, t + '_fields'))
            if self.include_std:
                fields.update(standard_fields)
            fields.update(self.forced_fields)
            data['types'][t] = dict([ (f, f in fields) for f in all_fields ])

        self.log.debug(all_fields)
        self.log.info(standard_fields)
        data['mode'] = mode
        data['all_fields'] = list(all_fields)
        data['ok_view_fields'] = sorted(set(all_fields) - self.forced_fields, key=lambda x: all_fields.index(x))
        data['ok_new_fields'] = sorted(set(all_fields) - set(['summary', 'reporter', 'description', 'owner', 'type', 'status', 'resolution']), key=lambda x: all_fields.index(x))
        return (
         'condfields.js', {'condfields': data}, 'text/javascript')

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if req.path_info.startswith('/newticket') or req.path_info.startswith('/ticket/'):
            add_script(req, '/condfields/%s.js' % (req.path_info.startswith('/newticket') and 'new' or 'view'))
        return (
         template, data, content_type)

    def get_htdocs_dirs(self):
        return ()

    def get_templates_dirs(self):
        return ()