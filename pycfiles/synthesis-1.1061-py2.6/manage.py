# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/manage.py
# Compiled at: 2010-08-05 11:04:07
from migrate.versioning.shell import main
from conf import settings
main(url='postgres://%s:%s@%s:%s/%s' % (
 settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_PORT, settings.DB_DATABASE), repository='Synthesis_Repository')