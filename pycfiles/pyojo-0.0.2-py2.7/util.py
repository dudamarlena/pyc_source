# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyojo\util.py
# Compiled at: 2013-06-05 12:21:45
""" Miscelaneus utilities. 

"""
import os, base
from .func import log
from .content import CachedText

class TestPage(object):

    def __init__(self):
        self.title = 'pyojo Test page'
        self.head = []
        self.meta('content-type', 'text/html; charset=utf-8')
        self.link('shortcut icon', 'image/x-icon', '/favicon.ico')
        self.link('StyleSheet', 'text/css', '/static/js/dojo/dijit/themes/claro/claro.css')
        self.link('StyleSheet', 'text/css', '/static/css/pyojo.css')
        self.body = []
        dojo_src = '/static/js/dojo/dojo/dojo.js'
        dojo_cfg = "async:true, packages:[{name: 'pyojo', location: '/pyojo'}]"
        self.head.append('<script src="%s" data-dojo-config="%s">\n</script>' % (
         dojo_src, dojo_cfg))
        self.code = []

    def meta(self, http, content):
        self.head.append('<meta http-equiv="%s" content="%s">' % (http,
         content))

    def link(self, rel, ctype, href):
        self.head.append('<link rel="%s" type="%s" href="%s">' % (rel,
         ctype,
         href))

    def script(self, loc):
        self.body.append('<script>%s</script>' % loc)

    def html(self):
        html = '<html><title>%s</title>' % self.title
        html += ('\n').join(self.head)
        html += '</head><body id="base" class="claro">'
        html += ('\n').join(self.body)
        html += '</body></html>'
        return html


def CacheStatic(folder):
    www = base.Config.www
    count = 0
    folder = 'static/' + folder
    folder = folder.replace('/', os.path.sep)
    log.info('Loading %s', folder)
    for root, _, files in os.walk(os.path.join(www, folder)):
        base = root.replace(www, '').replace(os.path.sep, '/')
        for filename in files:
            if os.path.splitext(filename)[1][1:] in ('js', 'css'):
                url = base + '/' + filename.replace(os.path.sep, '/')
                cache = CachedText(url, os.path.join(root, filename))
                count += 1

    try:
        total = cache.total_size() / 1024
    except:
        total = 0

    log.info('Cached %s files, total %s Kb', count, total)