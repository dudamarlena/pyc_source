# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/webapp/webapp_base/webapp_template/src/webapp/startup.py
# Compiled at: 2012-02-18 12:08:22
__docformat__ = 'restructuredtext'
import zope.app.wsgi
try:
    import psyco
    psyco.profile()
except:
    pass

def application_factory(global_conf):
    zope_conf = global_conf['zope_conf']
    app = zope.app.wsgi.getWSGIApplication(zope_conf)

    def wrapper(environ, start_response):
        vhost = ''
        vhost_skin = environ.get('HTTP_X_VHM_SKIN')
        if vhost_skin and not environ.get('CONTENT_TYPE', '').startswith('application/json') and not environ.get('PATH_INFO', '').startswith('/++skin++'):
            vhost = '/++skin++' + vhost_skin
        url_scheme = environ.get('wsgi.url_scheme', 'http')
        vhost_root = environ.get('HTTP_X_VHM_ROOT', '')
        if url_scheme == 'https' or vhost_root and vhost_root != '/':
            vhost += '%s/++vh++%s:%s:%s/++' % (vhost_root,
             url_scheme,
             environ.get('SERVER_NAME', ''),
             environ.get('SERVER_PORT', '80'))
        environ['PATH_INFO'] = vhost + environ['PATH_INFO']
        return app(environ, start_response)

    return wrapper