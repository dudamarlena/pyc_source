# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/amsterdam/config/scirius/local_settings.py
# Compiled at: 2016-05-22 16:35:41
import os
USE_ELASTICSEARCH = True
ELASTICSEARCH_ADDRESS = 'elasticsearch:9200'
ELASTICSEARCH_2X = True
KIBANA_VERSION = 4
KIBANA_INDEX = '.kibana'
KIBANA_URL = 'http://kibana:5601'
SURICATA_UNIX_SOCKET = '/var/run/suricata/suricata-command.socket'
USE_KIBANA = True
KIBANA_PROXY = True
KIBANA_DASHBOARDS_COUNT = 25
USE_EVEBOX = True
EVEBOX_ADDRESS = 'evebox:5636'
USE_SURICATA_STATS = True
USE_LOGSTASH_STATS = True
ELASTICSEARCH_LOGSTASH_ALERT_INDEX = 'logstash-alert-'
DATA_DIR = '/sciriusdata/'
STATIC_ROOT = '/sciriusstatic/'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(DATA_DIR, 'scirius.sqlite3')}}
GIT_SOURCES_BASE_DIRECTORY = os.path.join(DATA_DIR, 'git-sources/')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DBBACKUP_STORAGE = 'dbbackup.storage.filesystem_storage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backups/'}