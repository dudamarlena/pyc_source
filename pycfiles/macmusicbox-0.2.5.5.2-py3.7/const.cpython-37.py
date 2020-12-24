# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/NEMbox/const.py
# Compiled at: 2020-03-16 06:19:50
# Size of source mod 2**32: 612 bytes
from __future__ import print_function, unicode_literals, division, absolute_import
import os

class Constant(object):
    conf_dir = os.path.join(os.path.expanduser('~'), '.netease-musicbox')
    download_dir = os.path.join(os.path.expanduser('~'), 'Music/网易云音乐')
    config_path = os.path.join(conf_dir, 'config.json')
    storage_path = os.path.join(conf_dir, 'database.json')
    cookie_path = os.path.join(conf_dir, 'cookie')
    log_path = os.path.join(conf_dir, 'musicbox.log')
    cache_path = os.path.join(conf_dir, 'nemcache')