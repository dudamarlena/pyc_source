# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Updoc/updoc/iniconf.py
# Compiled at: 2017-07-18 01:53:20
# Size of source mod 2**32: 1247 bytes
from djangofloor.conf.fields import BooleanConfigField, CharConfigField
from djangofloor.conf.mapping import SENDFILE_MAPPING, INI_MAPPING as DEFAULT
__author__ = 'Matthieu Gallet'
INI_MAPPING = DEFAULT + SENDFILE_MAPPING + [
 BooleanConfigField('global.public_bookmarks', 'PUBLIC_BOOKMARKS', help_str='Are bookmarks publicly available?'),
 BooleanConfigField('global.public_proxies', 'PUBLIC_PROXIES', help_str='Is proxy.pac file publicly available?'),
 BooleanConfigField('global.public_index', 'PUBLIC_INDEX', help_str='Is the list of all documentations publicly available?'),
 BooleanConfigField('global.public_docs', 'PUBLIC_DOCS', help_str='Are documentations publicly available?'),
 CharConfigField('elasticsearch.hosts', 'ES_HOSTS', help_str='Comma-separated list of ElasticSearch servers.\nElasticSearch can be used to index all documents but remains optional.Example: es-srv1.example.org:9200,es-srv2.example.org:9200'),
 CharConfigField('elasticsearch.index', 'ES_INDEX', help_str='Name of the ElasticSearch index')]