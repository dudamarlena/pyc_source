# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jcrack/celeryconfig.py
# Compiled at: 2012-02-06 22:03:28
import jconfig
config = jconfig.getConfig()
dburi = 'mysql://' + config.get('db', 'user') + ':' + config.get('db', 'passwd') + '@' + config.get('db', 'host') + '/' + config.get('db', 'database')
BROKER_TRANSPORT = 'sqlalchemy'
BROKER_HOST = dburi
BROKER_URI = dburi
CELERY_RESULT_BACKEND = 'database'
CELERY_RESULT_DBURI = dburi