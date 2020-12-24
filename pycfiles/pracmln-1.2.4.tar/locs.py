# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/utils/locs.py
# Compiled at: 2018-04-24 04:48:32
import os, appdirs
from pracmln._version import APPNAME, APPAUTHOR
root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
user_data = appdirs.user_data_dir(APPNAME, APPAUTHOR)
if os.path.basename(root).startswith('python'):
    root = os.path.realpath(os.path.join(root, '..'))
    app_data = root
else:
    app_data = appdirs.site_data_dir(APPNAME, APPAUTHOR)
    if not os.path.exists(app_data):
        app_data = user_data
trdparty = os.path.join(app_data, '3rdparty')
examples = os.path.join(app_data, 'examples')
etc = os.path.join(app_data, 'etc')