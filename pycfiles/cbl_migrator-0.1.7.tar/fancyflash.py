# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cblog/widgets/fancyflash.py
# Compiled at: 2006-12-15 15:47:35
__all__ = [
 'FancyFlash']
import pkg_resources
from turbogears.widgets import Widget, JSSource, JSLink, CSSLink, js_location, register_static_directory
from simplejson import loads
from cblog.widgets import jslibs
static_dir = pkg_resources.resource_filename('cblog', 'static')
register_static_directory('fancyflash', static_dir)
fancyflash_css = [
 CSSLink('fancyflash', 'css/fancyflash.css', media='screen')]
fancyflash_js = [jslibs.events, JSLink('fancyflash', 'javascript/fancyflash.js'),
 JSSource("document.write('<style>#statusmessage {position: absolute;}</style>');", js_location.head)]

def _escape(s, quote=False):
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    if quote:
        s = s.replace('"', '&quot;')
    return s


class FancyFlash(Widget):
    __module__ = __name__
    name = 'statusmessage'
    template = '\n<div xmlns:py="http://purl.org/kid/ns#" id="statusmessage">\n  <!--[if gte ie 5.5000]>\n  <link rel="stylesheet" type="text/css"\n    href="/tg_widgets/fancyflash/css/ie.css">\n  <![endif]-->\n  <div py:if="message" class="${status}" py:content="XML(message)"></div>\n  <script py:if="timeout" py:replace="script()" />\n</div>\n'
    params = [
     'message', 'status', 'timeout']
    message = ''
    status = 'info'
    timeout = 0
    css = fancyflash_css
    javascript = fancyflash_js

    def update_params(self, params):
        super(FancyFlash, self).update_params(params)
        params.update(self._parse_tg_flash(params.get('value')))

    def _parse_tg_flash(self, tg_flash):
        params = dict()
        if tg_flash:
            try:
                tg_flash = loads(tg_flash)
            except:
                tg_flash = dict(msg=tg_flash)
            else:
                if not (isinstance(tg_flash, dict) and tg_flash.has_key('msg')):
                    if isinstance(tg_flash, basestring):
                        tg_flash = dict(msg=tg_flash)
                    else:
                        tg_flash = dict(msg=str(tg_flash))

            msg = tg_flash.get('msg')
            if msg:
                if not tg_flash.get('allow_html', False):
                    msg = _escape(msg)
                params['message'] = msg
                params['status'] = tg_flash.get('status', 'info')
                try:
                    params['timeout'] = int(tg_flash.get('timeout', 0))
                except ValueError:
                    pass
                else:
                    if params['timeout'] > 0:
                        params['script'] = JSSource("setHideTimeout('%s', %s);" % (self.name, params['timeout']))
        return params