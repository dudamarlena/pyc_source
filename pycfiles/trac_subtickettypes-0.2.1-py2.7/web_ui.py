# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subtickettypes/web_ui.py
# Compiled at: 2013-09-04 16:02:34
from pprint import pprint
from pkg_resources import resource_filename
from genshi import HTML
from genshi.builder import tag
from genshi.filters.transform import Transformer
from trac.core import *
from trac.ticket import model
from trac.util.text import unicode_quote_plus
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider
from trac.web.chrome import ITemplateStreamFilter
from trac.web.chrome import add_notice
from trac.web.chrome import add_script
from trac.ticket.roadmap import TicketGroupStats
from trac.util.translation import _

class SubTicketTypesModule(Component):
    """Implements subtickettypes in Trac's interface."""
    implements(IRequestFilter, ITemplateProvider, ITemplateStreamFilter)

    def pre_process_request(self, req, handler):
        if req.path_info.startswith('/admin/ticket/type/'):
            if req.method == 'POST' and req.args.get('cancel'):
                req.redirect(req.href.admin('ticket', 'type'))
            if req.method == 'POST' and 'rename_children' in req.args:
                if req.args.get('rename_children') != 'on':
                    return handler
                parent_ticket_type_name = req.path_info[19:]
                parent_ticket_type = model.Type(self.env, parent_ticket_type_name)
                parent_ticket_type.name = req.args.get('name')
                try:
                    parent_ticket_type.update()
                except self.env.db_exc.IntegrityError:
                    raise TracError(_('The ticket type "%(name)s" already exists.', name=parent_ticket_type_name))

                child_ticket_types = self._get_tickettype_children(parent_ticket_type_name)
                for ticket_type in child_ticket_types:
                    ticket_type.name = ticket_type.name.replace(parent_ticket_type_name, req.args.get('name'), 1)
                    ticket_type.update()

                add_notice(req, _('Your changes have been saved.'))
                req.redirect(req.href.admin('ticket', 'type'))
        return handler

    def post_process_request(self, req, template, data, content_type):
        if req.path_info.startswith('/ticket/') or req.path_info.startswith('/newticket'):
            add_script(req, 'subtickettypes/tickettypeselect.js')
        if template == 'query.html':
            begins_with_select_item = {'name': _('begins with'), 'value': ''}
            if begins_with_select_item not in data['modes']['select']:
                data['modes']['select'].insert(0, begins_with_select_item)
        if template == 'milestone_view.html':
            if data['grouped_by'] == 'type':
                ticket_type_name = ''
                new_groups = []
                new_ticket_types = []
                for ticket_type in data['groups']:
                    ticket_type_name = ticket_type['name'].split('/')[0]
                    if ticket_type_name not in new_ticket_types:
                        new_ticket_types.append(ticket_type_name)
                        new_hrefs = []
                        for interval_href in ticket_type['interval_hrefs']:
                            new_hrefs.append(interval_href.replace(unicode_quote_plus(ticket_type['name']), '^' + ticket_type_name))

                        ticket_type['stats_href'] = ticket_type['stats_href'].replace(unicode_quote_plus(ticket_type['name']), '^' + ticket_type_name)
                        ticket_type['interval_hrefs'] = new_hrefs
                        ticket_type['name'] = ticket_type_name
                        new_groups.append(ticket_type)
                    else:
                        core_ticket_type = new_groups[new_ticket_types.index(ticket_type_name)]
                        merged_stats = core_ticket_type['stats']
                        new_stats = ticket_type['stats']
                        merged_stats.count += new_stats.count
                        i = 0
                        for interval in merged_stats.intervals:
                            new_interval = new_stats.intervals[i]
                            interval['count'] += new_interval['count']
                            i += 1

                        merged_stats.refresh_calcs()

                data['groups'] = new_groups
        return (
         template, data, content_type)

    def get_htdocs_dirs(self):
        """Return the absolute path of a directory containing additional
        static resources (such as images, style sheets, etc).
        """
        return [
         (
          'subtickettypes', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        """Return the absolute path of the directory containing the provided
        ClearSilver templates.
        """
        return ''

    def filter_stream(self, req, method, filename, stream, data):
        if filename == 'admin_enums.html' and data['active_cat'] == 'ticket' and data['active_panel'] == 'type' and data['view'] == 'detail':
            if len(self._get_tickettype_children(data['enum'].name)) > 0:
                stream |= Transformer("//div[@class='field'][1]").after(self._build_renamechildren_field())
        elif req.path_info.startswith('/query'):
            html = HTML('<script type="text/javascript" charset="utf-8" src="' + req.href.base + '/chrome/subtickettypes/tickettypeselect.js"></script>')
            stream |= Transformer('//head').append(html)
        return stream

    def _get_tickettype_children(self, name):
        tickettypes = model.Type.select(self.env)
        result = []
        for tickettype in tickettypes:
            if tickettype.name.startswith(name + '/') and tickettype.name != name:
                result.append(tickettype)

        return result

    def _build_renamechildren_field(self):
        return tag.div(tag.label(tag.input(_('Also rename children'), type='checkbox', id='rename_children', name='rename_children', checked='checked')), class_='field')