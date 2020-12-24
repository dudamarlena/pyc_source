# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/davfolder.py
# Compiled at: 2012-10-12 07:02:39
from xml.sax.saxutils import escape
from time import strftime, gmtime, time
from coils.foundation import *
from coils.core import *
from dav import DAV
from bufferedwriter import BufferedWriter
from reports import Parser
from davobject import DAVObject
PROP_METHOD = 0
PROP_NAMESPACE = 1
PROP_LOCALNAME = 2
PROP_DOMAIN = 3

class DAVFolder(DAV):
    """ Represents a DAV collection (folder).

        self.data is expected to be dict, where the key is the DAV name of the
        resource within the collection.  The contents of the value is a *list*
        where the first object is the Entity (Contact, Enterprise, Project,
        etc...) which the child represents.  That entity is passed to the
        new child object as 'entity'. """

    def __init__(self, parent, name, **params):
        DAV.__init__(self, parent, name, **params)

    @property
    def is_folder(self):
        return True

    def get_property_unknown_iscollection(self):
        return self.get_property_webdav_iscollection()

    def get_property_webdav_iscollection(self):
        """ Returns the value of the 'is collection' property which is always
            a value of '1'.  Believe this to be a non-standard WebDAV
            attribute. """
        return '1'

    def get_property_unknown_resourcetype(self):
        return self.get_property_webdav_resourcetype(self)

    def get_property_webdav_resourcetype(self):
        """ Return the resource type of the collection, which is always
            'collection'.

            See RFC2518, Section 13.9"""
        return '<D:collection/>'

    def get_property_unknown_getcontenttype(self):
        return self.get_property_webdav_getcontenttype(self)

    def get_property_webdav_getcontenttype(self):
        return self.context.user_agent_description['webdav']['folderContentType']

    def get_property_unknown_getcontentlength(self):
        return self.get_property_webdav_getcontentlength()

    def get_property_webdav_getcontentlength(self):
        """ Retun the content-length of the collection. The content length of
            a collection is always 0.

            See RFC2518, Section 13.4 """
        return '0'

    def get_property_webdav_displayname(self):
        """ Return the displayName of the collection.

            Used by PROPFIND requests."""
        return escape(self.name)

    def get_name(self):
        """ Return the name of the collection, this is the name in the URL
            which the client requested."""
        return self.name

    def do_HEAD(self):
        self.request.simple_response(200)

    def no_such_path(self):
        raise NoSuchPathException(('Not such path as {0}').format(self.request.path))

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        """Retrieve the DAV object for the specified name."""
        if auto_load_enabled:
            self.load_contents()
        if self.is_loaded:
            x = self.get_child(name)
            if x is not None:
                return x
        self.no_such_path()
        return

    def get_object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        return self.object_for_key(name, auto_load_enabled=auto_load_enabled, is_webdav=is_webdav)

    def do_GET(self):
        message = ('GET requests are not supported on collection objects, use a WebDAV client.\nCurrent path {0} is a collection.\n').format(self.webdav_url)
        self.request.simple_response(200, data=message, mimetype='text/plain')

    def do_LOCK(self):
        raise NotSupportedException('Locks on collections not supported by server')

    def do_UNLOCK(self):
        raise NotSupportedException('Locks on collections not supported by server')