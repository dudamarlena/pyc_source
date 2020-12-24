# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/documentobject.py
# Compiled at: 2012-10-12 07:02:39
import urllib
from StringIO import StringIO
from time import strftime, gmtime, time
from coils.core import *
from coils.net import DAVObject, Parser
from coils.net.ossf import MarshallOSSFChain
from coils.foundation.api import elementflow

class DocumentObject(DAVObject):
    _MIME_MAP_ = None

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)
        if DocumentObject._MIME_MAP_ is None:
            sd = ServerDefaultsManager()
            self._mime_type_map = sd.default_as_dict('CoilsExtensionMIMEMap')
        return

    def __repr__(self):
        return ('<DocumentObject path="{0}"/>').format(self.get_path())

    def get_property_webdav_getlastmodified(self):
        x = gmtime(time())
        return strftime('%a, %d %b %Y %H:%M:%S GMT', x)

    def get_property_webdav_getcontentlength(self):
        return str(self.entity.file_size)

    def get_property_webdav_creationdate(self):
        if self.entity.created is not None:
            return self.entity.created.strftime('%a, %d %b %Y %H:%M:%S GMT')
        else:
            return self.get_property_webdav_getlastmodified()
            return

    def get_property_webdav_getlastmodified(self):
        if self.entity.modified is not None:
            return self.entity.modified.strftime('%a, %d %b %Y %H:%M:%S GMT')
        else:
            return strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime(time()))
            return

    def get_property_webdav_getcontenttype(self):
        return self.entity.get_mimetype(type_map=self._mime_type_map)

    def get_mswebdav_property(self, name, default=None):
        prop = self.context.property_manager.get_property(self.entity, 'http://www.opengroupware.us/mswebdav', 'win32fileattributes')
        if prop is None:
            return default
        else:
            return prop.get_value()

    def set_mswebdav_property(self, name, value):
        self.context.property_manager.set_property(self.entity, 'http://www.opengroupware.us/mswebdav', name, value)

    def get_property_mswebdav_win32fileattributes(self):
        return self.get_mswebdav_property('win32fileattributes', '00000020')

    def set_property_mswebdav_win32fileattributes(self, value):
        return self.set_mswebdav_property('win32fileattributes', value)

    def get_property_mswebdav_win32lastmodifiedtime(self):
        return self.get_mswebdav_property('win32lastmodifiedtime', self.get_property_webdav_getlastmodified())

    def set_property_mswebdav_win32lastmodifiedtime(self, value):
        return self.set_mswebdav_property('win32lastmodifiedtime', value)

    def get_property_mswebdav_win32lastaccesstime(self):
        return self.get_mswebdav_property('win32lastaccesstime', None)

    def set_property_mswebdav_win32lastaccesstime(self, value):
        return self.set_mswebdav_property('win32lastaccesstime', value)

    def get_property_mswebdav_win32creationtime(self):
        return self.get_mswebdav_property('win32creationtime', None)

    def set_property_mswebdav_win32creationtime(self, value):
        return self.set_mswebdav_property('win32creationtime', value)

    def get_property_coils_checksum(self):
        return self.entity.checksum

    def get_property_coils_ownerid(self):
        return unicode(self.entity.owner_id)

    def get_property_coils_revisioncount(self):
        return unicode(self.entity.version_count)

    def do_HEAD(self):
        self.request.simple_response(200, data=None, mimetype=self.entity.get_mimetype(type_map=self._mime_type_map), headers={'etag': self.get_property_getetag(), 'Content-Length': str(self.entity.file_size)})
        return

    def do_GET(self):
        handle = self.context.run_command('document::get-handle', id=self.entity.object_id)
        self.log.debug(('Document MIME-Type is "{0}"').format(self.entity.mimetype))
        (handle, mimetype) = MarshallOSSFChain(handle, self.entity.mimetype, self.parameters)
        self.log.debug(('MIME-Type after OSSF processing is {0}').format(mimetype))
        self.context.run_command('document::record-download', document=self.entity)
        self.context.commit()
        self.request.stream_response(200, stream=handle, mimetype=mimetype, headers={'etag': self.get_property_getetag()})
        BLOBManager.Close(handle)