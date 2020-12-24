# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/config.py
# Compiled at: 2007-12-17 05:32:50
"""Configuration for instance manager
"""
CONFIGDIR = '.instancemanager'
SITECONFIG = '/etc/instancemanager/sitedefaults.py'
SECRET_PREFIX = 'local-'
STUB_PREFIX = 'stub.'
DEBUGCONFIGCHANGES = {'#    security-policy-implementation python': 'security-policy-implementation python\n', 'verbose-security on': 'verbose-security on\n', 'debug-mode on': 'debug-mode on\n', 'devmode on': 'devmode on\n'}
CONFSNIPPETS = {'http-server': {'address ': 'address %(port)s'}, 'ftp-server': {'address ': '  address %(ftp_port)s'}, 'webdav-source-server': {'address ': '  address %(webdav_port)s'}, 'icp-server': {'address ': '  address %(icp_port)s'}}
SNIPPETCONDITIONS = {'http-server': 'port', 'server': 'port', 'ftp-server': 'ftp_port', 'webdav-source-server': 'webdav_port', 'icp-server': 'icp_port'}
Z3FTPPORTSNIPPET = '<server ftp>\n  type FTP\n  address %(ftp_port)s\n</server>\n'
LOGFILE = 'instancemanager.log'
QISCRIPT = 'quickreinstaller.py'
UISCRIPT = 'uninstaller.py'
PACKSCRIPT = 'pack.py'
CHANGEOWNSCRIPT = 'changeownership.py'
ZEOSNIPPET = '<zodb_db main>\n  mount-point /\n  # ZODB cache, in number of objects\n  cache-size 500\n  <zeoclient>\n    server localhost:%(zeoport)s\n    storage 1\n    name zeostorage\n    var $INSTANCE/var\n    # ZEO client cache, in bytes\n    cache-size 20MB\n    # Uncomment to have a persistent disk cache\n    %(zeo_client_line)s\n  </zeoclient>\n</zodb_db>\n'
Z3ZEOSNIPPET = '<zodb>\n  <zeoclient>\n    server localhost:%(zeoport)s\n    storage 1\n    # ZEO client cache, in bytes\n    cache-size 20MB\n    # Uncomment to have a persistent disk cache\n    #client zeo1\n  </zeoclient>\n</zodb>\n'
DATABASE_TEMPFILES = [
 'Data.fs.tmp', 'Data.fs.index', 'Data.fs.lock']
APACHE_TEMPLATE = "\nFor the apache config:\n\n  # Use the simple example at \n  # http://plone.org/documentation/tutorial/plone-apache/virtualhost\n  # as your starting point.\n\n  # Configuration for use with a squid that is configured using CacheFu.\n  # Normalize URLs by removing trailing /'s\n  RewriteRule ^/(.*)/$ http://127.0.0.1:3128/http/%(sn)s/80/$1 [L,P]\n  # Pass all other urls straight through\n  RewriteRule ^/(.*)$  http://127.0.0.1:3128/http/%(sn)s/80/$1 [L,P]\n\n  # If you have zope directly behind apache, use the following;\n  #RewriteRule ^(.*) http://localhost:%(zopeport)s/VirtualHostBase/http/%(sn)s:80/%(plonesite)s/VirtualHostRoot$1 [L,P]\n\n\nFor at the end of the cachefu squid.cfg (in CacheFuDocumentation/squid):\n\n  yoursitenamehere.com: 127.0.0.1:%(zopeport)s/%(plonesite)s\n\n"