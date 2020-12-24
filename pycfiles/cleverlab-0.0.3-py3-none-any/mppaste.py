# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/lib/mppaste.py
# Compiled at: 2006-08-02 05:57:51
from mod_python import apache
from paste.deploy import loadapp
from harold.lib.mpwsgi import WsgiAdapter
apps = {}

def handler(req):
    """ maps mod_python request to a paste application indicated by the config

    @param req mod_python request object
    @return always returns apache.OK; HTTP status set by adapter
    """
    options = req.get_options()
    configname = options['paste.config']
    interpname = options.get('PythonInterpreter', None)
    appskey = (configname, interpname)
    try:
        app = apps[appskey]
    except (KeyError,):
        appname = options.get('paste.app', None)
        relativeto = options.get('paste.relative_to', None)
        app = apps[appskey] = loadapp('config:%s' % configname, name=appname, relative_to=relativeto)

    WsgiAdapter(req).run(app)
    return apache.OK