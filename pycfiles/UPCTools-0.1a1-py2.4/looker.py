# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\upc_tools\looker.py
# Compiled at: 2006-12-11 10:18:00
import xmlrpclib, cherrypy
from turbogears import config, expose, controllers
xml_rpc_server = 'http://www.upcdatabase.com/rpc'
upc_server = None

class UPCAjaxController(controllers.Controller):
    __module__ = __name__

    @expose(template='upc_tools.templates.partial_upc')
    def index(self, code):
        try:
            upc = lookup(code)
        except:
            upc = ''

        if isinstance(upc, str):
            upc = dict(error='There was an error with the lookup')
        return dict(upc=upc)


def start_extension():
    global upc_server
    if not config.get('upc_tools.on', False):
        return
    upc_server = xmlrpclib.ServerProxy(xml_rpc_server)
    if hasattr(cherrypy.root, 'upc_tools'):
        raise 'The path /upc_tools is already taken'
    cherrypy.root.upc_tools = UPCAjaxController()


def stop_extension():
    global upc_server
    if not config.get('upc_tools.on', False):
        return
    if upc_server is None:
        return
    delattr(cherrypy.root, 'upc_tools')
    upc_server = None
    return


def lookup(code):
    if not config.get('upc_tools.on', False):
        raise 'UPC-Tools is not enabled, add upc_tools.on = True to your config file.'
    if len(code) == 12:
        code = '0' + code
    elif len(code) == 13:
        pass
    elif len(code) == 8:
        code = upc_server.convertUPCE(code)
    else:
        raise 'kaboom'
    return upc_server.lookupEAN(code)