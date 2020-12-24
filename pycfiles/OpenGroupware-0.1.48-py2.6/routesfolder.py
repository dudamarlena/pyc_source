# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/routesfolder.py
# Compiled at: 2012-10-12 07:02:39
import os
from tempfile import mkstemp
from coils.core import *
from coils.net import DAVFolder, OmphalosCollection
from routefolder import RouteFolder
from utility import compile_bpml
from signalobject import SignalObject
from workflow import WorkflowPresentation

class RoutesFolder(DAVFolder, WorkflowPresentation):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        self.data = {}
        if self.name == 'Routes':
            self.log.debug('Returning enumeration of available routes.')
            routes = self.context.run_command('route::get', properties=[Route])
            for route in routes:
                self.insert_child(route.name, route)

        else:
            return False
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == 'signal':
            return SignalObject(self, name, parameters=self.parameters, entity=None, context=self.context, request=self.request)
        else:
            if name in ('.ls', '.json', '.contents'):
                if self.load_contents():
                    if name in ('.json', '.contents'):
                        return OmphalosCollection(self, name, detailLevel=65535, rendered=True, data=self.get_children(), parameters=self.parameters, context=self.context, request=self.request)
                    if name == '.ls':
                        return OmphalosCollection(self, name, rendered=False, data=self.get_children(), parameters=self.parameters, context=self.context, request=self.request)
            else:
                if self.is_loaded:
                    route = self.get_child(name)
                else:
                    route = self.context.run_command('route::get', name=name)
                if route:
                    return RouteFolder(self, name, parameters=self.parameters, entity=route, context=self.context, request=self.request)
            raise self.no_such_path()
            return

    def do_PUT(self, request_name):
        """ Allows routes to be created by dropping BPML documents into /dav/Routes """
        bpml = BLOBManager.ScratchFile(suffix='bpml')
        bpml.write(self.request.get_request_payload())
        (description, cpm) = compile_bpml(bpml, log=self.log)
        try:
            route = self.context.run_command('route::new', values=description, handle=bpml)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Route creation failed.')

        BLOBManager.Close(bpml)
        self.context.commit()
        self.request.simple_response(301, headers={'Location': ('/dav/Workflow/Routes/{0}/markup.xml').format(route.name), 'Content-Type': 'text/xml'})