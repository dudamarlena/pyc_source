# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\freedomsponsors\freedomsponsors_trac.py
# Compiled at: 2013-08-09 09:30:02
from genshi.builder import tag
from trac.core import Component, implements
from trac.web.api import IRequestFilter
from trac.web.chrome import add_ctxtnav

class FreedomSponsorsPlugin(Component):
    implements(IRequestFilter)

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        ticket_id = req.args.get('id')
        if template == 'ticket.html' and ticket_id:
            ticket_url = req.abs_href('ticket', ticket_id)
            fs_url = 'http://www.freedomsponsors.org/core/issue/sponsor?trackerURL=%s' % ticket_url
            text = 'Sponsor #%s in FreedomSponsors.org!' % ticket_id
            add_ctxtnav(req, tag.a(text, href=fs_url, target='_blank'))
        return (
         template, data, content_type)