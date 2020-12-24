# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/proplistobject.py
# Compiled at: 2012-10-12 07:02:39
from base64 import b64encode
from StringIO import StringIO
from datetime import datetime
from coils.core import *
from coils.net import *

class PropertyListObject(DAVObject):
    """ Represent a BPML markup object in WebDAV """

    def __init__(self, parent, name, **params):
        self.version = None
        DAVObject.__init__(self, parent, name, **params)
        self.text = None
        return

    def get_property_webdav_getetag(self):
        return ('{0}:{1}:propertyList').format(self.entity.object_id, self.entity.version)

    def get_property_webdav_displayname(self):
        return 'Object Property List'

    def get_property_webdav_getcontentlength(self):
        self.generate_property_list_text()
        return str(len(self.text))

    def get_property_webdav_getcontenttype(self):
        return 'text/plain'

    def get_property_webdav_creationdate(self):
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def get_property_webdav_getlastmodified(self):
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    def generate_property_list_text(self):
        if self.text is None:
            props = self.context.property_manager.get_properties(self.entity)
            stream = StringIO('')
            if len(props) > 0:
                for prop in props:
                    stream.write(('{{{0}}}{1}\r\n').format(prop.namespace, prop.name))
                    try:
                        try:
                            x = None
                            x = unicode(prop.get_value())
                        except:
                            x = b64encode(prop.get_value)

                    finally:
                        stream.write(x)

                    stream.write('\r\n')
                    stream.write('\r\n')

            else:
                stream.write('\r\n')
            self.text = stream.getvalue()
            stream.close()
        return

    def do_GET(self):
        """ Handle a GET request. """
        self.generate_property_list_text()
        self.request.simple_response(200, data=self.text, mimetype='application/text', headers={'ETag': self.get_property_webdav_getetag()})