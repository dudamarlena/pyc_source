# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tracext/google/ads/web_ui.py
# Compiled at: 2008-11-26 17:55:59
from trac.core import Component, implements, TracError
from trac.web.api import ITemplateStreamFilter
from trac.web.chrome import add_ctxtnav, add_script, add_stylesheet
from trac.web import IRequestHandler
from trac.util.text import unicode_unquote
from genshi.builder import tag
from genshi.core import Markup
from genshi.filters.transform import Transformer, StreamBuffer

class GoogleAdsPanel(Component):
    env = log = config = None
    implements(ITemplateStreamFilter, IRequestHandler)

    def __init__(self):
        Component.__init__(self)
        try:
            import adspanel
            if self.env.is_component_enabled(adspanel.web_ui.AdsPanel):
                raise TracError('You need to disable/un-install the old AdsPanel plugin in order to work with the newone. (package rename)')
        except ImportError:
            pass

    def filter_stream(self, req, method, filename, stream, data):
        self.log.debug('Google Ads Stream Filter: %s', req.session)
        if req.path_info.startswith('/admin'):
            return stream
        else:
            if req.path_info.startswith('/ticket'):
                add_script(req, 'common/js/diff.js')
                add_stylesheet(req, 'common/css/diff.css')
            state = req.session.get('adspanel.state', 'shown')
            if state == 'hidden':
                state = 'show'
            elif state == 'shown':
                state = 'hide'
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            cursor.execute('SELECT value FROM system WHERE name=%s', ('google.ads_html', ))
            code = cursor.fetchone()
            if code:
                code = unicode_unquote(code[0])
            else:
                return stream
            add_ctxtnav(req, tag.a('%s Ads' % state.capitalize(), href=req.href.adspanel(state), class_='toggle_ads'))
            if self.dont_show_ads(req):
                self.log.debug('Not displaying ads, returning stream')
                return stream
            jscode = "jQuery(document).ready(function() {\n    jQuery('a.toggle_ads').show();\n    jQuery('a.toggle_ads').attr('href', 'javascript:;');\n    jQuery('a.toggle_ads').bind('click', function() {\n        var state = jQuery('#%(show_hide_id)s').is(':hidden') ? 'show' : 'hide';\n        var name = jQuery('#%(show_hide_id)s').is(':hidden') ? 'Hide Ads' : 'Show Ads';\n        jQuery(this).html(name);\n        jQuery('#%(show_hide_id)s').animate({opacity: state}, 200);\n        jQuery.get('%(href)s/'+state);\n    });\n});"
            ads_div_id = self.config.get('google.ads', 'ads_div_id', 'main')
            if ads_div_id == 'main':
                streambuffer = StreamBuffer()
                return stream | Transformer('//div[@id="main"]/* | //div[@id="main"]/text()').cut(streambuffer, accumulate=True).buffer().end().select('//div[@id="main"]').prepend(tag.table(tag.tr(tag.td(streambuffer, width='100%', style='vertical-align: top;') + tag.td(Markup(code), id='ads_panel', style='vertical-align: top;')), width='100%') + tag.script(jscode % dict(href=req.href.adspanel(), show_hide_id='ads_panel'), type='text/javascript')).end()
            return stream | Transformer('//div[@id="%s"]/* | //div[@id="%s"]/text()' % (
             ads_div_id, ads_div_id)).replace(tag(Markup(code), tag.script(jscode % dict(href=req.href.adspanel(), show_hide_id=ads_div_id), type='text/javascript')))

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
        if req.session.get('adspanel.state') == 'shown':
            return False
        if req.authname and req.authname != 'anonymous':
            if self.config.getbool('google.ads', 'hide_for_authenticated', False):
                return True
        return False