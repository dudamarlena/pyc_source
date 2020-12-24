# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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