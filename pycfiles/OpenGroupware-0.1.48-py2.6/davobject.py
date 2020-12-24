# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/davobject.py
# Compiled at: 2012-10-12 07:02:39
from xml.sax.saxutils import escape
from time import strftime, gmtime, time
from coils.foundation import *
from coils.core import *
from bufferedwriter import BufferedWriter
from dav import DAV
from reports import Parser
from entity_map import ENTITYMAP

class DAVObject(DAV):
    """ Represents an OpenGroupware entity in a DAV collection,  a GET will return the
        representation of the object - vCard, vEvent, vToDo, etc... """

    def __init__(self, parent, name, **params):
        DAV.__init__(self, parent, name, **params)
        self._representation = None
        return

    @property
    def is_object(self):
        return True

    def supports_GET(self):
        return True

    def get_property_getetag(self):
        if self.load_contents():
            if hasattr(self.entity, 'object_id'):
                left = str(self.entity.object_id)
            elif hasattr(self.entity, 'uuid'):
                left = self.entity.uuid.strip()
            else:
                raise CoilsException('No candidate property for etag creation')
        if hasattr(self.entity, 'version'):
            if self.entity.version is None:
                return ('{0}:0').format(left, self.entity.version)
            else:
                return ('{0}:{1}').format(left, self.entity.version)
        else:
            return ('{0}:0').format(left)
        return

    def get_property_unknown_getetag(self):
        return self.get_property_getetag()

    def get_property_webdav_getetag(self):
        return self.get_property_getetag()

    def get_property_unknown_iscollection(self):
        return self.get_property_webdav_iscollection()

    def get_property_webdav_iscollection(self):
        return '0'

    def get_property_webdav_displayname(self):
        return escape(self.name)

    def get_property_unknown_resourcetype(self):
        return self.get_property_webdav_resourcetype(self)

    def get_property_webdav_resourcetype(self):
        return ''

    def get_property_unknown_getcontentlength(self):
        return self.get_property_webdav_getcontentlength()

    def get_property_webdav_getcontentlength(self):
        if self.dir_entry:
            if self.entity.info.ics_size:
                return self.entity.info.ics_size
        payload = self.get_representation()
        if payload:
            return str(len(payload))
        return '0'

    def get_property_unknown_getcontenttype(self):
        return get_property_webdav_getcontenttype(self)

    def get_property_webdav_getcontenttype(self):
        if hasattr(self.entity, '__entityName__'):
            if self.entity.__entityName__ in ENTITYMAP:
                return ENTITYMAP[self.entity.__entityName__]['mime-type']
        return 'application/octet-stream'

    def get_property_unknown_href(self):
        return self.get_property_webdav_href()

    def get_property_webdav_href(self):
        return self.webdav_url

    def supports_LOCK(self):
        if hasattr(self, 'entity'):
            if hasattr(self.entity, 'object_id'):
                return True
        return False

    def get_keys(self):
        return

    def _load_contents(self):
        if self.entity is None:
            if self.name.isdigit():
                object_id = int(self.name)
                kind = self.context.type_manager.get_type(object_id)
                if kind == 'Unknown':
                    return False
                self.entity = self.context.run_command(ENTITYMAP[kind]['get-command'], id=object_id)
                if self.entity is None:
                    return False
            else:
                return False
        return True

    def get_representation(self):
        if self.load_contents():
            command = ENTITYMAP[self.entity.__entityName__]['data-command']
            self.log.debug(('Selected {0} to retrieve object representation.').format(command))
            x = self.context.run_command(ENTITYMAP[self.entity.__entityName__]['data-command'], object=self.entity)
            if x is None:
                self.log.warn('Data command for object representation returned None!')
                return ''
        return x

    def do_GET(self):
        if hasattr(self, 'location') and self.location is not None:
            if self.current_path != self.location:
                if self.context.user_agent_description['webdav']['supports301']:
                    self.log.debug(('Redirecting client from {0} to {1}').format(self.current_path, self.location))
                    self.request.simple_response(301, headers={'Location': self.location})
                    return
                self.log.warn(('Redirectable request for "{0}" from user-agent "{1}" known to not support 301 responses; would have redirected to "{2}"').format(self.current_path, self.context.user_agent_description['name'], self.location))
        payload = self.get_representation()
        if payload is not None:
            self.request.simple_response(200, data=payload, mimetype=ENTITYMAP[self.entity.__entityName__]['mime-type'], headers={'ETag': self.get_property_getetag()})
            if self.context.is_dirty:
                self.context.commit()
            return
        else:
            raise NoSuchPathException('%s not found' % self.name)
            return

    def do_HEAD(self):
        if hasattr(self, 'location') and self.location is not None:
            if self.current_path != self.location:
                if self.context.user_agent_description['webdav']['supports301']:
                    self.log.debug(('Redirecting client from {0} to {1}').format(self.current_path, self.location))
                    self.request.simple_response(301, headers={'Location': self.location})
                    return
                self.log.warn(('Redirectable request for "{0}" from user-agent "{1}" known to not support 301 responses; would have redirected to "{2}"').format(self.current_path, self.context.user_agent_description['name'], self.location))
        x = self.get_representation()
        if x is not None:
            x = unicode(x)
            self.request.simple_response(204, data=None, mimetype=ENTITYMAP[self.entity.__entityName__]['mime-type'], headers={'ETag': self.get_property_getetag(), 'Content-Length': len(x)})
            return
        else:
            raise NoSuchPathException(('{0} not found').format(self.name))
            return