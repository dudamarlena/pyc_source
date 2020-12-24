# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/bpmlobject.py
# Compiled at: 2012-10-12 07:02:39
import io
from datetime import datetime
from coils.core import *
from coils.net import *
from coils.net import *
from utility import filename_for_route_markup, filename_for_process_markup

class BPMLObject(DAVObject):
    """ Represent a BPML markup object in WebDAV """

    def __init__(self, parent, name, **params):
        self.version = None
        DAVObject.__init__(self, parent, name, **params)
        if self.version is None:
            self.version = self.entity.version
        return

    def get_property_webdav_getetag(self):
        return ('{0}:{1}').format(self.entity.object_id, self.version)

    def get_property_webdav_displayname(self):
        if isinstance(self.entity, Route):
            return ('BPML Markup of route {0}').format(self.entity.name)
        if isinstance(self.entity, Process):
            return ('BPML Markup for process {0}').format(self.entity.object_id)
        raise CoilsException('Invalid entity for BPMLObject')

    def get_property_webdav_getcontentlength(self):
        markup = self.entity.get_markup()
        if markup is None:
            return '0'
        else:
            return unicode(len(self.entity.get_markup()))

    def get_property_webdav_getcontenttype(self):
        return 'application/xml'

    def get_property_webdav_creationdate(self):
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def do_GET(self):
        """ Handle a GET request. """
        if isinstance(self.entity, Route):
            handle = BLOBManager.Open(filename_for_route_markup(self.entity, self.version), 'rb', encoding='binary')
        else:
            handle = BLOBManager.Open(filename_for_process_markup(self.entity), 'rb', encoding='binary')
        self.request.stream_response(200, stream=handle, mimetype='application/xml', headers={'etag': self.get_property_webdav_getetag()})
        BLOBManager.Close(handle)