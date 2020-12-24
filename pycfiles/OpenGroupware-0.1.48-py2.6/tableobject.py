# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/tableobject.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from coils.core import *
from coils.net import *
from coils.net import *

class TableObject(DAVObject):
    """ Represents a workflow message in a process with a DAV hierarchy. """

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)
        self.log.debug((' TableObject named {0} is entity {1}').format(name, repr(self.entity)))
        self._yaml = None
        return

    def get_yaml_content(self):
        if self._yaml is None:
            self._yaml = self.entity.as_yaml()
        return self._yaml

    def get_property_webdav_getetag(self):
        return ('{0}').format(self.entity.name)

    def get_property_webdav_displayname(self):
        return ('{0}').format(self.entity.name)

    def get_property_webdav_getcontentlength(self):
        return str(len(self.get_yaml_content()))

    def get_property_webdav_getcontenttype(self):
        return 'text/plain'

    def get_property_webdav_creationdate(self):
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def do_HEAD(self):
        self.request.simple_response(201, mimetype=self.get_property_webdav_getcontenttype(), headers={'Content-Length': self.get_property_webdav_getcontentlength(), 'etag': self.get_property_webdav_getetag()})

    def do_GET(self):
        self.request.simple_response(200, data=self.get_yaml_content(), mimetype=self.get_property_webdav_getcontenttype(), headers={'ETag': self.get_property_webdav_getetag()})