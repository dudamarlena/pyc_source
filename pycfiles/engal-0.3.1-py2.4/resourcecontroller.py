# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/engal/resourcecontroller.py
# Compiled at: 2006-09-19 08:27:24
from turbogears import controllers, expose
import cherrypy, logging
log = logging.getLogger('engal.resourcecontroller')

class Resource(controllers.Controller):
    __module__ = __name__
    item_getter = None
    friendly_resource_name = None
    exposed_resource = True

    @expose()
    def default(self, *vpath, **params):
        if not vpath:
            return self.index(**params)
        vpath = list(vpath)
        atom = vpath.pop(0)
        method = getattr(self, atom, None)
        if method and getattr(method, 'expose_container', False):
            return method(*vpath, **params)
        item = self.item_getter(atom)
        if item is None:
            raise cherrypy.NotFound
        self._addResource(item)
        if vpath:
            method = getattr(self, vpath[0], None)
            if method and getattr(method, 'exposed_resource'):
                return method(item, *vpath[1:], **params)
        return self.show(item, *vpath, **params)

    def _addResource(self, item):
        if not getattr(cherrypy.request, '_resourcecontroller', None):
            cherrypy.request._resourcecontroller = dict()
        cherrypy.request._resourcecontroller[self] = item
        if self.friendly_resource_name:
            cherrypy.request._resourcecontroller[friendly_resource_name] = item
        return

    def _getResource(self):
        return cherrypy.request._resourcecontroller.get(self, None)

    def _getResources(self):
        return cherrypy.request._resourcecontroller


def expose_resource(func):
    func.exposed = False
    func.exposed_resource = True
    return func