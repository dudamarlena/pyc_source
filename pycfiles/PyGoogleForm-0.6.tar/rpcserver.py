# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pygoogleearth\rpcserver.py
# Compiled at: 2009-09-26 22:10:50
import SimpleXMLRPCServer, geapplication

class GoogleEarthXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
    """
    # Example Server Creation:
    import pygoogleearth
    rpcserver = pygoogleearth.GoogleEarthXMLRPCServer(('localhost', 9500))
    rpcserver.serve_forever()
    # Example Client
    import xmlrpclib
    google_earth = xmlrpclib.ServerProxy('http://localhost:9500')
    google_earth.set_camera_params(50.234392, -94.234343)
    """

    def __init__(self, *args, **kwargs):
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, allow_none=True, *args, **kwargs)
        self.register_instance(geapplication.GoogleEarth())


if __name__ == '__main__':
    print 'Dishing up Google Earth on port 9000'
    server = GoogleEarthXMLRPCServer(('localhost', 9000))
    server.serve_forever()