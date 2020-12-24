# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /data/code/pracmln/python3/pracmln/utils/locs.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 587 bytes
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