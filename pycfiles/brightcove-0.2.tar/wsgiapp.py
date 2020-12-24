# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/brightcontent/wsgiapp.py
# Compiled at: 2006-08-06 14:59:53
__doc__ = '\nThis module defines the WSGI entry point for this application.\n'
from paste.urlmap import URLMap
from paste.urlparser import make_static
from beaker.cache import CacheMiddleware

def make_app(global_conf, store='core', app='core', renderer='core', **kw):
    brightcontent = __import__('brightcontent.%s.store' % store)
    store = getattr(getattr(brightcontent, store), 'store')
    store = store.flatfile_repository(kw['store_config'])
    brightcontent = __import__('brightcontent.%s.app' % app)
    app = getattr(getattr(brightcontent, app), 'app')
    brightcontent = __import__('brightcontent.%s.renderer' % renderer)
    renderer = getattr(getattr(brightcontent, renderer), 'renderer')
    app = renderer.FeedRenderer(app.WSGIApplication(store))
    app = CacheMiddleware(app, global_conf)
    static = make_static(global_conf, 'brightcontent/static')
    urlmap = URLMap()
    urlmap['/'] = app
    urlmap['/static'] = static
    return urlmap