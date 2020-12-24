# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/yamlobject.py
# Compiled at: 2012-10-12 07:02:39
import io, yaml, pickle
from datetime import datetime
from coils.core import *
from coils.net import *
from utility import compile_bpml, filename_for_route_markup, filename_for_process_code

class YAMLObject(DAVObject):
    """ Represent a BPML markup object in WebDAV """

    def __init__(self, parent, name, **params):
        self.version = None
        DAVObject.__init__(self, parent, name, **params)
        self._payload = None
        if self.version is None:
            self.version = self.entity.version
        return

    def get_markup(self):
        if self._payload is None:
            cpm = None
            if isinstance(self.entity, Route):
                code = BLOBManager.Open(filename_for_route_markup(self.entity, self.version), 'rb', encoding='binary')
                (description, cpm) = compile_bpml(code, log=self.log)
                BLOBManager.Close(code)
            elif isinstance(self.entity, Process):
                code = BLOBManager.Open(filename_for_process_code(self.entity, self.version), 'rb', encoding='binary')
                cpm = pickle.load(code)
                BLOBManager.Close(code)
            self._payload = yaml.dump(cpm)
        return self._payload

    def get_property_webdav_getetag(self):
        return ('{0}:{1}:YAML').format(self.entity.object_id, self.entity.version)

    def get_property_webdav_displayname(self):
        return self.name

    def get_property_webdav_getcontentlength(self):
        return str(len(self.get_markup()))

    def get_property_webdav_getcontenttype(self):
        return 'application/yaml'

    def get_property_webdav_creationdate(self):
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def do_GET(self):
        """ Handle a GET request. """
        self.request.simple_response(200, data=self.get_markup(), mimetype='application/yaml', headers={'ETag': self.get_property_webdav_getetag()})