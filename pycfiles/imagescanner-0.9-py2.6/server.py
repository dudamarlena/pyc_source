# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imagescanner/core/server.py
# Compiled at: 2011-05-14 11:06:17
"""ImageScanner XMLRPC library. 

Runs a server which provide some of the library features on the network.

$id$

"""
import xmlrpclib
from cStringIO import StringIO
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import cjson
from imagescanner import ImageScanner
from imagescanner.utils import scanner_serializer

def list_scanners():
    devices = ImageScanner(remote_search=False).list_scanners()
    serialized_devices = [ scanner_serializer(device) for device in devices ]
    return cjson.encode(serialized_devices)


def scan(device_id):
    image = ImageScanner(remote_search=False).scan(device_id)
    if image is None:
        return
    else:
        image_data = StringIO()
        image.save(image_data, 'tiff')
        image_data.seek(0)
        return xmlrpclib.Binary(image_data.read())


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2', )


def run(listen_address, port):
    server = SimpleXMLRPCServer((listen_address, port), requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_function(list_scanners)
    server.register_function(scan)
    server.serve_forever()