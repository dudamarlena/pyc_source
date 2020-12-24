# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/xsltobject.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from coils.core import *
from coils.net import *

class XSLTObject(DAVObject):

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def get_property_webdav_getetag(self):
        return ('{0}:{1}').format(self.entity.name, self.get_property_webdav_modifieddate())

    def get_property_webdav_displayname(self):
        return self.entity.name

    def get_property_webdav_getcontentlength(self):
        return str(self.entity.size)

    def get_property_webdav_getcontenttype(self):
        return 'text/xml'

    def get_property_webdav_creationdate(self):
        return self.entity.created

    def get_property_webdav_modifieddate(self):
        return self.entity.modified

    def do_HEAD(self):
        self.request.simple_response(201, mimetype=self.entity.mimetype, headers={'Content-Length': str(self.entity.size), 'ETag': self.get_property_webdav_getetag()})

    def do_GET(self):
        self.request.stream_response(200, stream=self.entity.handle, mimetype='application/xml', headers={'etag': self.get_property_webdav_getetag()})