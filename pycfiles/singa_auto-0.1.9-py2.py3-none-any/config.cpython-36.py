# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/config.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 982 bytes
import os
APP_SECRET = os.environ.get('APP_SECRET', 'singa_auto')
SUPERADMIN_EMAIL = 'superadmin@singaauto'
SUPERADMIN_PASSWORD = os.environ.get('SUPERADMIN_PASSWORD', 'singa_auto')