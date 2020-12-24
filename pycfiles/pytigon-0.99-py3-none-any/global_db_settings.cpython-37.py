# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/pytigon/pytigon/prj/schportal/global_db_settings.py
# Compiled at: 2019-03-17 14:25:22
# Size of source mod 2**32: 706 bytes
import os

def setup_databases(app_name):
    p = os.path.expanduser('~')
    db_name = os.path.join(p, '.pytigon/%s/%s.db' % (app_name, app_name))
    dbs = {'default': {'ENGINE':'django.db.backends.postgresql', 
                 'NAME':'pytigon', 
                 'USER':'pytigon', 
                 'PASSWORD':'PkozieniceL1', 
                 'HOST':'pytigon.cloud'}}
    return (
     dbs, None)