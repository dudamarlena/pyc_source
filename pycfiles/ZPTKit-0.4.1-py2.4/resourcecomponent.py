# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ZPTKit/resourcecomponent.py
# Compiled at: 2006-06-20 16:13:48
"""
This module can be used to create fall-back resources.  E.g., if you
have no Context/stylesheet.css, you may define another directory where
these resources may be found.

Typically you use this by turning ExtraPathInfo on in
Application.config, and adding a component to index.py (or Main.py)
like::

    components = SitePage.components + [
        ResourceComponent(resource_paths)]
"""
import os, mimetypes
from Component import ServletComponent, Component

class ResourceServletComponent(ServletComponent):
    __module__ = __name__

    def __init__(self, resource_dirs):
        if isinstance(resource_dirs, (str, unicode)):
            resource_dirs = [
             resource_dirs]
        self.resource_dirs = resource_dirs

    def awakeEvent(self, trans):
        req = trans.request()
        res = trans.response()
        path = req.extraURLPath()
        if not path:
            return
        assert path.startswith('/')
        path = path.lstrip('/')
        assert not path.startswith('/')
        for dir in self.resource_dirs:
            filename = os.path.join(dir, path)
            if os.path.exists(filename):
                break
        else:
            res.setHeader('status', '404 Not Found')
            res.write('<html><head><title>Not Found</title>\n            </head><body>\n            <h1>Not Found</h1>\n            The resource %s was not found.\n            </body></html>' % req.environ().get('REQUEST_URI'))
            self.servlet().endResponse()

        (type, encoding) = mimetypes.guess_type(filename)
        res.setHeader('content-type', type)
        if encoding:
            res.setHeader('content-encoding', encoding)
        res.flush()
        f = open(filename, 'rb')
        while 1:
            t = f.read(8000)
            if not t:
                break
            res.write(t)

        f.close()
        self.servlet().endResponse()


class ResourceComponent(Component):
    __module__ = __name__
    _componentClass = ResourceServletComponent