# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/adspanel/web_ui.py
# Compiled at: 2008-02-22 19:18:04
from trac.core import *
from trac.config import Option
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import add_ctxtnav
from trac.web import HTTPNotFound, IRequestHandler
from trac.util.text import unicode_unquote
from genshi.builder import tag
from genshi.core import Markup
from genshi.filters.transform import Transformer, StreamBuffer
from pkg_resources import resource_filename

class AdsPanel(Component):
    config = None
    implements(ITemplateStreamFilter, IRequestHandler)

    def filter_stream(self, req, method, filename, stream, data):
        self.log.debug(req.session)
        if req.path_info.startswith('/admin'):
            return stream
        state = req.session.get('adspanel.state', 'shown')
        if state == 'hidden':
            state = 'show'
        elif state == 'shown':
            state = 'hide'
        add_ctxtnav(req, tag.a('%s Ads' % state.capitalize(), href=req.href.adspanel(state), class_='toggle_ads'))
        if self.dont_show_ads(req):
            self.log.debug('Not displaying ads, returning stream')
            return stream
        jscode = "jQuery(document).ready(function() {\n    jQuery('a.toggle_ads').show();\n    jQuery('a.toggle_ads').attr('href', 'javascript:;');\n    jQuery('a.toggle_ads').bind('click', function() {\n        var state = jQuery('#ads_panel').is(':hidden') ? 'show' : 'hide';\n        var name = jQuery('#ads_panel').is(':hidden') ? 'Hide Ads' : 'Show Ads';\n        jQuery(this).html(name);\n        jQuery('#ads_panel').animate({opacity: state}, 200);\n        jQuery.get('%s/'+state);\n    });\n});" % req.href.adspanel()
        cursor = self.env.get_db_cnx().cursor()
        cursor.execute('SELECT value FROM system WHERE name=%s', ('adspanel.code', ))
        code = cursor.fetchone()
        if code:
            code = unicode_unquote(code[0])
        else:
            code = ''
        streambuffer = StreamBuffer()
        return stream | Transformer('//div[@id="main"]/* | //div[@id="main"]/text()').cut(streambuffer).end().select('//div[@id="main"]').prepend(tag.table(tag.tr(tag.td(streambuffer, width='100%', style='vertical-align: top;') + tag.td(Markup(code), id='ads_panel', style='vertical-align: top;')), width='100%') + tag.script(jscode, type='text/javascript'))

    def match_request(self, req):
        if req.path_info == '/adspanel/hide':
            req.args['adspanel.state'] = 'hidden'
            return True
        if req.path_info == '/adspanel/show':
            req.args['adspanel.state'] = 'shown'
            return True
        return False

    def process_request(self, req):
        req.session['adspanel.state'] = req.args.get('adspanel.state', 'hidden')
        req.session.save()
        if req.get_header('X-Requested-With') == 'XMLHttpRequest':
            req.send_response(code=200)
            req.end_headers()
        else:
            referer = req.get_header('Referer')
            if referer and not referer.startswith(req.base_url):
                referer = None
            req.redirect(referer or self.env.abs_href())
        return

    def dont_show_ads(self, req):
        if req.session.get('adspanel.state') == 'hidden':
            return True
        elif req.session.get('adspanel.state') == 'shown':
            return False
        elif req.authname and req.authname != 'anonymous':
            if self.config.getbool('adspanel', 'hide_for_authenticated', False):
                return True
        return False