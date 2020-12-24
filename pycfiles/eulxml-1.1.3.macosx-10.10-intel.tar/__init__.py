# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/__init__.py
# Compiled at: 2016-06-03 15:43:14
import os, pkg_resources
__version_info__ = (1, 1, 3, None)
__version__ = ('.').join([ str(i) for i in __version_info__[:-1] ])
if __version_info__[(-1)] is not None:
    __version__ += '-%s' % (__version_info__[(-1)],)
SCHEMA_DATA_DIR = 'schema_data'
if pkg_resources.resource_isdir(__name__, SCHEMA_DATA_DIR):
    XMLCATALOG_DIR = pkg_resources.resource_filename(__name__, SCHEMA_DATA_DIR)
    XMLCATALOG_FILE = pkg_resources.resource_filename(__name__, '%s/catalog.xml' % SCHEMA_DATA_DIR)
else:
    XMLCATALOG_DIR = os.path.join(os.path.dirname(__file__), SCHEMA_DATA_DIR)
    XMLCATALOG_FILE = os.path.join(XMLCATALOG_DIR, 'catalog.xml')
if XMLCATALOG_FILE not in os.environ.get('XML_CATALOG_FILES', ''):
    os.environ['XML_CATALOG_FILES'] = (':').join([ path for path in (os.environ.get('XML_CATALOG_FILES'), XMLCATALOG_FILE) if path
                                                 ])