# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/reports/namespaces.py
# Compiled at: 2012-10-12 07:02:39
XML_NAMESPACE = {'http://www.w3.org/1999/xhtml': 'xhtml', 'dav': 'webdav', 
   'dav:': 'webdav', 
   'http://apache.org/dav/props/': 'webdav', 
   'urn:schemas-microsoft-com:office:office': 'msoffice', 
   'urn:schemas-microsoft-com:office:word': 'msword', 
   'http://schemas.microsoft.com/hotmail/': 'hotmail', 
   'urn:schemas-microsoft-com:': 'mswebdav', 
   'urn:schemas:httpmail:': 'mshttpmail', 
   'http://schemas.microsoft.com/exchange/': 'msexchange', 
   'urn:schemas:calendar:': 'mscalendar', 
   'urn:schemas:contacts:': 'mscontacts', 
   'http://webdav.org/cadaver/custom-properties/': 'cadaver', 
   'http://services.eazel.com/namespaces': 'eazel', 
   'http://www.w3.org/2005/Atom': 'atom', 
   'http://groupdav.org/': 'groupdav', 
   'http://calendarserver.org/ns/': 'caldav', 
   'urn:ietf:params:xml:ns:caldav': 'caldav', 
   'urn:ietf:params:xml:ns:carddav': 'carddav', 
   '57c7fc84-3cea-417d-af54-b659eb87a046': 'coils', 
   '"http://ucb.openoffice.org/dav/props/': 'openoffice'}
REVERSE_XML_NAMESPACE = {'webdav': 'dav', 'apache': 'http://apache.org/dav/props/', 
   'caldav': 'urn:ietf:params:xml:ns:caldav', 
   'carddav': 'urn:ietf:params:xml:ns:carddav', 
   'coils': '57c7fc84-3cea-417d-af54-b659eb87a046', 
   'groupdav': 'http://groupdav.org/', 
   'mswebdav': 'urn:schemas-microsoft-com', 
   'openoffice': '"http://ucb.openoffice.org/dav/props/', 
   'atom': 'http://www.w3.org/2005/Atom'}
ALL_PROPS = [
 ('get_property_webdav_name', 'DAV:', 'name', 'webdav'),
 ('get_property_webdav_href', 'DAV:', 'href', 'webdav'),
 ('get_property_webdav_getcontenttype', 'DAV:', 'getcontenttype', 'webdav'),
 ('get_property_webdav_contentclass', 'DAV:', 'contentclass', 'webdav'),
 ('get_property_webdav_getlastmodified', 'DAV:', 'getlastmodified', 'webdav'),
 ('get_property_webdav_getcontentlength', 'DAV:', 'getcontentlength', 'webdav'),
 ('get_property_webdav_iscollection', 'DAV:', 'iscollection', 'webdav'),
 ('get_property_webdav_displayname', 'DAV:', 'displayname', 'webdav'),
 ('get_property_caldav_getctag', 'urn:ietf:params:xml:ns:caldav', 'getctag', 'webdav'),
 ('get_property_webdav_resourcetype', 'DAV:', 'resourcetype', 'webdav')]