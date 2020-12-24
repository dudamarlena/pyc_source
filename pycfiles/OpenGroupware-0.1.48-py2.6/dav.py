# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/dav.py
# Compiled at: 2012-10-12 07:02:39
import xmldict, urllib, json, re
from StringIO import StringIO
from coils.core import *
from pathobject import PathObject
from bufferedwriter import BufferedWriter
from reports import Parser, REVERSE_XML_NAMESPACE, introspect_properties
from xml.sax.saxutils import escape
from coils.foundation.api import elementflow
from itertools import izip
PATH_CACHE = {}
USE_CACHE = False
PROP_METHOD = 0
PROP_NAMESPACE = 1
PROP_LOCALNAME = 2
PROP_DOMAIN = 3
PROP_PREFIXED = 4

class DAV(PathObject):

    def get_appropriate_href(self, href):
        if self.context.user_agent_description['webdav']['absoluteHrefs']:
            if PathObject.__davServerName__ is None:
                server_name = self.request.server_name
            else:
                server_name = PathObject.__davServerName__
            if PathObject.__discardPortOnAbsoluteURLs__:
                return ('http://{0}{1}').format(server_name, href)
            return ('http://{0}:{1}{2}').format(server_name, self.request.server_port, href)
        else:
            return href
        return

    def __init__(self, parent, name, **params):
        """ Root DAV Object;  provides utility methods for implementing WebDAV.

        Keyword Arguments:
        parent - The parent object in the DAV hierarchy, should be a DAV object
        name - The name of this object, as used in the URL

        Additional named parameters are used to directly set attributes of this
        object,  so you you set fred=123 an attribute of fred will be set on the
        object with a value of 123.
        """
        self.name = name
        self._dentry = None
        self._contents = None
        self._aliases = None
        self._depth = -1
        PathObject.__init__(self, parent, **params)
        if hasattr(parent, 'root'):
            self._root = parent.root
        else:
            self._root = None
        if not hasattr(PathObject, '__discardPortOnAbsoluteURLs__'):
            sd = ServerDefaultsManager()
            PathObject.__discardPortOnAbsoluteURLs__ = sd.bool_for_default('DAVDiscardServerPort')
            server_name = sd.string_for_default('DAVHostForHref')
            if len(server_name):
                PathObject.__davServerName__ = server_name
            else:
                PathObject.__davServerName__ = None
        return

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def dir_entry(self):

        def lookup_dentry(self):
            if hasattr(self, 'entity'):
                if hasattr(self.entity, 'info'):
                    if self.entity.info:
                        if self.entity.info.version == self.entity.version:
                            return self.entity.info
                ObjectInfoManager.Repair(self.entity, self.context, log=self.log)
            return

        if self._dentry is None:
            dentry = lookup_dentry(self)
            if dentry:
                self._dentry = dentry
            else:
                self._dentry = False
        if self._dentry:
            return self._dentry
        else:
            return

    @property
    def is_folder(self):
        return False

    @property
    def is_object(self):
        return False

    def get_path(self):
        """ Reconstruct the path used to arrive at this object"""
        return self.current_path

    def get_parent_path(self):
        return self.parent.get_path()

    def quoted_value(self, value):
        if '&' in value or '<' in value or '"' in value:
            value = value.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')
        return value

    def unquoted_value(self, value):
        if '&amp;' in value or '&lt;' in value or '&quot;' in value:
            value = value.replace('&amp;', '&').replace('&lt;', '<').replace('&quot;', '"')
        return value

    @property
    def url(self):
        return self.get_absolute_path()

    @property
    def webdav_url(self):
        return self.get_appropriate_href(self.current_path)

    @property
    def current_path(self):
        """ Returns the path used in the current request to arrive at this object """
        path = self.name
        x = self.parent
        while x is not None:
            path = '%s/%s' % (x.get_name(), path)
            x = x.parent

        return self.quoted_value(path)

    @property
    def current_url(self):
        return self.get_appropriate_href(self.current_path)

    def insert_child(self, key, value, alias=None):
        key = unicode(key)
        if self._contents is None:
            self._contents = {}
        if self._aliases is None:
            self._aliases = {}
        self._contents[unicode(key)] = value
        if alias is not None:
            self._aliases[unicode(alias)] = key
        else:
            self._aliases[unicode(key)] = key
        return

    def empty_content(self):
        if self._contents is None:
            self._contents = {}
        if self._aliases is None:
            self._aliases = {}
        return

    def get_alias_for_key(self, key):
        if self._aliases is None:
            return key
        else:
            name = self._aliases.get(unicode(key), key)
            return name

    def get_child(self, key, minimum_components=1, component_seperator='.', supports_aliases=True):
        result = None
        key = str(key)
        if self._aliases is None:
            self.log.error('Aliases is not initialized')
        if self._contents is None:
            self.log.error('Contents is not initialized')
        if supports_aliases:
            if key in self._aliases:
                key = self._aliases[key]
        key = key.split(component_seperator)
        for i in range(len(key), 0, -1):
            if i < minimum_components:
                break
            result = self._contents.get(('.').join(key[0:i]), None)
            if result is not None:
                break

        return result

    def has_child(self, key, minimum_components=1, component_seperator='.', supports_aliases=True):
        if self.get_child(key, minimum_components=minimum_components, component_seperator=component_seperator, supports_aliases=supports_aliases) is None:
            return False
        else:
            return True

    def get_children(self):
        return self._contents.values()

    @property
    def is_loaded(self):
        if self._contents is None:
            return False
        else:
            return True

    def load_contents(self):
        """ If the DAV objects does not contain any data (self.data is None) then
            an attempt is made to retrieve the relevent information.  This method
            calls the _load_self() which the child is expected to implement. """
        if self.is_loaded:
            return True
        else:
            if self._load_contents():
                if self._contents is None:
                    self._contents = {}
                if self._aliases is None:
                    self._aliases = {}
                return True
            return False

    def _load_contents(self):
        return True

    def get_keys(self):
        if self.load_contents():
            return self._contents.keys()
        return []

    def get_aliased_keys(self):
        if self.load_contents():
            return self._aliases.keys()
        return []

    def get_property_webdav_href(self):
        return self.quoted_value(self.webdav_url)

    def get_ctag(self):
        """ Return a ctag appropriate for this object.
            Actual WebDAV objects should override this method """
        return '0'

    def get_property_webdav_executable(self):
        return self.get_property_apache_executable()

    def get_property_apache_executable(self):
        return '0'

    def get_property_unknown_creationdate(self):
        return self.get_property_webdav_creationdate()

    def get_property_webdav_creationdate(self):
        if self.dir_entry:
            if self.dir_entry.created:
                return self.dir_entry.created.strftime('%a, %d %b %Y %H:%M:%S GMT')
        if hasattr(self, 'entity'):
            if self.load_contents() and hasattr(self.entity, 'created'):
                if self.entity.created is not None:
                    return self.entity.created.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return 'Thu, 09 Sep 2010 10:17:06 GMT'

    def get_property_unknown_getlastmodified(self):
        return self.get_property_webdav_getlastmodified()

    def get_property_webdav_getlastmodified(self):
        if self.dir_entry:
            if self.dir_entry.modified:
                return self.dir_entry.modified.strftime('%a, %d %b %Y %H:%M:%S GMT')
        if hasattr(self, 'entity'):
            if self.load_contents() and hasattr(self.entity, 'modified'):
                if self.entity.modified is not None:
                    return self.entity.modified.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return 'Thu, 09 Sep 2010 10:17:06 GMT'

    def get_property_webdav_supportedlock(self):
        if self.supports_LOCK():
            return '<D:lockentry><D:lockscope><D:exclusive/></D:lockscope><D:locktype><D:write><D:/locktype></D:lockentry>'
        else:
            return
            return

    def get_property_webdav_lockdiscovery(self):
        if self.supports_LOCK():
            return
        else:
            return
            return

    def get_property_coils_revision(self):
        if hasattr(self, 'entity'):
            if hasattr(self.entity, 'version'):
                if self.entity.version:
                    return unicode(self.entity.version)
        return

    def get_property_coils_objectid(self):
        if hasattr(self, 'entity'):
            if hasattr(self.entity, 'object_id'):
                if self.entity.version:
                    return unicode(self.entity.object_id)
        return

    def supports_GET(self):
        return False

    def supports_POST(self):
        return False

    def supports_PUT(self):
        return False

    def supports_DELETE(self):
        return False

    def supports_PROPFIND(self):
        return True

    def supports_PROPPATCH(self):
        return True

    def supports_MKCOL(self):
        return False

    def supports_MOVE(self):
        return False

    def supports_LOCK(self):
        return False

    def supports_UNLOCK(self):
        return self.supports_LOCK()

    def supports_REPORT(self):
        return False

    def supports_ACL(self):
        return False

    def get_methods(self):
        return [
         'GET', 'POST', 'PUT', 'DELETE', 'PROPFIND', 'PROPPATCH', 'MKCOL',
         'MOVE', 'UNLOCK', 'LOCK', 'REPORT', 'ACL']

    def supports_operation(self, operation):
        operation = operation.upper().strip()
        method = ('supports_{0}').format(operation)
        if hasattr(self, method):
            return getattr(self, method)()
        return False

    def do_OPTIONS(self):
        """ Return a valid WebDAV OPTIONS response """
        methods = [
         'HEAD', 'OPTIONS']
        for method in self.get_methods():
            if self.supports_operation(method):
                methods.append(method)

        self.request.simple_response(200, data=None, headers={'DAV': '1', 'Allow': (',').join(methods), 
           'Connection': 'close', 
           'MS-Author-Via': 'DAV'})
        return

    def parse_propfind_for_property_names(self, payload):
        if not self.context:
            raise CoilsException('Operation has no context!')
        return Parser.propfind(payload, user_agent_description=self.context.user_agent_description)

    def do_PROPFIND(self):
        """ Respond to a PROPFIND request.

            RFC2518 Section 8.1

            The depth property of the request determines if this is an
            examination of the collection object (depth 0) or an
            examination of the collections contents (depth 1). If no
            depth is specified a depth of inifinity must be assumed
            [according to the spec; yes, that is stupid, but that is
            the spec]."""
        depth = Parser.get_depth(self.request)
        if depth == '1':
            depth = 2
        elif depth == '0':
            depth = 1
        else:
            depth = 25
        payload = self.request.get_request_payload()
        (props, namespaces) = self.parse_propfind_for_property_names(payload)
        w = StringIO('')
        with elementflow.xml(w, 'D:multistatus', indent=True, namespaces=namespaces) as (xml):
            if isinstance(props, basestring):
                if props == 'ALLPROP':
                    self.do_property_propfind(depth=depth, response=xml, allprop=True)
                elif props == 'PROPNAME':
                    self.do_propname_propfind(depth=depth, response=xml)
                else:
                    raise CoilsException('Unimplemented special case from PROPFIND parser')
            elif isinstance(props, list):
                self.do_property_propfind(props=props, depth=depth, response=xml)
            else:
                raise CoilsException('Unrecognzed response from PROPFIND parser')
        headers = {'X-Dav-Error': '200 No error', 'Ms-Author-Via': 'DAV'}
        if hasattr(self, 'location'):
            if self.context.user_agent_description['webdav']['supports301']:
                headers['Location'] = self.location
        self.request.simple_response(207, data=w.getvalue(), mimetype='text/xml; charset="utf-8"', headers=headers)
        if self.context.is_dirty:
            self.context.commit()

    def do_propname_propfind(self, depth=25, response=None):
        self.do_propname_response(depth=depth, response=response)

    def do_propname_response(self, depth=25, response=None):
        abbreviations = {}
        (properties, namespaces) = introspect_properties(self)
        with response.container('D:response', namespaces=namespaces) as (xml):
            xml.element('D:href', text=self.webdav_url)
            with xml.container('D:propstat'):
                for prop in properties:
                    xml.element(prop[4])

                xml.element('D:status', text='HTTP/1.1 200 OK')
        depth += -1
        if depth > 0 and self.is_folder:
            self.load_contents()
            for key in self.get_aliased_keys():
                result = self.get_object_for_key(key, auto_load_enabled=True, is_webdav=True)
                result.do_propname_response(depth=depth, response=response)

    def do_property_propfind(self, props=[], depth=25, response=None, allprop=False):
        self.do_property_response(props=props, depth=depth, response=response, allprop=allprop)

    def do_property_response(self, props=[], depth=25, response=None, allprop=False):
        known = {}
        unknown = []
        if allprop:
            (props, namespaces) = introspect_properties(self)
        for i in range(len(props)):
            prop = props[i]
            if hasattr(self, prop[PROP_METHOD]):
                x = getattr(self, prop[PROP_METHOD])
                known[prop] = x()
                x = None
            else:
                unknown.append(prop)

        if allprop:
            self.do_property_partial_response(depth=depth, response=response, allprop=True, known=known, unknown=unknown, namespaces=namespaces)
        else:
            self.do_property_partial_response(props=props, depth=depth, response=response, known=known, unknown=unknown, namespaces=[])
        return

    def do_property_partial_response(self, props=None, depth=25, response=None, allprop=False, known=None, unknown=None, namespaces=None):
        with response.container('D:response', namespaces=namespaces):
            response.file.write(('<D:href>{0}</D:href>').format(self.webdav_url))
            if len(known) > 0:
                with response.container('D:propstat'):
                    response.element('D:status', text='HTTP/1.1 200 OK')
                    with response.container('D:prop'):
                        for prop in known.keys():
                            if known[prop] is None:
                                response.element(prop[PROP_PREFIXED])
                            else:
                                response.element(prop[PROP_PREFIXED], text=unicode(known[prop]), escape=False)

            if len(unknown) > 0:
                with response.container('D:propstat'):
                    response.element('D:status', text='HTTP/1.1 404 Not found')
                    with response.container('D:prop'):
                        for prop in unknown:
                            response.element(prop[PROP_PREFIXED])

        depth += -1
        if depth > 0 and self.is_folder:
            self.load_contents()
            for key in self.get_aliased_keys():
                result = self.get_object_for_key(key, auto_load_enabled=True, is_webdav=True)
                result.do_property_response(props=props, depth=depth, response=response, allprop=allprop)

        return

    def do_PROPPATCH(self):
        payload = self.request.get_request_payload()
        (set_props, unset_props, namespaces) = Parser.proppatch(payload)
        w = StringIO('')
        with elementflow.xml(w, 'D:multistatus', indent=True, namespaces=namespaces) as (xml):
            with xml.container('D:response'):
                for prop in set_props:
                    if hasattr(self, prop[0]):
                        x = getattr(self, prop[0])
                        z = x(prop[5])
                        self.log.debug(('setting {0} property via {1} method').format(prop[4], prop[0]))
                        with xml.container('D:propstat'):
                            xml.element('D:prop', text=unicode(('<{0}/>').format(prop[4])), escape=False)
                            xml.element('D:status', text=unicode('HTTP/1.1 200 OK'))
                    else:
                        with xml.container('D:propstat'):
                            xml.element('D:prop', text=unicode(('<{0}/>').format(prop[4])), escape=False)
                            xml.element('D:status', text=unicode('HTTP/1.1 403 Forbidden'))

        data = w.getvalue()
        w.close()
        self.context.commit()
        self.log.debug(('Committed PROPPATCH to {0}').format(self.entity))
        self.request.simple_response(207, data=data, mimetype='text/xml; charset=UTF-8')

    def do_LOCK(self):
        if self.supports_LOCK():
            duration = 3600
            payload = self.request.get_request_payload()
            if len(payload) > 0:
                try:
                    lockinfo = Parser.lockinfo(payload, self.entity.object_id, self.context.account_id)
                except Exception, e:
                    self.log.error(('Failed to parse LOCK request: {0}').format(payload))
                    self.log.exception(e)
                    raise CoilsException('Failed to parse LOCK request')
                else:
                    lockinfo = self.context.lock_manager.lock(self.entity, duration, json.dumps(lockinfo['owner']))
            else:
                header = self.request.headers.get('If')
                self.log.info(('Got if header of {0}').format(header))
                token = re.findall('opaquelocktoken:[A-z0-9-]*', header)[0][16:]
                self.log.info(('Lock token is "{0}"').format(token))
                lockinfo = self.context.lock_manager.refresh(token, 5400)
            self.log.debug(('Lock info for LOCK operation: {0}').format(lockinfo))
            self.context.commit()
            if lockinfo is None:
                pass
            w = StringIO('')
            with elementflow.xml(w, 'D:prop', indent=True, namespaces={'D': 'DAV'}) as (xml):
                with xml.container('D:lockdiscovery'):
                    with xml.container('D:activelock'):
                        with xml.container('D:locktype'):
                            xml.element('D:write')
                        with xml.container('D:lockscope'):
                            xml.element('D:exclusive')
                        xml.element('D:depth', text='0')
                        if 'TEXT' in lockinfo['owner']:
                            xml.element('D:owner', text=lockinfo['owner']['TEXT'])
                        else:
                            xml.file.write(lockinfo['owner']['XML'])
                        xml.element('D:timeout', text=('Second-{0}').format(duration))
                        with xml.container('D:locktoken'):
                            xml.element('D:href', text=('opaquelocktoken:{0}').format(lockinfo['token']))
            data = w.getvalue()
            w.close()
            self.request.simple_response(200, data=data, mimetype='text/xml; charset=UTF-8', headers={'Lock-Token': ('opaquelocktoken:{0}').format(lockinfo['token'])})
        else:
            raise NotSupportedException('Lock on this object is not supported.')
        return

    def do_UNLOCK(self):
        if self.supports_UNLOCK():
            self.request.simple_response(204)
        else:
            raise NotSupportedException('Locks on collections not supported by server')